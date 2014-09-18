# -*- coding: utf-8 -*-

__author__ = 'bilibili'

import smtplib
 
fromaddr = 'fromuser@gmail.com'  
toaddrs  = 'touser@gmail.com'  
msg = 'There was a terrible error that occured and I wanted you to know!'  

username = 'username'  
password = 'password'  

smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=120) 
server.starttls()  
server.login(username,password)  
server.sendmail(fromaddr, toaddrs, msg)  
server.quit() 