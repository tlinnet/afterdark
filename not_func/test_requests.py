import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument('-m',  '--mail', required=True, help="Input your mail")
parser.add_argument('-p',  '--passwd', required=True, help="Input your passwords")
parser.add_argument('-c',  '--conf', action='store_true', help="configure")
args = parser.parse_args()

#print(args.conf)
print("Logging in for user: %s"%args.mail)

#login = r'https://adfs.netcompany.com/adfs/ls?version=1.0&action=signin&realm=urn%3AAppProxy%3Acom&appRealm=01de8a3b-f6f2-e811-8154-0050568c6b3d&returnUrl=https%3A%2F%2Fafterdark.netcompany.com%2F'
login = "https://afterdark.netcompany.com/"
url = "https://afterdark.netcompany.com/"
#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'}
headers["Referer"] = url


with requests.Session() as s:
    r = s.get(login, headers=headers)
    #print(r.text)
    csrftoken = s.cookies['SAMLResponse']
    payload = {'SAMLResponse':csrftoken, 'UserName': args.mail, 'Password': args.passwd}
    #payload = {'Login.userNameInput': args.mail, 'Login.passwordInput': args.passwd}
    p = s.post(login, data=payload, headers=headers)   
    r2 = s.get(url, headers=headers)
    print(r2.text)
    
    #r = s.get(url, headers=headers)

#r = requests.post(url, data=payload)
#r = requests.get(url)
#print(r.text)
