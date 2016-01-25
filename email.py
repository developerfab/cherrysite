#!/usr/bin/python

import smtplib

sender = 'from@fromdomain.com'
receivers = ['fab7696650@gmail.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <fab7696650@gmail.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message)         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"
