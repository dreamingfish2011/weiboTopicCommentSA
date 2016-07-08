__author__ = 'zhuhongmei'
# encoding=utf-8
#!/usr/bin/python3
########测试requests的cookie和session
import requests
print("-----cookie test--------------")
params= {'username':'Ryan','password':'password'}
r = requests.post("http://pythonscraping.com/pages/cookies/welcome.php",data=params)
print(r.text)
print(r.cookies.get_dict())
print("-------------------")
r = requests.get("http://pythonscraping.com/pages/cookies/profile.php",cookies=r.cookies)
print(r.text)

print("-----session test--------------")
session = requests.session()
params= {'username':'username','password':'password'}
s = session.post("http://pythonscraping.com/pages/cookies/welcome.php",data=params)
print(s.cookies.get_dict())
s = session.get("http://pythonscraping.com/pages/cookies/profile.php")
print(s.text)