import getpass, json, sys, os, os.path, time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException



def get_credentials():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m',  '--mail', required=False, help="Input your mail")
    parser.add_argument('-p',  '--passwd', required=False, help="Input your passwords")
    args = parser.parse_args()

    if args.mail == None:
        print("Please input your mail")
        args.mail = input()
    if args.passwd == None:
        print("Please input your password: This field does not show any keypress.")
        args.passwd =  getpass.getpass()

    return args.mail, args.passwd

class Afterdark:
    def __init__(self, mail, passwd):
        self.mail = mail
        self.passwd = passwd

        self.url = "https://afterdark.netcompany.com/"
        self.url_events = "https://afterdark.netcompany.com/event-calendar/"

        self.waittime = 1 # min
        self.sleeptime = 10 # s
        self.looptime = datetime.now() + timedelta(minutes=self.waittime)

        self.driver = None
        self.use_driver = "chrome"
        #self.use_driver = "phantom"

    def start_driver(self):
        if self.driver == None:
            #print("Driver starting")
            if self.use_driver == "phantom":
                self.driver = webdriver.PhantomJS()
            else:
                options = webdriver.ChromeOptions()
                options.add_argument('headless')
                options.add_argument('--log-level=3')
                #options.add_argument('--disable-extensions')
                 #options.add_argument('window-size=1200x600')
                self.driver = webdriver.Chrome(options=options)

    # Login
    def login(self):
        self.start_driver()
        self.driver.get(self.url)
        title = self.driver.title
        print(title)
        if title == "Log på":
            print("Logging in for user: %s"%self.mail)
            username = self.driver.find_element_by_id('userNameInput').send_keys(self.mail)
            password = self.driver.find_element_by_id('passwordInput').send_keys(self.passwd)
            self.driver.get_screenshot_as_file('page_01_login.png')
            login = self.driver.find_element_by_id('submitButton')
            login.click()
            self.driver.get_screenshot_as_file('page_02_after_login.png')

        title = self.driver.title
        if title == "Log på":
            print(title)
            print("Failed to login")
            sys.exit()

    def scroll_wait(self, snr=1000, delay=10, href="christmas-party-2018"):
        snr_tot = snr
        delay_i = 0
        delay_per_round = 1
        print("\nWaiting for page")
        found = False
        while not found and delay_i < delay:
            try:
                #myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
                myElem = WebDriverWait(self.driver, delay_per_round).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='%s']"%href)))
                #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, ".//a[contains(@href,'christmas-party-2018')]")))
                #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, ".//a[contains(@href,'end-of-season-celebration')]")))
                #print("Page is ready!\n")
                found = True
            except TimeoutException:
                #print("Loading took too much time!\n")
                found = False
                self.driver.execute_script("window.scrollTo(0, %i);"%snr_tot)
                snr_tot += snr
                delay_i += delay_per_round
                #print(found, delay_i)

    def p_ids(self):
        ids = self.driver.find_elements_by_xpath('//*[@id]')
        for ii in ids:
            #print ii.tag_name
            print(ii.get_attribute('id'))
        print()

    def p_event_titles(self, do_print=False):
        ids = self.driver.find_elements_by_class_name("event-link")
        res = []
        for ii in ids:
            #print ii.tag_name
            title = ii.get_attribute('title')
            href = ii.get_attribute('href')
            if do_print:
                print(title)
            res.append([title, href])
        print()
        return res

    def find_event_signup(self, event_list):
        res = []
        for title, href in event_list:
            self.driver.get(href)
            signup_elements = self.driver.find_elements_by_class_name("event-signup")
            signup = False
            signup_link = ""
            if len(signup_elements) > 0:
                signup = True
                link_element = self.driver.find_element_by_link_text("Sign me up")
                signup_link = link_element.get_attribute('href')

            date_element = self.driver.find_element_by_css_selector("h2.event-date.d-block")
            date_text = date_element.text
            time_element = self.driver.find_element_by_css_selector("span.event-timed-block")
            time_text = time_element.text.replace(" ","")
            do  = datetime.strptime(date_text, '%A, %d. %B %Y')

            res.append([title, href, signup, signup_link, do, time_text])
        return res

    # Load forntpage
    def recent_events(self):
        print("###############################")
        print("# Front Page - Recent Events  #")
        print("###############################")
        self.driver.get(self.url)
        #self.scroll_wait(snr=2000, delay=10, href="christmas-party-2018")
        # Print event titles
        p_event_titles(do_print=True)

    # Go to events
    def list_event_calendar(self):
        print("###############################")
        print("# Event calendar              #")
        print("###############################")
        self.driver.get(self.url_events)
        self.scroll_wait(snr=2000, delay=4, href="")
        self.driver.get_screenshot_as_file('page_03_events.png')
        # Print event titles
        event_list = self.p_event_titles(do_print=False)
        signup_list = self.find_event_signup(event_list)

        for title, href, signup, signup_link, date, time in signup_list:
            print("Signup: %-5s %s %s : %-45s  Link: %s"%(signup, date.strftime('%Y-%m-%d'), time, title, signup_link))

    def read_or_create_conf(self):
        home = os.path.expanduser("~")
        jfname = "afterdark_conf.json"
        fout = os.path.join(home, jfname)
        if not os.path.isfile(fout):
            outfile = open(fout, "w")
            data = {}
            json.dump(data, outfile, indent=4)
        with open(fout) as json_file:  
            data = json.load(json_file)
        return data

    def loop_time(self):
        while datetime.now() < self.looptime:
            print("Sleeping until %s > %s"% (datetime.now().strftime('%H:%M:%S'), self.looptime.strftime('%H:%M:%S')) )
            time.sleep(self.sleeptime)
        self.looptime = datetime.now() + timedelta(minutes=self.waittime)
        print()

    def make_conf(self):
        print()
        print("1: Continue ")
        print("2: Make configurations")
        print("0: Exit")
        choice = input("Make a choice: ") or "1"
        if choice == "1":
            pass
        elif choice == "2":
            print("Making configurations")
        elif choice == "0":
            print("Exit")
            sys.exit()
        else:
            pass

if __name__ == "__main__":
    mail, passwd = get_credentials()
    Ad = Afterdark(mail, passwd)
    Ad.login()
    Ad.list_event_calendar()
    while True:
        try:
            print()
            print("Hit 'Ctrl+c' to Exit or make configurations")
            Ad.loop_time()
            Ad.list_event_calendar()
        except (KeyboardInterrupt, SystemExit):
            Ad.make_conf()
    
    print("\nDone")
    #print("\nPress any key to exit")
    #x = input()
