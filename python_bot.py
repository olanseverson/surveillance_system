# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:13:14 2019
Source :
    https://www.guru99.com/xpath-selenium.html
    http://ashishkhan.com/blog/buddy-whatsapp-chat-bot-with-python
    https://codepad.co/snippet/whatsapp-bot-using-selenium-with-python
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#multi-valued-attributes
    https://selenium-python.readthedocs.io/locating-elements.html
    https://realpython.com/intro-to-python-threading/#conclusion-threading-in-python
    https://docs.python.org/2/howto/logging.html#loggers
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

from queue import Queue

logging.basicConfig(level = logging.WARNING,)
#logging.root.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter("[%(levelname)s] => (%(name)s||%(threadName)-s):  %(message)s")
logger_handler = logging.StreamHandler() # handler
logger_handler.setFormatter(FORMATTER)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#%% Open WA
# Replace below path with the absolute path of the \#chromedriver in your computer
dirname, filename = os.path.split(os.path.abspath(__file__))
driver = webdriver.Chrome(dirname + '/chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 100)

#%% Click trarget
target = '"Bot Nokia"'
x_arg = '//span[contains(@title,' + target + ')]';
group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)));
#print ("Wait for few seconds")
group_title.click()

url = driver.page_source
soup = bs(url, "lxml")

#%% Get Chat From WA
def getChatFromWA(ChatRoom):
    loggerm = logging.getLogger(__name__ + 'getChat')
    loggerm.setLevel(logging.WARN)
    # ================= OPEN CHAT ROOM =====================
    x_arg = '//span[contains(@title,' + ChatRoom + ')]';
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)));
    group_title.click()    
    
    # =================== GET THE CHAT ======================
    url = driver.page_source
    soup = bs(url, "lxml")
    loggerm.debug("get the chat")
    chatdict = {}
    try:
        gotchat = soup.find_all(class_="FTBzM")[-1] # searching node for last chat
    except IndexError as err:
        return None
        loggerm.error("Error: ", err)
        loggerm.error('class name (maybe) rearranged')
    else:
        try:
            gottext = gotchat.find_all("span", class_="selectable-text invisible-space copyable-text")[-1]
            gotdate_hour = gotchat.find_all("div", class_="copyable-text")[0].attrs['data-pre-plain-text']
        except IndexError as error:
            loggerm.error("ERROR: ", error)
            loggerm.error("Last message is not a text")
            return None
        else:
            # ================= PARSING DATA CHAT ============
            hour = gotdate_hour.split(']')[0][1:].split(',')[0].strip()  #parsing gotdate_hour to get hour 
            date = gotdate_hour.split(']')[0][1:].split(',')[1].strip()  #parsing gotdate_hour to get date
            senderName = gotdate_hour.split(']')[1].strip()[:-1]         #parsing gotdate_hour to get sender name
            chatdict['hour'] = hour
            chatdict['date'] = date
            chatdict['text'] = gottext.string
            chatdict['sender'] = senderName            
            return chatdict
    #END GETCHATFROMWA

#print(getChatFromWA('"Bot Nokia"'))
#%% BOT Testing

#logging.basicConfig(level=logging.DEBUG,
#                    format='(%(threadName)-9s) %(message)s',)
#target = '"My Number"'
#target = '"Kak Yeyen"'
#target = '"Bang Rio"'
target = '"Bot Nokia"'
prevChat = {}
isMainBusy = False
isNeedReply = False
BUF_SIZE = 10
q = Queue(BUF_SIZE)
def sendTexttoWA(messageText, target):
    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@contenteditable="true"]')[-1]
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
    #logger
    logger.setLevel(logging.DEBUG)
    global isMainBusy
    global isNeedReply
    global q
    isFound, procedure_name, Reply= isExistInDB(command['text'].lower(), 'command.csv')
    if (isFound == True): # if command is a recognized command
        if (isMainBusy == True): # busy, doing another request
            if (isNeedReply == False):
                logger.info('busy')
                sendTexttoWA("Server busy, please wait another process to be finished!", target)
        else:
            isNeedReply = Reply
            isMainBusy  = True
            logger.debug('sender: ' + command['sender'])
            logger.debug('proced: ' + procedure_name)
            logger.debug('isNeed: ' + str(Reply))
            
            #start a new thread
            logger.info('start thread')
            cmdThread = threading.Thread(target = eval(procedure_name)
                                         , args = ( )
                                         , name = command['sender'])     
            cmdThread.setDaemon(True)
            cmdThread.start();
#            cmdThread.join();
            
    else:
        sendTexttoWA("BOT:Unknown command for: "+ command['text'], target)
        
def echo():
    logger.setLevel(logging.DEBUG)# logger
    global isMainBusy
    logger.debug("START ECHO")
    time.sleep(5)
    isMainBusy = False;
    logger.debug("isMainBusy :%d ", isMainBusy)
    logger.debug("TERMINATE ECHO")
#    print('why')

def charting():
    global isMainBusy
    global isNeedReply
    isCmdComplete = False
    logger.debug('START CHART')
    logger.debug('CHARTING')
    while isCmdComplete == False:
        if (q.empty() == True):
            pass
        message = q.get()
        logging.debug("Consumer storing message: %s (size=%d)"
                      , message, q.qsize())
        if (message == '2g' or message == '3g' or message == '4g'):
            logger.debug('message is : %s', message)
            isNeedReply = False;
            with q.mutex:
                q.queue.clear()
            isCmdComplete = True
        else:
            logger.debug('invalid respon')
        
    isMainBusy = False
    logger.debug("END CHARTING")
    return;

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
#            print('-')
#            
#if __name__ == "__main__":
#    schedule.every(1).seconds.do(checkNewMessage)
#    while True:
#        schedule.run_pending()
#        print(time.ctime())
#        time.sleep(60)
        
    
tl = Timeloop()
@tl.job(interval=timedelta(seconds=1))
def checkNewMessage():
    global prevChat
    global isMainBusy
    global isNeedReply
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    recentChat = getChatFromWA(target)
    if (recentChat != None): # if message is a text (not an image, sticker, etc.)
        if (isNewChat(prevChat, recentChat, "Yoland Nababan") == True):
            print(recentChat['text'])
            prevChat = recentChat
            if (isMainBusy == True and isNeedReply == True):
                logger.info('add command to queue')
                if not q.full():
                    q.put(recentChat['text'])
                logger.info('Putting ' + recentChat['text']
                        + ' : ' + str(q.qsize()) + ' items in queue')
            else:
                doCommand(recentChat)
            
    # DEBUGGING THREAD
    print("Total number of threads", threading.activeCount())
#    print("List of threads: ", threading.enumerate())
#    print("this thread: ", threading.current_thread)
if __name__ == "__main__":
    tl.start(block=True)
    
#driver.close()
#sys.exit()