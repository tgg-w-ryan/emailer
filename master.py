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

first_names = []
last_names = []
domains = []
company_names = []

for entry in range(1,len(email_list)):
    first_names.append(email_list[entry][0])
    last_names.append(email_list[entry][1])
    domains.append(email_list[entry][2])
    company_names.append(email_list[entry][3])
    
    
    
    
#%%

#Import body text
dog_csv = csv.reader(open('dog_facts.csv'), delimiter=',')

dog_list = list(dog_csv)

facts = []

for entry in range(1,len(dog_list)):
    facts.append(dog_list[entry][0])


#%% Functions to enerate potential email structures

#Turna  prefix and suffix into an email
def emailize(prefix, suffix):
    prefix = str(prefix)
    suffix = str(suffix)
    email_str = prefix + '@' + suffix
    return(email_str)
    
#function to get all seperators
def all_seps(first, second):
    response_list = []
    str1 = first + "-" + second
    str2 = first + "_" + second
    str3 = first + "." + second
    str4 = first + second
    response_list.append(str1)
    response_list.append(str2)
    response_list.append(str3)
    response_list.append(str4)
    return(response_list)

#function to get all seperators backwards and forwards
def bckfwd(first, second):
    response = []
    response.append(all_seps(first, second))
    response.append(all_seps(second, first))
    #return a flattened list
    return([item for sublist in response for item in sublist])

#function to get all prefixes
def gen_prefix(fn, ln):
    #create list to store results
    results = []
    #Get initials
    fi = fn[:1]
    li = ln[:1]
    #Generate all possible prefixes
    results.append(bckfwd(fn, ln))
    results.append(bckfwd(fn, li))
    results.append(bckfwd(fi, ln))
    results.append(bckfwd(fi, li))
    results.append(fn)
    results.append(fi)
    results.append(ln)
    results.append(li)
    return([item for sublist in results for item in sublist])

#generate email addresses
def gen_addresses(prefixes, domain):
    results = []
    #create emails
    for i in range(0,len(prefixes)):
        addy = emailize(prefixes[i], domain)
        results.append(addy)
    #clear duplicates
    results = list(set(results))
    #return list of email addresses
    return(results)

# Generate the email address for one entry
def make_addy(fn, ln, domain):
    prefix = gen_prefix(fn, ln)
    addresses = gen_addresses(prefix, domain)
    return(addresses)



#%% Test potential email structures

#check initial email address
    domain_name = 'emailhippo.com'
    prefix = 'info'
    
def check_email(prefix, domain_name):
    #Create full email address for checking
    email_addy = prefix + "@" + domain_name
    
    #Step 1
    #Check using Regex that an email meets minimum requirements, throw an error if not
    #This should never be triggered if you're generating the last name/first name combos accurately
    addressToVerify = email_addy
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    
    if match == None:
    	print('Bad Syntax')
    	raise ValueError('Bad Syntax')
    
    #Step 2
    #get the MX record for the domain
    records = dns.resolver.query(domain_name, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    
    #Step 3
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
    	return('Y')
    else:
    	return('N')
     
 
 
 

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



