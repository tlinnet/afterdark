import argparse
import re
import mechanize
import http.cookiejar
import time
import urllib

parser = argparse.ArgumentParser()
parser.add_argument('-m',  '--mail', required=True, help="Input your mail")
parser.add_argument('-p',  '--passwd', required=True, help="Input your passwords")
parser.add_argument('-c',  '--conf', action='store_true', help="configure")
args = parser.parse_args()

#print(args.conf)
print("Logging in for user: %s"%args.mail)

url = "https://afterdark.netcompany.com/"

# Start Browser
br = mechanize.Browser()
cj = http.cookiejar.LWPCookieJar()
br.set_cookiejar( cj ) 

# Broser options 
br.set_handle_equiv( True ) 
br.set_handle_gzip( True ) 
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
#br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]
#br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134' ) ]
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open(url)
br.select_form(nr=0)
br.submit()

br.select_form(nr=0)
br.form["UserName"] = args.mail
br.form["Password"] = args.passwd
br.submit()

br.select_form(nr=0)
br.submit()

rs = br.open(url)
print(rs.read())

#res = br.open(url)
#print(br.title())
#print(res.geturl())
#print(res.info())  # headers
#print(res.read())  # body

#if br.title() == "Log på":
#    br.select_form(id="loginForm")
#    br.set_all_readonly(False)
#    print(br.form)
#    br.form["UserName"] = args.mail
#    br.form["Password"] = args.passwd
#    print(br.form)

#    print()
    
#    br.select_form(id="options")
#    print(br.form)
    #br.form["Kmsi"] = False
    #br.find_control("AuthMethod").disabled = True
    #br.find_control("Kmsi").disabled = True
#    response = br.submit()

    #post_url, post_data, headers =  br.form.click_request_data()
    #params = {u'UserName': args.mail, u'Password':args.passwd}
    #data = urllib.parse.urlencode(params)
    #request = mechanize.Request( url )
    #res = mechanize.urlopen(request, data=data)
    #res = mechanize.urlopen(post_url, post_data)
    #res = mechanize.urlopen(post_url, data=data)
    #br.submit()
    #print(post_url)
    #print(post_data)
    #print(headers)
    
    #br.select_form(id="submitButton")
    #print(br.form)
    #req = mybrowser.click(type="submit", nr=1)
    #mybrowser.open(req)

# Wait some seconds
#time.sleep(5)

#print(br.title())
#print(response.read())

#print(res)
#print(res.info())  # headers
#print(res.read())  # body
