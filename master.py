# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:40:30 2016

@author: w_ryan
"""

import smtplib
import getpass
import os
import csv

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



