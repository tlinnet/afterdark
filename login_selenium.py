import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
#from selenium.webdriver.remote.remote_connection import LOGGER
#import logging
#LOGGER.setLevel(logging.WARNING)

parser = argparse.ArgumentParser()
parser.add_argument('-m',  '--mail', required=True, help="Input your mail")
parser.add_argument('-p',  '--passwd', required=True, help="Input your passwords")
parser.add_argument('-c',  '--conf', action='store_true', help="configure")
args = parser.parse_args()

#print(args.conf)
print("Logging in for user: %s"%args.mail)

url = "https://afterdark.netcompany.com/"
url_events = "https://afterdark.netcompany.com/event-calendar/"
use_driver = "chrome"
#use_driver = "phantom"

if use_driver == "phantom":
    driver = webdriver.PhantomJS()
else:
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--log-level=3')
    #options.add_argument('--disable-extensions')
     #options.add_argument('window-size=1200x600')
    driver = webdriver.Chrome(options=options)
    print()

def p_ids(mydriver):
    ids = mydriver.find_elements_by_xpath('//*[@id]')
    for ii in ids:
        #print ii.tag_name
        print(ii.get_attribute('id'))
    print()

def p_event_titles(mydriver, do_print=False):
    ids = mydriver.find_elements_by_class_name("event-link")
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

def scroll_wait(snr=1000, delay=10, href="christmas-party-2018"):
    snr_tot = snr
    delay_i = 0
    delay_per_round = 1
    print("\nWaiting for page")
    found = False
    while not found and delay_i < delay:
        try:
            #myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
            myElem = WebDriverWait(driver, delay_per_round).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='%s']"%href)))
            #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, ".//a[contains(@href,'christmas-party-2018')]")))
            #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, ".//a[contains(@href,'end-of-season-celebration')]")))
            #print("Page is ready!\n")
            found = True
        except TimeoutException:
            #print("Loading took too much time!\n")
            found = False
            driver.execute_script("window.scrollTo(0, %i);"%snr_tot)
            snr_tot += snr
            delay_i += delay_per_round
            #print(found, delay_i)

def find_event_signup(event_list):
    res = []
    for title, href in event_list:
        driver.get(href)
        signup_elements = driver.find_elements_by_class_name("event-signup")
        signup = False
        signup_link = ""
        if len(signup_elements) > 0:
            signup = True
            link_element = driver.find_element_by_link_text("Sign me up")
            signup_link = link_element.get_attribute('href')

        date_element = driver.find_element_by_css_selector("h2.event-date.d-block")
        date_text = date_element.text
        time_element = driver.find_element_by_css_selector("span.event-timed-block")
        time_text = time_element.text.replace(" ","")
        do  = datetime.strptime(date_text, '%A, %d. %B %Y')

        res.append([title, href, signup, signup_link, do, time_text])
    return res

# Login
driver.get(url)
username = driver.find_element_by_id('userNameInput').send_keys(args.mail)
password = driver.find_element_by_id('passwordInput').send_keys(args.passwd)
driver.get_screenshot_as_file('page_01_login.png')
login = driver.find_element_by_id('submitButton')
login.click()
driver.get_screenshot_as_file('page_02_after_login.png')

# Load forntpage
if False:
    print("###############################")
    print("# Front Page - Recent Events  #")
    print("###############################")
    driver.get(url)
    #scroll_wait(snr=2000, delay=10, href="christmas-party-2018")
    # Print event titles
    p_event_titles(driver, do_print=True)

# Go to events
if True:
    print("###############################")
    print("# Event calendar              #")
    print("###############################")
    driver.get(url_events)
    scroll_wait(snr=2000, delay=4, href="")
    driver.get_screenshot_as_file('page_03_events.png')
    # Print event titles
    event_list = p_event_titles(driver, do_print=False)
    signup_list = find_event_signup(event_list)

    for title, href, signup, signup_link, date, time in signup_list:
        print("Signup: %-5s %s %s : %-45s  Link: %s"%(signup, date.strftime('%Y-%m-%d'), time, title, signup_link))
