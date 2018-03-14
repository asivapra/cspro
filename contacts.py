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
#import hashlib
#-------------------------------------------------------------------------------
# Globals
#-------------------------------------------------------------------------------
mail_server = Secret('mailserver')
to_name = 'Arapaut Sivaprasad'
to_email = Secret('to_email')
password = Secret('pw')
subject = 'Uploading and sending file'
#-------------------------------------------------------------------------------
# Upload a file
#-------------------------------------------------------------------------------
def uploadfile(form):
	try: # Windows needs stdio set for binary mode.
	    import msvcrt
	    import uuid
	    msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
	    msvcrt.setmode (1, os.O_BINARY) # stdout = 1
	except ImportError:
	    pass
	
	# Generator to buffer file chunks
	def fbuffer(f, chunk_size=10000):
	   while True:
	      chunk = f.read(chunk_size)
	      if not chunk: break
	      yield chunk
	
	# A nested FieldStorage instance holds the file
	fileitem = form['file']

	# Test if the file was uploaded
	if fileitem.filename:
	
		# strip leading path from file name to avoid directory traversal attacks
		fn = os.path.basename(fileitem.filename)
#		print (fn); return		
		# Internet Explorer will attempt to provide full path for filename fix
#		fn = fn.split('\\')[-1]
		
		# This path must be writable by the web server in order to upload the file.
		path = '/tmp/'
		filepath = path + fn

		# Open the file for writing 
		f = open(filepath , 'wb', 10000)
		
		datalength = 0

		# Read the file in chunks
		for chunk in fbuffer(fileitem.file):
			f.write(chunk)
			datalength += len(chunk)
		f.close()
		return filepath
#-------------------------------------------------------------------------------
# Mail the form content with or without attachment
#-------------------------------------------------------------------------------
def mailit(name,email,phone,message_text,filepath):
	fileupload = filepath
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
	print ("location: http://www.webgenie.com/thanks.html\n\n")
#-------------------------------------------------------------------------------
# Call the main to read the form inputs. Check if re-Captcha passed and, then, call 'mailit()'
#-------------------------------------------------------------------------------
def main():	
	form = cgi.FieldStorage() 
	recaptcha  = form.getvalue('g-recaptcha-response');  recaptcha = 1
	if recaptcha:
		filepath = uploadfile(form);
		# Get data from fields
		name = form.getvalue('Use_name')
		email  = form.getvalue('User_email')
		phone  = form.getvalue('User_phone')
		message_text  = form.getvalue('Message')
		mailit(name,email,phone,message_text,filepath)

	else: print ("location: http://www.webgenie.com/nocaptcha.html\n\n")
#-------------------------------------------------------------------------------
#print ("Content-type:text/html\n\n")
main()
#-------------------------------------------------------------------------------

