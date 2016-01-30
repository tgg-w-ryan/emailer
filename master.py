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

#for making the program wait
import time

#set directory

working_path = 'C:/Users/w_ryan/emailer/'


os.chdir(working_path)


#%% function for cleaning lists

#Do some cleaning of the imported text to make sure it's lower case with 
# no whitespace
def clean_list(dirty_list):
    for i in range(0,len(dirty_list)):
        #convert to lowercase
        dirty_list[i] = dirty_list[i].lower()
        #strip all whitespace
        dirty_list[i] = "".join(dirty_list[i].split())
    return(dirty_list)


#%% import email text
emails_csv = csv.reader(open('email_list.csv'), delimiter=',')

email_list = list(emails_csv)

first_names = []
last_names = []
domains = []
company_names = []

#import everything
for entry in range(1,len(email_list)):
    first_names.append(email_list[entry][0])
    last_names.append(email_list[entry][1])
    domains.append(email_list[entry][2])
    company_names.append(email_list[entry][3])

#Clean everything

#turn lower, remove whitespace
first_names = clean_list(first_names)
last_names = clean_list(last_names)
domains = clean_list(domains)
company_names = clean_list(company_names)

#get rid of leading "www"s in domain names
for i in range(0,len(domains)):
    if 'www.' in domains[i]:
        domains[i] = domains[i].split('www.')[1]
    else:
        1
        
#%% Functions to generate potential email structures


#Turn a  prefix and suffix into an email
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
    new_res = []
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
    #get rid of nested lists
    new_res = results[0] + results[1] + results[2] + results[3]
    new_res.append(results[4])
    new_res.append(results[5])
    new_res.append(results[6])
    new_res.append(results[7])
    return(new_res)

#generate email addresses
def gen_addresses(prefixes, domain):
    results = []
    #create emails
    for i in range(0,len(prefixes)):
        addy = emailize(prefixes[i], domain)
        results.append(addy)
    #clear duplicates
    results = list(uniqify_list(results))
    #return list of email addresses
    return(results)

# Generate the email address for one entry
def make_addy(fn, ln, domain):
    prefix = gen_prefix(fn, ln)
    addresses = gen_addresses(prefix, domain)
    return(addresses)



#%% Functions to check domains and emails

#Check if a domain always returns 250 basically no matter what
def check_domain(domain_name):
    addressToVerify = "qwertyboy98plm@" + domain_name
    #Step 1: Getting MX record
    #get the MX record for the domain
    records = dns.resolver.query(domain_name, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    
    #Step 2: ping email server
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
    elif code == 450:
     return('Rate limited')
     time.sleep(5)
    else:
    	return('N')

#Check if an email address exists
def ping_email(email_address):
    #Step 1: Check email
    #Check using Regex that an email meets minimum requirements, throw an error if not
    #This should never be triggered if you're generating the last name/first name combos accurately
    addressToVerify = email_address
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    
    if match == None:
    	print('Bad Syntax in ' + addressToVerify)
    	raise ValueError('Bad Syntax')
    
    #Step 2: Getting MX record
    #Pull domain name from email address
    domain_name = email_address.split('@')[1]
    
    #get the MX record for the domain
    records = dns.resolver.query(domain_name, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)
    
    #Step 3: ping email server
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

#Check all domains
def check_domains(domains):
    domain_check = []
    for i in range(0,len(domains)):
        domain_check.append(check_domain(domains[i]))
        #add a pause so as to not get banned
        time.sleep(3)
    return(domain_check)

#Check all emails for a given person
def check_emails(addresses):
    email_check = []
    for i in range(0,len(addresses)):
        email_check.append(ping_email(addresses[i]))
        #add a pause so as to not get banned
        time.sleep(3)
    return(email_check)


#%% Check all names to find correct emails

#do the domain checks
domain_checks =  check_domains(domains)

#make a list of all the email address combos
email_lol = []
for i in range(0,len(first_names)):
    address_list = make_addy(first_names[i], last_names[i], domains[i])
    email_lol.append(address_list)

#Run the email checks for all the email address combos where domains were ok
email_results = []
for i in range(0,len(email_lol)):
    if domain_checks[i] == 'N':
        email_results.append(check_emails(email_lol[i]))
    else:
        email_results.append('Invalid domain, cannot check')


#%% Pull out the email addresses which worked

#Check for invalid domains or those with multiple addresses found, they will be excluded
email_list_status = []
for i in range(0,len(email_results)):
    if email_results[i].count('Y') == 1:
        email_list_status.append('One match')
    elif email_results[i] == 'Invalid domain, cannot check':
        email_list_status.append('Invalid')
    elif email_results[i].count('Y') > 1:
        email_list_status.append('Multiple matches')
    elif email_results[i].count('Y') == 0:
        email_list_status.append('No match but valid')
    else:
        email_list_status.append('Error')

#Check for invalid domain's indexes
invalid_domains = [i for i,x in enumerate(email_list_status) if x == 'Invalid']

single_matches = [i for i,x in enumerate(email_list_status) if x == 'One match']

multiple_matches = [i for i,x in enumerate(email_list_status) if x == 'Multiple matches']

no_matches = [i for i,x in enumerate(email_list_status) if x == 'No match but valid']

#Create list of working email addresses
working_emails = []

for i in range(0,len(email_results)):
    if i in invalid_domains:
        working_emails.append('ERROR: Invalid domain')
    elif i in multiple_matches:
        emails_concat = []
        for u in range(0,len(email_results[i])):
            
            if email_results[i][u] == 'N':
                1
            else:
               emails_concat.append(email_lol[i][u])
        working_emails.append(emails_concat)
    elif i in no_matches:
        working_emails.append('ERROR: No matches')
    elif i in single_matches:
        for u in range(0,len(email_results[i])):
            if email_results[i][u] == 'N':
                1
            else:
               working_emails.append(email_lol[i][u])
    else: 
        working_emails.append('ERROR: Last step failed')
       

#%% Write results to a new CSV

header = ('First', 'Last', 'Domain', 'Company', 'Email')
output_list = [first_names, last_names, domains, company_names, working_emails]
      
with open('output.csv', 'w', newline='') as myfile:
    wr = csv.writer(myfile, delimiter=',')
    wr.writerow(header)
    for row in zip(first_names, last_names, domains, company_names, working_emails):
        wr.writerow(row)







#==============================================================================
# #%% Start email client
# 
# # get username and pass
# print("Username")
# gm_username = "fundogfacts4you@gmail.com"
# print("Password")
# gm_pass = "Freako312"
# 
# #send stuff
# session = smtplib.SMTP('smtp.gmail.com', 587)
# session.ehlo()
# session.starttls()
# session.login(gm_username, gm_pass)
# 
# #%% Send individual emails function
# 
# def send(recipient, email_subject, link):
#     
#     body_of_email = "Hi, you have been selected to receive a great link and stuff. Here is your very special link: " + link
#     headers = "\r\n".join(["from: " + gm_username,
#                            "subject: " + email_subject,
#                            "to: " + recipient,
#                            "mime-version: 1.0",
#                            "content-type: text/html"])
#     
#     # body_of_email can be plaintext or html!                    
#     content = headers + "\r\n\r\n" + body_of_email
#     session.sendmail(gm_username, recipient, content)
#     return
# 
# 
# #%% send the emails
# 
# for entry in range(0,len(emails)):
#     send(emails[entry], "Special offer", links[entry])
#==============================================================================



