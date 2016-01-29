# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:40:30 2016

@author: w_ryan
"""

#library to send email addresses
import smtplib

#library to get passwords
import getpass

#library to navigate directories
import os

#library to read CSVs
import csv

#libraries to check email addresses
import re
import dns.resolver
import socket
import smtplib

#set directory
os.chdir('C:/Users/w_ryan/emailer/')



#%% import email text
emails_csv = csv.reader(open('email_list.csv'), delimiter=',')

email_list = list(emails_csv)

emails = []
links = []

for entry in range(1,len(email_list)):
    emails.append(email_list[entry][0])
    links.append(email_list[entry][1])

#%%

#Import body text
dog_csv = csv.reader(open('dog_facts.csv'), delimiter=',')

dog_list = list(dog_csv)

facts = []

for entry in range(1,len(dog_list)):
    facts.append(dog_list[entry][0])


#%% Generate potential email structures







#%% Test potential email structures

#check initial email address
    domain_name = 'emailhippo.com'
    prefix = 'info'
    
def check_email(prefix, domain_name):
    #Create full email address for checking
    email_addy = prefix + "@" + domain_name
    
    #Check using Regex that an email meets minimum requirements, throw an error if not
    #This should never be triggered if you're generating the last name/first name combos accurately
    addressToVerify = email_addy
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    
    if match == None:
    	print('Bad Syntax')
    	raise ValueError('Bad Syntax')
    
    #get the MX record for the domain
    records = dns.resolver.query(domain_name, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    
    #check if the email address exists
    # Get local server hostname
    host = socket.gethostname()
    
    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)
    
    # SMTP Conversation
    server.connect(mxRecord)
    server.helo(host)
    server.mail('me@domain.com')
    code, message = server.rcpt(str(addressToVerify))
    server.quit()
    
    # Assume 250 as Success
    if code == 250:
    	print('Success')
    else:
    	print('Bad')
     
 
 
 

#%% Start email client


# Script to send emails
print("Username")
gm_username = "fundogfacts4you@gmail.com"
print("Password")
gm_pass = "Freako312"

session = smtplib.SMTP('smtp.gmail.com', 587)
session.ehlo()
session.starttls()
session.login(gm_username, gm_pass)

#%% Send individual emails function

def send(recipient, email_subject, link):
    
    body_of_email = "Hi, you have been selected to receive a great link and stuff. Here is your very special link: " + link
    headers = "\r\n".join(["from: " + gm_username,
                           "subject: " + email_subject,
                           "to: " + recipient,
                           "mime-version: 1.0",
                           "content-type: text/html"])
    
    # body_of_email can be plaintext or html!                    
    content = headers + "\r\n\r\n" + body_of_email
    session.sendmail(gm_username, recipient, content)
    return


#%% send the emails

for entry in range(0,len(emails)):
    send(emails[entry], "Special offer", links[entry])



