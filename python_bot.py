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

import pandas as pd

# for periodic task 
import time
from timeloop import Timeloop
from datetime import timedelta

import schedule
import threading
import logging
#logger = logging.getLogger()
#logging.basicConfig(level=logging.DEBUG,
#                    format='(%(threadName)-9s) %(message)s',)
#%% Open WA
tl = Timeloop()

# Replace below path with the absolute path of the \#chromedriver in your computer
dirname, filename = os.path.split(os.path.abspath(__file__))
driver = webdriver.Chrome(dirname + '/chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 100)

#%% Click trarget
target = '"Kak Yeyen"'
x_arg = '//span[contains(@title,' + target + ')]';
group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)));
#print (group_title)
#print ("Wait for few seconds")
group_title.click()

url = driver.page_source
soup = bs(url, "lxml")

#%% Get Chat From WA
def getChatFromWA(ChatRoom):
    # ================= OPEN CHAT ROOM =====================
#    print("click chat room ")
#    logging.set(logging.WARNING)
#    print(logging.getLevelName(logging.WARNING))
    logging.disable(logging.DEBUG)
#    logger = logging.getLogger()
#    logger.propagate = True
#    logger.
#    logging.disable(sys.maxsize)
#    print(sys.maxsize)
    x_arg = '//span[contains(@title,' + ChatRoom + ')]';
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)));
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
#logging.basicConfig(level=logging.DEBUG,
#                    format='(%(threadName)-9s) %(message)s',)
#target = '"My Number"'
#target = '"Kak Yeyen"'
target = '"Bang Rio"'
isMainBusy = False
isNeedReply = False
def sendTexttoWA(messageText, target):
    #from selenium import webdriver
#    target = '"' + e3.get() + '"'
    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(messageText + '\n')
    
def isExistInDB(cmd, filename):
    isFound = False
    procedure_name = None
    isNeedReply = None
    data = pd.read_csv(filename) 
    for idx in range(len(data['command'])):
        if (data['command'][idx] == cmd):
            isFound = True
            procedure_name = data['procedure_name'][idx]
            isNeedReply = data['IsNeedReply'][idx]
            break
    return isFound, procedure_name, isNeedReply
    
def doCommand(command):
    global isMainBusy
    global isNeedReply
#    print('doCmd: ', isMainBusy)
    isFound, procedure_name, Reply= isExistInDB(command['text'].lower(), 'command.csv')
    if (isFound == True): # if command is a recognized command
#        print('found')
        if (isMainBusy == True): # busy, doing another request
            if (isNeedReply == True):
                print('add command to queue')
#                time.sleep(2);
            else:
                print('busy')
                sendTexttoWA("Server busy, please wait another process to be finished!", target)
        else:
            isNeedReply = Reply
            isMainBusy  = True
#            print('sender: ' + command['sender'])
#            print('proced: ' + procedure_name)
#            print('isNeed: ' + str(Reply))
            print('start thread')
            #start a new thread
            cmdThread = threading.Thread(target = function_mapping
                                         , args = (procedure_name, )
                                         , name = command['sender'])     
            cmdThread.start();
#            cmdThread.join();
#            print ('d.isAlive()', cmdThread.isAlive())
    else:
        sendTexttoWA("BOT:Unknown command for: "+ command['text'], target)
#        sendTexttoWA("BOT: "+ command['text'], target)
#        print(command['text'])
        
def function_mapping(function_name):
    logger = logging.getLogger()
    logger.propagate = True
    logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
    t = threading.currentThread()
    logging.info(t.getName())
    if(function_name == 'echo'):
        echo()
    elif (function_name == 'charting2g3g4g'):
        charting2g3g4g()

def echo():
    global isMainBusy
    print('====start echo()=======')
    print(time.ctime())
    time.sleep(10)
    print(time.ctime())
    isMainBusy = False;
    
    print("isMainBusy: ", isMainBusy)
    print('====END echo()=======')
    return 0

def charting2g3g4g():
    global isMainBusy
    print('====start charting()=======')
    print('CHARTING')
    time.sleep(8)
    isMainBusy = False
    print("isMainBusy: ", isMainBusy)
    print('====END chart()=======')
    return 0;

def isNewChat(prevChat, newChat,botname):
    if (newChat['sender'] != botname): # request is not from bot itself
        if not prevChat.get('date'):
            return True
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

#def checkNewMessage():
#    global prevChat
#    recentChat = getChatFromWA(target)
#    if (recentChat != None): # if message is a text (not an image, sticker, etc.)
#        if (isNewChat(prevChat, recentChat, "Yoland Nababan") == True):
#            print(recentChat['text'])
#            prevChat = recentChat
#            doCommand(recentChat)
#        else:
#            print(' ')
#            
#if __name__ == "__main__":
#    schedule.every(5).seconds.do(checkNewMessage)
#    while True:
#        schedule.run_pending()
#        time.sleep(1)
    
tl = Timeloop()
@tl.job(interval=timedelta(seconds=2))
def checkNewMessage():
    global prevChat
    recentChat = getChatFromWA(target)
    if (recentChat != None): # if message is a text (not an image, sticker, etc.)
        if (isNewChat(prevChat, recentChat, "Yoland Nababan") == True):
            print(recentChat['text'])
            prevChat = recentChat
            doCommand(recentChat)
#        else:
#            print('-')
    # debugging thread process
    print("Total number of threads", threading.activeCount())
#    print("List of threads: ", threading.enumerate())
#    print("this thread: ", threading.current_thread)
if __name__ == "__main__":
    tl.start(block=True)
    




    
#tl = Timeloop()
#@tl.job(interval=timedelta(seconds=3))
#def sample_job_every_3s():
#    global prevChat
#    recentChat = getChatFromWA(target)
#    if (recentChat != None): # if message is a text (not an image, sticker, etc.)
#        if (isNewChat(prevChat, recentChat, "Yoland Nababan") == True):
#            print(recentChat['text'])
#            prevChat = recentChat
#            doCommand(recentChat['text'])
#        else:
#            print('IDLE')
#driver.close()
#sys.exit()