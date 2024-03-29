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

#%% Open WA
tl = Timeloop()

# Replace below path with the absolute path of the \#chromedriver in your computer
dirname, filename = os.path.split(os.path.abspath(__file__))
print(dirname)

driver = webdriver.Chrome(dirname + '/chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 100)

# Replace 'My Bsnl' with the name of your friend or group name

#%% Click trarget
target = '"My Number"'
x_arg = '//span[contains(@title,' + target + ')]'
group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
print (group_title)
print ("Wait for few seconds")
group_title.click()

url = driver.page_source
soup = bs(url, "lxml")
#print (" =========" )
#print(soup.find_all(class_="FTBzM")[-2].prettify())
#print (" =========" )
#print(soup.find_all(class_="FTBzM")[-1].prettify())


#%% Get Chat From WA
def getChatFromWA(ChatRoom):
    # ================= OPEN CHAT ROOM =====================
#    print("click chat room ")
    x_arg = '//span[contains(@title,' + ChatRoom + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
#    print (group_title)
#    print ("Wait for few seconds")
    group_title.click()    
    
    # =================== GET THE CHAT ======================
    url = driver.page_source
    soup = bs(url, "lxml")
#    print("get the chat")
    chatdict = {}
    try:
        gotchat = soup.find_all(class_="FTBzM")[-1] # searching node for last chat
    except IndexError as err:
        return None
        print ("Error : ", err)
        print('class name (maybe) rearranged')
    else:
        try:
            gottext = gotchat.find_all("span", class_="selectable-text invisible-space copyable-text")[-1]
            gotdate_hour = gotchat.find_all("div", class_="copyable-text")[0].attrs['data-pre-plain-text']
        except IndexError as error:
            print("ERROR: ", error)
            print("Last message is not a text")
            return None
        else:
            # ================= PARSING DATA CHAT ============
#            print("parsing data from chat ")
            hour = gotdate_hour.split(']')[0][1:].split(',')[0].strip()  #parsing gotdate_hour to get hour 
            date = gotdate_hour.split(']')[0][1:].split(',')[1].strip()  #parsing gotdate_hour to get date
            senderName = gotdate_hour.split(']')[1].strip()[:-1]         #parsing gotdate_hour to get sender name
            chatdict['hour'] = hour
            chatdict['date'] = date
            chatdict['text'] = gottext.string
            chatdict['sender'] = senderName            
            return chatdict
    #END GETCHATFROMWA
    
print(getChatFromWA('"My Number"'))
#%% BOT Testing
prevChat = {}

#target = '"My Number"'
def isExistInDB(cmd, filename):
    data = pd.read_csv(filename) 
    isFound =False
    procedure_name = None
    for idx in range(len(data['command'])):
        if (data['command'][idx] == cmd):
            isFound = True
            procedure_name = data['procedure_name'][idx]
            break
    return isFound, procedure_name
    
def doCommand(command):
    isFound, procedure = isExistInDB(command, 'command.csv')
    if (isFound == True):
        print('here')
        exec(procedure)
    else:
        sendTexttoWA("Unknown command for: "+ command, target)
        
def echo():
    print('echo')
def charting2g3g4g():
    print('charting')

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

target = '"Kak Yeyen"'
tl = Timeloop()
@tl.job(interval=timedelta(seconds=3))
def sample_job_every_10s():
    global prevChat
    recentChat = getChatFromWA(target)
    if (recentChat != None): # if message is a text (not an image, sticker, etc.)
        if (isNewChat(prevChat, recentChat, "Yoland Nababan") == True):
            print(recentChat['text'])
            prevChat = recentChat
            doCommand(recentChat['text'])
        else:
            print('IDLE')

def sendTexttoWA(messageText, target):
    #from selenium import webdriver
#    target = '"' + e3.get() + '"'
    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(messageText + '\n')   
    
if __name__ == "__main__":
    tl.start(block=True)



#Store chat
#def storeChat(filepath, filename):
##store chat if it is unique
#    threading.Timer(5.0, repeatfun).start()
    
#driver.close()
#sys.exit()