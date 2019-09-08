# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:13:14 2019
Source :
    https://www.guru99.com/xpath-selenium.html
    http://ashishkhan.com/blog/buddy-whatsapp-chat-bot-with-python
    https://codepad.co/snippet/whatsapp-bot-using-selenium-with-python
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#multi-valued-attributes
    https://selenium-python.readthedocs.io/locating-elements.html
@author: Olan
"""
#%% Import dependencies
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from requests import get
from bs4 import BeautifulSoup as bs
import keyboard
import click
import os
import sys
import csv
import threading

import pandas as pd

# for periodic task 
import time
from timeloop import Timeloop
from datetime import timedelta

tl = Timeloop()

# Replace below path with the absolute path of the \#chromedriver in your computer
dirname, filename = os.path.split(os.path.abspath(__file__))
print(dirname)

driver = webdriver.Chrome(dirname + '/chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 100)

# Replace 'My Bsnl' with the name of your friend or group name

#%% Testing
target = '"My Number"'
x_arg = '//span[contains(@title,' + target + ')]'
group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
print (group_title)
print ("Wait for few seconds")
group_title.click()

url = driver.page_source
soup = bs(url, "lxml")
print (" =========" )
print(soup.find_all(class_="FTBzM")[-1].prettify())
print (" =========" )
print(soup.find_all(class_="FTBzM")[-2].prettify())


#%%
def getChatFromWA(ChatRoom):
    # ================= OPEN CHAT ROOM =====================
    print("click chat room ")
    x_arg = '//span[contains(@title,' + ChatRoom + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
#    print (group_title)
    print ("Wait for few seconds")
    group_title.click()    
    
    # =================== GET THE CHAT ======================
    url = driver.page_source
    soup = bs(url, "lxml")
    print("get the chat")
    try:
        gotchat = soup.find_all(class_="FTBzM")[-1] # searching node for last chat
        gottext = gotchat.find_all("span", class_="selectable-text invisible-space copyable-text")[-1]
#        gothour = gotchat.find_all("div", role="button")[-1].contents[0]
        gotdate_hour = gotchat.find_all("div", class_="copyable-text")[0].attrs['data-pre-plain-text']
    except IndexError:
        gotchat = 'null'
#    print(gotchat.prettify())
    
    # ================= PARSING DATA CHAT ============
    print("parsing data from chat ")
    chatdict = {}
    hour = gotdate_hour.split(']')[0][1:].split(',')[0].strip()  #parsing gotdate_hour to get hour 
    date = gotdate_hour.split(']')[0][1:].split(',')[1].strip()  #parsing gotdate_hour to get date
    senderName = gotdate_hour.split(']')[1].strip()[:-1]         #parsing gotdate_hour to get sender name
    chatdict['hour'] = hour
    chatdict['date'] = date
    chatdict['text'] = gottext.string
    chatdict['sender'] = senderName
#    print(gotdate_hour)
    return chatdict
    #END GETCHATFROMWA
#%%    sdfsdfsf
print(getChatFromWA('"My Number"'))
#%% test
prevChat = {}
def isNewChat(prevChat, newChat,botname):
    if not prevChat.get('date'):
        return True
    if (newChat['sender'] != botname): # request is not from bot itself
        if (prevChat['date'] != newChat['date']):
            return True
        else: 
            if (prevChat['hour']!=newChat['hour']):
                return True
            else:
                if (prevChat['text']!=newChat['text']):
                    return True
                else:
                    return False
    else:
        return False        
    #END :isNewChat

target = '"My Number"'
tl = Timeloop()
@tl.job(interval=timedelta(seconds=3))
def sample_job_every_10s():
    global prevChat
    recentChat = getChatFromWA(target)
    print ('ini recent chat')
    print (recentChat)
    if (isNewChat(prevChat, recentChat, "Yoland Nababan") == True):
        print('ini textnya')
        print(recentChat['text'])
        prevChat = recentChat
        doCommand(recentChat['text'])
    else:
        print('IDLE')
#    print('oke')

def sendTexttoWA(messageText, target):
    #from selenium import webdriver
#    target = '"' + e3.get() + '"'
    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(messageText + '\n')
    
def doCommand(command):
    text = 'BOT: ' + command
    sendTexttoWA(text,target)
if __name__ == "__main__":
    tl.start(block=True)

#Store chat
#def storeChat(filepath, filename):
##store chat if it is unique
#    threading.Timer(5.0, repeatfun).start()
    
#driver.close()
#sys.exit()