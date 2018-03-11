#!/usr/local/bin/python
# jumble.py - To find the 9-letter word from a jumbled matrix
# Copyright (c) 2018; A.V. Sivaprasad. All Rights Reserved.
# Created on Mar 10, 2018.
# Last modified on: Mar 11, 2018
#-------------------------------------------------------------------------------
# Import modules for CGI handling 
print ("Content-type:text/html\r\n\r\n")
import os
import cgi, cgitb 
cgitb.enable()
import smtplib
import base64
import sys
from getpass import getpass
from email_utils import EmailConnection, Email
from secrets import Password
#-------------------------------------------------------------------------------
# Globals
#-------------------------------------------------------------------------------
mail_server = 'smtp.webgenie.com'
name = 'Arapaut Sivaprasad'
email = 'avs@webgenie.com'
password = Password()
subject = 'Sending mail attachment easily with Python'
attachments = [sys.argv[0]]
#-------------------------------------------------------------------------------

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
to_name = form.getvalue('Use_name')
to_email  = form.getvalue('User_email')
User_phone  = form.getvalue('User_phone')
message  = form.getvalue('Message')

message = "%s<br><b>Phone:</b> %s" % (message,User_phone)

server = EmailConnection(mail_server, email, password)
email = Email(from_='"%s" <%s>' % (name, email), #you can pass only email
              to='"%s" <%s>' % (to_name, to_email), #you can pass only email
              subject=subject, 
              message=message, 
              attachments=['/var/www/vhosts/webgenie.com/httpdocs/AI-Genie/p7.png'])
server.send(email)
server.close()

def unused():
	sender = 'avs@webgenie.com'
	receivers = ['avs2904@webgenie.com']
	message = """From: From Person <%s>
	To: To Person <to@todomain.com>
	MIME-Version: 1.0
	Content-type: text/html
	Subject: SMTP e-mail test
	
	Email: %s
	Phone: %s
	Message: %s
	This is a <b>test e-mail message.</b>
	""" % (Use_name, User_email, User_phone, Message)

	message = part1 + part2 + part3


	#print ("Content-type:text/html\r\n\r\n")
	print ("<html>")
	print ("<head>")
	print ("<title>Hello - Second CGI Program</title>")
	print ("</head>")
	print ("<body>")
	print ("<h2>Hello %s %s</h2>" % (Use_name, User_email))
	print ("</body>")
	print ("</html>")

