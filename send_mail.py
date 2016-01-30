# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 19:52:15 2016

@author: w_ryan
"""
#%%

#NOTE: YOU CAN ONLY USE THIS SCRIPT FOR PERSONAL EMAILS, NOT COMMERCIAL ONES, AS FAR AS I KNOW

# DONT LOAD IN ANY EMAILS WHICH PEOPLE HAVENT GIVEN YOU W FULL KNOWLEDGE

#%%



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

#%%
working_path = 'C:/Users/w_ryan/emailer/'


os.chdir(working_path)

#%% import email text

emails_csv = csv.reader(open('output.csv'), delimiter=',')

email_list = list(emails_csv)

first_names = []
last_names = []
domains = []
companies = []
working_emails = []

#import everything
for entry in range(1,len(email_list)):
    first_names.append(email_list[entry][0])
    last_names.append(email_list[entry][1])
    domains.append(email_list[entry][2])
    companies.append(email_list[entry][3])
    working_emails.append(email_list[entry][4])



#%% Start email client

# get username and pass
print("Username")
gm_username = "fundogfacts4you@gmail.com"
print("Password")
gm_pass = "Freako312"

#send stuff
session = smtplib.SMTP('smtp.gmail.com', 587)
session.ehlo()
session.starttls()
session.login(gm_username, gm_pass)

#%% Send individual emails function

def send(sender, recipient, first_name, last_name, subj_insert, body_insert1, body_insert2):
    
    body_of_email = "Hey, <br>" + first_name + ", you have been selected to receive a great link and stuff. I think it will be very helpful for " + body_insert1
    headers = "\r\n".join(["from: " + sender,
                           "subject: Tell me more about what you're up to at " + subj_insert + "!",
                           "to: " + recipient,
                           "mime-version: 1.0",
                           "content-type: text/html"])
    
    # body_of_email can be plaintext or html!                    
    content = headers + "\r\n\r\n" + body_of_email
    session.sendmail(gm_username, recipient, content)
    return


#%% send the emails

for i in range(0,len(working_emails)):
    send(gm_username, working_emails[i], first_names[i], last_names[i], companies[i], companies[i], companies[i])
    
    
    
    