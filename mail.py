import poplib
from email import parser
import requests
import os
import json

import getpass

class MailGun(object):
	"""docstring for MainGun"""
	def __init__(self, api_key, domain, recipient):
		super(MailGun, self).__init__()
		self.api_key = api_key
		self.domain = domain
		self.recipient = recipient
		self.url = "https://api.mailgun.net/v3/"+self.domain+"/messages"

	def send_message(self,sender,subject,body):
		return requests.post(self.url,auth=("api",self.api_key),data={"from":sender,"to":self.recipient,"subject":subject,"text":body})

		


home_dir = os.path.expanduser('~')
cred_dir = os.path.join(home_dir, '.webmail')
credential_path = os.path.join(cred_dir,'creds.txt')
if not os.path.exists(credential_path):
	if not os.path.exists(cred_dir):
		os.makedirs(cred_dir)

	creds = {}
	creds['webmail'] = raw_input("Please enter your webmail username:\n")
	creds['password'] = getpass.getpass()
	print("\n\nSelect your webmail server:\n[1] Teesta\n[2] Naambor\n[3] Disang\n[4] Tamdil\n[5] Dikrong")
	server_in = input("Enter the number corresponding to the server:\n")-1
	server_list = ['202.141.80.12','202.141.80.9','202.141.80.10','202.141.80.11','202.141.80.13']
	creds['server'] = server_list[server_in]
	creds['api'] = raw_input("Please enter you mailgun api-key:\n")
	creds['domain'] = raw_input("Please enter your mailgun sandbox url:\n")
	creds['to'] = raw_input("Please enter the email address you want to forward to:\n")
	creds['flast'] = input("Since this is your first time running the script, \nplease enter the number of existing emails you want to forward:\n")
	json.dump(creds, open(credential_path,'w'))
else:
	creds = json.load(open(credential_path,'r'))	



pop_conn = poplib.POP3_SSL(creds['server'])
pop_conn.user(creds['webmail'])
pop_conn.pass_(creds['password'])
total = len(pop_conn.list()[1])
if creds['flast']!=-1:
	creds['last'] = total - creds['flast'] 
	creds['flast'] = -1
# print total
#Get messages from server:
messages = [pop_conn.retr(i) for i in range(creds['last']+1,total+1)]

# print messages
# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]
# print messages[0]
#Parse message intom an email object:
mailSender = MailGun(creds['api'],creds['domain'],[creds['to']])
messages = [parser.Parser().parsestr(mssg) for mssg in messages]

for i,b in enumerate(messages):
	body = ""
	if b.is_multipart():
		for part in b.walk():
			ctype = part.get_content_type()
			cdispo = str(part.get('Content-Disposition'))
			if ctype == 'text/plain' and 'attachment' not in cdispo:
				body += part.get_payload(decode=True)  # decode
				break
	else:
		body += b.get_payload(decode=True)	  
	print mailSender.send_message(b['from'],b['subject'],body)

			  
pop_conn.quit()

creds['last'] = total
json.dump(creds, open(credential_path,'w'))

