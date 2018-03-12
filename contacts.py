#!/usr/local/bin/python
# jumble.py - To find the 9-letter word from a jumbled matrix
# Copyright (c) 2018; A.V. Sivaprasad. All Rights Reserved.
# Created on Mar 10, 2018.
# Last modified on: Mar 12, 2018
#-------------------------------------------------------------------------------
# Import the modules for CGI handling 
#-------------------------------------------------------------------------------
import os
import cgi, cgitb 
cgitb.enable()
import smtplib
import base64
import sys
from getpass import getpass
from email_utils import EmailConnection, Email
from secrets import Secret
#-------------------------------------------------------------------------------
# Globals
#-------------------------------------------------------------------------------
mail_server = Secret('mailserver')
to_name = 'Arapaut Sivaprasad'
to_email = Secret('to_email')
password = Secret('pw')
subject = 'Uploading and sending file'
#-------------------------------------------------------------------------------
# Mail the form content with or without attachment
#-------------------------------------------------------------------------------
def mailit(name,email,phone,message_text,base_filename):
#	global name,email,phone,message_text # Either export and import as global, or send as params
	
	if base_filename and base_filename != 'undefined': fileupload = '/var/www/vhosts/webgenie.com/httpdocs/Tmp/' + base_filename
	else: fileupload = ''
	message = "<br><b>Name:</b> %s" % (name)
	message = "%s<br><b>Email:</b> %s" % (message,email)
	message = "%s<br><b>Phone:</b> %s" % (message,phone)
	message = "%s<br><b>Message:</b> %s" % (message, message_text)
	
	server = EmailConnection(mail_server, email, password)
	if fileupload:
		email = Email(from_='"%s" <%s>' % (name, email), #you can pass only email
		      to='"%s" <%s>' % (to_name, to_email), #you can pass only email
		      subject=subject,  
		      message=message, 
		      attachments=[fileupload])
	else:
		email = Email(from_='"%s" <%s>' % (name, email), #you can pass only email
		      to='"%s" <%s>' % (to_name, to_email), #you can pass only email
		      subject=subject,  
		      message=message) 
		
	server.send(email)
	server.close()
	print ("Content-type:text/html\n\n")
	print("Your file (%s) has been uploaded and emailed." % base_filename)
#-------------------------------------------------------------------------------
# Call the main to read the form inputs. Check if re-Captcha passed and, then, call 'mailit()'
#-------------------------------------------------------------------------------
def main():	
#	global name,email,phone,message_text # Either export and import as global, or send as params
	
	# Create instance of FieldStorage. This will only work if CGI is in /cgi-bin 
	form = cgi.FieldStorage() 

	# Get data from fields
	name = form.getvalue('Use_name')
	email  = form.getvalue('User_email')
	phone  = form.getvalue('User_phone')
	message_text  = form.getvalue('Message')
	base_filename  = form.getvalue('fileupload')
	recaptcha  = form.getvalue('g-recaptcha-response')
	if recaptcha: mailit(name,email,phone,message_text,base_filename)
	else: print ("location: http://www.webgenie.com/nocaptcha.html\n\n")
#-------------------------------------------------------------------------------
main()
#-------------------------------------------------------------------------------

