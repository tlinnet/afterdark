# https://stackoverflow.com/questions/16512965/logging-into-saml-shibboleth-authenticated-server-using-python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  #imports

things_to_download= [a,b,c,d,e,f]     #The values changing in the url
options = Options()
options.headless = False
driver = webdriver.Chrome('D:/chromedriver.exe', options=options)
driver.get('https://website.to.downloadfrom.com/')
driver.find_element_by_id('username').send_keys("Your_username") #the ID would be different for different website/forms
driver.find_element_by_id('password').send_keys("Your_password")
driver.find_element_by_id('logOnForm').submit()
session = requests.Session()
cookies = driver.get_cookies()
for things in things_to_download:    
    for cookie in cookies: 
        session.cookies.set(cookie['name'], cookie['value'])
    response = session.get('https://website.to.downloadfrom.com/bla/blabla/' + str(things_to_download))
    with open('Downloaded_stuff/'+str(things_to_download)+'.pdf', 'wb') as f:
        f.write(response.content)            # saving the file
driver.close()
