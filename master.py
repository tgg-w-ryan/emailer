# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 17:40:30 2016

@author: w_ryan
"""

import smtplib


print("Username")
gm_username = input()
print("Password")
gm_pass = input()

session = smtplib.SMTP('smtp.gmail.com', 587)
session.ehlo()
session.starttls()
session.login(gm_username, gm_pass)

headers = "\r\n".join(["from: " + gm_username,
                       "subject: " + email_subject,
                       "to: " + recipient,
                       "mime-version: 1.0",
                       "content-type: text/html"])

# body_of_email can be plaintext or html!                    
content = headers + "\r\n\r\n" + body_of_email
session.sendmail(gm_username, recipient, content)