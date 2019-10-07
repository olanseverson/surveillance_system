from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

import os
import datetime
import schedule
import threading,time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
#import ctypes
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import sys
import SQLdict
import pandas as pd

import psutil
import signal
import suportingsystem

import logging

traffPSdictnow = {}
traffCSdictpast = {}
traffPSdictpast = {}

#booleanmycom = bool(0)
#booleangp = bool(0)
#booleaniindash = bool(0)
#booleanperf = bool(0)

dirname, filename = os.path.split(os.path.abspath(__file__))

driver = webdriver.Chrome(dirname + '/chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 100)

# User input
def exit_data():
    from pprint import pprint as pp
    list = []
    print("Exiting")
    children = psutil.Process().children(recursive=True)
    list = pp([p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name']])
    #list = pp([p.info for p in psutil.process_iter(attrs=['pid', 'name']) if 'python' in p.info['name']])
    #print(list)
    for child in children:
        print('>>> Killing pid {}'.format(child.pid))
        #os.kill(child.pid, signal.SIGTERM)
        #child.send_signal(SIGTERM)
    # sys.exit()
    #os.kill(os.getpid(), signal.SIGTERM)
def sitefiletoWA(address):
    if os.path.exists(address):
        target = '"' + e3.get() + '"'
        x_arg = '//span[contains(@title,' + target + ')]'
        group_title = wait.until(EC.presence_of_element_located((
        By.XPATH, x_arg)))
        group_title.click()
        time.sleep(5)
        fileToSend = address
        driver.find_element_by_css_selector('span[data-icon="clip"]').click()
    # add file to send by file path
        attach=driver.find_element_by_css_selector('input[type="file"]')
        attach.send_keys(fileToSend)
        time.sleep(5)
        #sendbutton = driver.find_element_by_class_name('yavlE')
        #sendbutton.click()
        send=driver.find_element_by_xpath("//div[contains(@class, 'iA40b')]")
        send.click()

def sendTexttoWA(messageText):
    #from selenium import webdriver
    target = '"' + e3.get() + '"'
    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(messageText + '\n')


def sendtoWA(textadd,header,footer):
    #print("sent to WA")
    #currentDate = datetime.datetime.today()- datetime.timedelta(hours =24)
    #yesterday = datetime.date.today() - datetime.timedelta(hours =192)
    senttoWAAstring = open(textadd, 'r')
    datastring = senttoWAAstring.read()
    senttoWAAstring.close()
    target = '"' + e3.get() + '"'

    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located((
    By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(header + '\n')
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(datastring + '\n')
    message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]
    message.send_keys(footer + '\n')

def iin_dashboards():
    window.wm_title("Runing iin_dashboards ")
    sendTexttoWA("Iin_dashboard is in progress . . . ")
    fieldnames = []
    if not os.path.exists(dirname + "/output"):
        os.makedirs(dirname + "/output")

    sqlscript_query = SQLdict.getSQLScript("Dash_Get_Data")
    suportingsystem.query_command(sqlscript_query,"nofeedback","isat_report",ipheidi,userheidi,passwodjeidi)

    if os.path.exists(dirname +'/output/2G_daily_dashboard.csv'):
        os.remove(dirname +'/output/2G_daily_dashboard.csv')
        outputfile = open(dirname +'/output/2G_daily_dashboard.csv', 'x')
    else:
        outputfile = open(dirname +'/output/2G_daily_dashboard.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("2Gdashboard_daily")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_3Gfiledname = pd.DataFrame(fieldnames)
    df2 = df_3Gfiledname.T
    df2.to_csv(outputfile, header=None, index=None, mode='a')
    #df = pd.DataFrame(queryresult)
    #df.to_csv(outputfile, header=None, index=None, mode='a')
    #outputfile.close()
    #sitefiletoWA(dirname +'/output/2G_daily_dashboard.csv')

    df = pd.DataFrame(queryresult)
    df.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/2G_daily_dashboard.csv')

#==========================================================
    if os.path.exists(dirname +'/output/3G_daily_dashboard.csv'):
        os.remove(dirname +'/output/3G_daily_dashboard.csv')
        outputfile = open(dirname +'/output/3G_daily_dashboard.csv', 'x')
    else:
        outputfile = open(dirname +'/output/3G_daily_dashboard.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("3Gdashboard_daily")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_3Gfiledname = pd.DataFrame(fieldnames)
    df2 = df_3Gfiledname.T
    df2.to_csv(outputfile, header=None, index=None, mode='a')
    df = pd.DataFrame(queryresult)
    df.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()

    sitefiletoWA(dirname +'/output/3G_daily_dashboard.csv')

#==========================================================

    if os.path.exists(dirname +'/output/4G_daily_dashboard.csv'):
        os.remove(dirname +'/output/4G_daily_dashboard.csv')
        outputfile = open(dirname +'/output/4G_daily_dashboard.csv', 'x')
    else:
        outputfile = open(dirname +'/output/4G_daily_dashboard.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("4Gdashboard_daily")
    queryresult,fieldnames =suportingsystem. query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_3Gfiledname = pd.DataFrame(fieldnames)
    df2 = df_3Gfiledname.T
    df2.to_csv(outputfile, header=None, index=None, mode='a')
    df = pd.DataFrame(queryresult)
    df.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    if os.path.exists(dirname +'/output/4G_daily_dashboard.csv'):
        sitefiletoWA(dirname +'/output/4G_daily_dashboard.csv')

#==========================================================
#==============================================================
    if os.path.exists(dirname +'/output/2G_bh_dashboard.csv'):
        os.remove(dirname +'/output/2G_bh_dashboard.csv')
        outputfile = open(dirname +'/output/2G_bh_dashboard.csv', 'x')
    else:
        outputfile = open(dirname +'/output/2G_bh_dashboard.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("2Gdashboard_bh")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_3Gfiledname = pd.DataFrame(fieldnames)
    df2 = df_3Gfiledname.T
    df2.to_csv(outputfile, header=None, index=None, mode='a')
    df = pd.DataFrame(queryresult)
    df.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    if os.path.exists(dirname +'/output/2G_bh_dashboard.csv'):
        sitefiletoWA(dirname +'/output/2G_bh_dashboard.csv')

#==========================================================
    if os.path.exists(dirname +'/output/3G_bh_dashboard.csv'):
        os.remove(dirname +'/output/3G_bh_dashboard.csv')
        outputfile = open(dirname +'/output/3G_bh_dashboard.csv', 'x')
    else:
        outputfile = open(dirname +'/output/3G_bh_dashboard.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("3Gdashboard_bh")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_3Gfiledname = pd.DataFrame(fieldnames)
    df2 = df_3Gfiledname.T
    df2.to_csv(outputfile, header=None, index=None, mode='a')
    df = pd.DataFrame(queryresult)
    df.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    if os.path.exists(dirname +'/output/3G_bh_dashboard.csv'):
        sitefiletoWA(dirname +'/output/3G_bh_dashboard.csv')

#==========================================================

    if os.path.exists(dirname +'/output/4G_bh_dashboard.csv'):
        os.remove(dirname +'/output/4G_bh_dashboard.csv')
        outputfile = open(dirname +'/output/4G_bh_dashboard.csv', 'x')
    else:
        outputfile = open(dirname +'/output/4G_bh_dashboard.csv', 'x')

    sqlscript_query = SQLdict.getSQLScript("4Gdashboard_bh")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_3Gfiledname = pd.DataFrame(fieldnames)
    df2 = df_3Gfiledname.T
    df2.to_csv(outputfile, header=None, index=None, mode='a')

    df = pd.DataFrame(queryresult)
    df.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    if os.path.exists(dirname +'/output/4G_bh_dashboard.csv'):
        sitefiletoWA(dirname +'/output/4G_bh_dashboard.csv')

#==========================================================
    sendTexttoWA("Iin  dashboard is ready")
    window.wm_title("iin_dashboards is done")

def getzerotraffic():
    window.wm_title("Runing zero traffic check.. ")
    currentDate = datetime.datetime.today()- datetime.timedelta(hours =24)
    sendTexttoWA("zero traffic check is in progress . . . ")
    #booleangp = bool(1)
    #schedule.every(120).seconds.do(exit_data)
    fieldnames = []
    if not os.path.exists(dirname + "/output"):
        os.makedirs(dirname + "/output")
    #============================================================================
    if os.path.exists(dirname +'/output/2GZero.csv'):
        os.remove(dirname +'/output/2GZero.csv')
        outputfile = open(dirname +'/output/2GZero.csv', 'x')
    else:
        outputfile = open(dirname +'/output/2GZero.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("2GZero")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2Gfiledname = pd.DataFrame(fieldnames)
    df2Gzeroheader = df_2Gfiledname.T
    df2Gzeroheader.to_csv(outputfile, header=None, index=None, mode='a')
    df_2Gtraf = pd.DataFrame(queryresult)
    df_2Gtraf.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/2GZero.csv')
    #============================================================================
    #============================================================================
    if os.path.exists(dirname +'/output/3GZero.csv'):
        os.remove(dirname +'/output/3GZero.csv')
        outputfile = open(dirname +'/output/3GZero.csv', 'x')
    else:
        outputfile = open(dirname +'/output/3GZero.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("3GZero")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2Gfiledname = pd.DataFrame(fieldnames)
    df2Gzeroheader = df_2Gfiledname.T
    df2Gzeroheader.to_csv(outputfile, header=None, index=None, mode='a')
    df_2Gtraf = pd.DataFrame(queryresult)
    df_2Gtraf.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/3GZero.csv')
    #============================================================================
    #============================================================================
    if os.path.exists(dirname +'/output/4GZero.csv'):
        os.remove(dirname +'/output/4GZero.csv')
        outputfile = open(dirname +'/output/4GZero.csv', 'x')
    else:
        outputfile = open(dirname +'/output/4GZero.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("4GZero")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2Gfiledname = pd.DataFrame(fieldnames)
    df2Gzeroheader = df_2Gfiledname.T
    df2Gzeroheader.to_csv(outputfile, header=None, index=None, mode='a')
    df_2Gtraf = pd.DataFrame(queryresult)
    df_2Gtraf.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/4GZero.csv')
    #============================================================================
    sendTexttoWA("zero traffic check completed")

def GPcheck():
    window.wm_title("Runing GP alignment check.. ")
    currentDate = datetime.datetime.today()- datetime.timedelta(hours =24)
    sendTexttoWA("GP alignment check is in progress . . . ")
    #booleangp = bool(1)
    #schedule.every(120).seconds.do(exit_data)
    fieldnames = []
    if not os.path.exists(dirname + "/output"):
        os.makedirs(dirname + "/output")
    #============================================================================
    if os.path.exists(dirname +'/output/2G_GPCheck.csv'):
        os.remove(dirname +'/output/2G_GPCheck.csv')
        outputfile = open(dirname +'/output/2G_GPCheck.csv', 'x')
    else:
        outputfile = open(dirname +'/output/2G_GPCheck.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("2G_GPCheck")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2Gfiledname = pd.DataFrame(fieldnames)
    df2 = df_2Gfiledname.T
    df2.to_csv(outputfile, header=None, index=None, mode='a')
    df_2G = pd.DataFrame(queryresult)
    df_2G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/2G_GPCheck.csv')
    #============================================================================
    if os.path.exists(dirname +'/output/3G_GPCheck.csv'):
        os.remove(dirname +'/output/3G_GPCheck.csv')
        outputfile = open(dirname +'/output/3G_GPCheck.csv', 'x')
    else:
        outputfile = open(dirname +'/output/3G_GPCheck.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("3G_GPCheck")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_3Gfiledname = pd.DataFrame(fieldnames)
    df3 = df_3Gfiledname.T
    df3.to_csv(outputfile, header=None, index=None, mode='a')
    df_3G = pd.DataFrame(queryresult)
    df_3G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/3G_GPCheck.csv')
    #============================================================================
    if os.path.exists(dirname +'/output/4G_GPCheck.csv'):
        os.remove(dirname +'/output/4G_GPCheck.csv')
        outputfile = open(dirname +'/output/4G_GPCheck.csv', 'x')
    else:
        outputfile = open(dirname +'/output/4G_GPCheck.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("4G_GPCheck")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_4Gfiledname = pd.DataFrame(fieldnames)
    df4 = df_4Gfiledname.T
    df4.to_csv(outputfile, header=None, index=None, mode='a')
    df_4G = pd.DataFrame(queryresult)
    df_4G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/4G_GPCheck.csv')
    #============================================================================
    sendTexttoWA("site that requires GP alignment has been provided... ")
    window.wm_title("GP alignment check completed ")

def select_sql():
    waitingsecond = 900 #15 menit
    sendTexttoWA("Thread_performance is running")
    window.wm_title("Thread_performance is running ")
    #schedule.every(1).seconds.do(exit_data)
    currentDate = datetime.datetime.today()- datetime.timedelta(hours =24)
    yesterday = datetime.date.today() - datetime.timedelta(hours =192)
    sqlscript_query = SQLdict.getSQLScript("2G")
    #print(sqlscript_query)
    queryresult,field_names = suportingsystem.query_command(sqlscript_query,"feedback","isat_cm",ipheidi,userheidi,passwodjeidi)
    #print(len(queryresult) )

    if len(queryresult) >7:
        restultadd = suportingsystem.queryPostProcessing1(queryresult,field_names,currentDate.strftime("%Y-%m-%d"),"2G")
        header = "*2G statistic " + currentDate.strftime("%Y-%m-%d") + "* _(Compare with " + yesterday.strftime("%Y-%m-%d") + ")_\n"
        sendTexttoWA(header)
        sitefiletoWA(dirname +'/output/comparasion_output2G.txt')
    else:
        sendTexttoWA("2G statistic is  not complete"+ "\n")    #print("2G proses")

    #sendTexttoWA("2G statistic is completed"+ "\n")
        #sendtoWA(restultadd,header,footer)
        #print("2G done")

    sqlscript_query = SQLdict.getSQLScript("3G")
    queryresult,field_names = suportingsystem.query_command(sqlscript_query,"feedback","isat_cm",ipheidi,userheidi,passwodjeidi)

    if len(queryresult) >7:
        restultadd = suportingsystem.queryPostProcessing1(queryresult,field_names,currentDate.strftime("%Y-%m-%d"),"3G")
        header = "*3G statistic " + currentDate.strftime("%Y-%m-%d") + "* _(Compare with " + yesterday.strftime("%Y-%m-%d") + ")_\n"
        sendTexttoWA(header)
        sitefiletoWA(dirname +'/output/comparasion_output3G.txt')

    else:
        sendTexttoWA("3G statistic is  not complete"+ "\n")    #print("2G proses")

        #sendtoWA(restultadd,header,footer)
        #print("3G done")


    sqlscript_query = SQLdict.getSQLScript("4G")
    queryresult,field_names = suportingsystem.query_command(sqlscript_query,"feedback","isat_cm",ipheidi,userheidi,passwodjeidi)

    if len(queryresult) >7:
        restultadd = suportingsystem.queryPostProcessing1(queryresult,field_names,currentDate.strftime("%Y-%m-%d"),"4G")
        header = "*4G statistic " + currentDate.strftime("%Y-%m-%d") + "* _(Compare with " + yesterday.strftime("%Y-%m-%d") + ")_\n"
        sendTexttoWA(header)
        sitefiletoWA(dirname +'/output/comparasion_output4G.txt')

    else:
        sendTexttoWA("3G statistic is  not complete"+ "\n")    #print("2G proses")
        #print("4g")
        #footer = "_comparation result is in braket, (-) mean degraded (+) means improving_\n"
        #sendtoWA(restultadd,header,footer)
        #print("4G done")
        #window.wm_title("Running success at : " + str((datetime.datetime.now()).strftime("%H:%M")) + ", next thread has been scheduled" )
    window.wm_title("Thread_performance completed")
    sendTexttoWA("performance thread is complete"+ "\n")

def mycomstat():
    window.wm_title("mycom statistic is running.. ")
    currentDate = datetime.datetime.today()- datetime.timedelta(hours =24)
    sendTexttoWA("mycom statistic is running . . . ")
    #booleanmycom = bool(1)

    #schedule.every(120).seconds.do(exit_data)
    fieldnames = []
    if not os.path.exists(dirname + "/output"):
        os.makedirs(dirname + "/output")
    #============================================================================
    if os.path.exists(dirname +'/output/2G_mycom.csv'):
        os.remove(dirname +'/output/2G_mycom.csv')
        outputfile = open(dirname +'/output/2G_mycom.csv', 'x')
    else:
        outputfile = open(dirname +'/output/2G_mycom.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("2G_mycom")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2Gfiledname = pd.DataFrame(fieldnames)
    df2 = df_2Gfiledname.T
    df2.to_csv(outputfile, header=None, index=None, mode='a')
    df_2G = pd.DataFrame(queryresult)
    df_2G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/2G_mycom.csv')
    #=================================

    #============================================================================

    if os.path.exists(dirname +'/output/3G_mycom.csv'):
        os.remove(dirname +'/output/3G_mycom.csv')
        outputfile = open(dirname +'/output/3G_mycom.csv', 'x')
    else:
        outputfile = open(dirname +'/output/3G_mycom.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("3G_mycom")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_3Gfiledname = pd.DataFrame(fieldnames)
    df3 = df_3Gfiledname.T
    df3.to_csv(outputfile, header=None, index=None, mode='a')
    df_3G = pd.DataFrame(queryresult)
    df_3G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/3G_mycom.csv')
    #=================================

    #============================================================================

    if os.path.exists(dirname +'/output/4G_mycom.csv'):
        os.remove(dirname +'/output/4G_mycom.csv')
        outputfile = open(dirname +'/output/4G_mycom.csv', 'x')
    else:
        outputfile = open(dirname +'/output/4G_mycom.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("4G_mycom")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_4Gfiledname = pd.DataFrame(fieldnames)
    df4 = df_4Gfiledname.T
    df4.to_csv(outputfile, header=None, index=None, mode='a')
    df_4G = pd.DataFrame(queryresult)
    df_4G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/4G_mycom.csv')
    #=================================

    window.wm_title("mycom statistic completed.. ")
    sendTexttoWA("mycom statistic completed. . . ")

def updatetabletraffic4G():
    window.wm_title("updating temp table")
    sqlscript_query = SQLdict.getSQLScript("chart4G_inserttabel")
    suportingsystem.query_command(sqlscript_query,"nofeedback","isat_report",ipheidi,userheidi,passwodjeidi)
    sqlscript_query = SQLdict.getSQLScript("chart3G_inserttabel")
    suportingsystem.query_command(sqlscript_query,"nofeedback","isat_report",ipheidi,userheidi,passwodjeidi)
    sqlscript_query = SQLdict.getSQLScript("chart2G_inserttabel")
    suportingsystem.query_command(sqlscript_query,"nofeedback","isat_report",ipheidi,userheidi,passwodjeidi)
    sqlscript_query = SQLdict.getSQLScript("prl3G")
    suportingsystem.query_command(sqlscript_query,"nofeedback","isat_report",ipheidi,userheidi,passwodjeidi)
    sqlscript_query = SQLdict.getSQLScript("prl4G")
    suportingsystem.query_command(sqlscript_query,"nofeedback","isat_report",ipheidi,userheidi,passwodjeidi)
    window.wm_title("temp table updated")

def updatetabletraffic4G_dummy():
    window.wm_title("updating temp table dummy")
    sqlscript_query = SQLdict.getSQLScript("chart4G_inserttabel")
    suportingsystem.query_command(sqlscript_query,"nofeedback","isat_report",ipheidi,userheidi,passwodjeidi)
    window.wm_title("temp table updated_dummy")

def searchSuffix():
    print('2g')
    searching ('2G')
    print('3g')
    searching ('3G')
    print('4g')
    searching ('4G')

def create_temp_tbl_yesterday():
    # create table yesterday
    print('create table 2G yesterday')
    sqlscript_query = SQLdict.getSQLScript("2G_yesterday_create_table")
    suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")    
    
    print('create table 3G yesterday')
    sqlscript_query = SQLdict.getSQLScript("3G_yesterday_create_table")
    suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
    
    print('create table 4G yesterday')
    sqlscript_query = SQLdict.getSQLScript("4G_yesterday_create_table")
    suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
        
def searching(gen):
    sendTexttoWA('============================')
    if gen == '2G':
        # create table today
        print('create table today')
        sqlscript_query = SQLdict.getSQLScript("2G_today_create_table")
        suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")

#        # create table yesterday
#        print('create table yesterday')
#        sqlscript_query = SQLdict.getSQLScript("2G_yesterday_create_table")
#        suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")

        # get missing sites from DB
        print('get missing file')
        sqlscript_query = SQLdict.getSQLScript("get_missing_2G")
        queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
        dfmissed = pd.DataFrame(queryresult,columns=fieldnames)
    #    print (dfmissed)
    #    print (dfmissed.columns)

        # save file
        print ("Save missing sites")
        if os.path.exists(dirname +'/output/2G_missing.csv'):
            os.remove(dirname +'/output/2G_missing.csv')
            outputfile = open(dirname +'/output/2G_missing.csv', 'x')
        else:
            outputfile = open(dirname +'/output/2G_missing.csv', 'x')
        #file_path = r'C:\Users\Olan\Desktop\python\output\2G_missing.csv'
        dfmissed.to_csv(outputfile, index = None, header=True)

        #sending file to WA
        sitefiletoWA(dirname +'/output/2G_missing.csv')
        
        # sending statistics to WA
        unique = {}
        unique = dfmissed['BSC'] + dfmissed['BCF'] + dfmissed ['BTS']
#        print (unique)
        sendTexttoWA("MISSING : " + str(len(unique.drop_duplicates().index)) + " Object" )

        # get union from DB
        print('get union file')
        sqlscript_query = SQLdict.getSQLScript("get_union_2G")
        queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
        df_union = pd.DataFrame(queryresult,columns=fieldnames)
        #print (df_union)
        #print (df_union.columns)

        if len(df_union.index) == 0:
            print("Union file empty")
            sendTexttoWA("Union file empty")
        else:
            # save file
            print ("Save union sites")
            if os.path.exists(dirname +'/output/2G_union.csv'):
                os.remove(dirname +'/output/2G_union.csv')
                outputfile = open(dirname +'/output/2G_union.csv', 'x')
            else:
                outputfile = open(dirname +'/output/2G_union.csv', 'x')
            #file_path = r'C:\Users\Olan\Desktop\python\output\2G_union.csv'
            df_union.to_csv(outputfile, index = None, header=True)

            #sending file to WA
            sitefiletoWA(dirname +'/output/2G_union.csv')

            # sending statistics to WA
            statistics = df_union.groupby(['Remark']).size() # Series data type
            for idx in range(len(statistics)):
                temp_str = str(statistics.index[idx]) + ': ' + str(statistics[idx])
                sendTexttoWA(temp_str)
    elif gen == '3G':
        # create table today
        print('create table today')
        sqlscript_query = SQLdict.getSQLScript("3G_today_create_table")
        suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")

#        # create table yesterday
#        print('create table yesterday')
#        sqlscript_query = SQLdict.getSQLScript("3G_yesterday_create_table")
#        suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")

        # get missing sites from DB
        print('get missing file')
        sqlscript_query = SQLdict.getSQLScript("get_missing_3G")
        queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
        dfmissed = pd.DataFrame(queryresult,columns=fieldnames)
#        print (dfmissed)
        # print (dfmissed.columns)

        # save file
        print ("Save missing sites")
#        if os.path.exists(dirname +'/output/3G_missing.csv'):
#            os.remove(dirname +'/output/3G_missing.csv')
#            outputfile = open(dirname +'/output/3G_missing.csv', 'x')
#        else:
#            outputfile = open(dirname +'/output/3G_missing.csv', 'x')
        outputfile = dirname +'/output/3G_missing.csv'
        dfmissed.to_csv(outputfile, index = None, header=True)

        #sending file to WA
        sitefiletoWA(dirname +'/output/3G_missing.csv')

        # sending statistics to WA
        sendTexttoWA("MISSING: " + str(len(dfmissed.index)) )

        # get union from DB
        print('get union file')
        sqlscript_query = SQLdict.getSQLScript("get_union_3G")
        queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
        df_union = pd.DataFrame(queryresult,columns=fieldnames)
        #print (df_union)
        #print (df_union.columns)

        if len(df_union.index) == 0:
            #print("Union file empty")
            sendTexttoWA("Union file empty")
        else:
            # save file
            print ("Save union sites")
            if os.path.exists(dirname +'/output/3G_union.csv'):
                os.remove(dirname +'/output/3G_union.csv')
                outputfile = open(dirname +'/output/3G_union.csv', 'x')
            else:
                outputfile = open(dirname +'/output/3G_union.csv', 'x')
            #file_path = r'C:\Users\Olan\Desktop\python\output\3G_union.csv'
            df_union.to_csv(outputfile, index = None, header=True)

            #sending file to WA
            sitefiletoWA(dirname +'/output/3G_union.csv')

            # sending statistics to WA
            statistics = df_union.groupby(['Remark']).size() # Series data type
            for idx in range(len(statistics)):
                temp_str = str(statistics.index[idx]) + ': ' + str(statistics[idx])
                sendTexttoWA(temp_str)
    elif gen == '4G':
        # create table today
        print('create table today')
        sqlscript_query = SQLdict.getSQLScript("4G_today_create_table")
        suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")

#        # create table yesterday
#        print('create table yesterday')
#        sqlscript_query = SQLdict.getSQLScript("4G_yesterday_create_table")
#        suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")

        # get missing sites from DB
        print('get missing file')
        sqlscript_query = SQLdict.getSQLScript("get_missing_4G")
        queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
        dfmissed = pd.DataFrame(queryresult,columns=fieldnames)
    #    print (dfmissed)
    #    print (dfmissed.columns)

        # save file
        print ("Save missing sites")
        if os.path.exists(dirname +'/output/4G_missing.csv'):
            os.remove(dirname +'/output/4G_missing.csv')
            outputfile = open(dirname +'/output/4G_missing.csv', 'x')
        else:
            outputfile = open(dirname +'/output/4G_missing.csv', 'x')
        #file_path = r'C:\Users\Olan\Desktop\python\output\4G_missing.csv'
        dfmissed.to_csv(outputfile, index = None, header=True)

        #sending file to WA
        sitefiletoWA(dirname +'/output/4G_missing.csv')

        # sending statistics to WA
        sendTexttoWA("MISSING: " + str(len(dfmissed.index)) )

        # get union from DB
        print('get union file')
        sqlscript_query = SQLdict.getSQLScript("get_union_4G")
        queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
        df_union = pd.DataFrame(queryresult,columns=fieldnames)
        #print (df_union)
#        print (df_union.columns)

        if len(df_union.index) == 0:
            print("Union file empty")
            sendTexttoWA("Union file empty")
        else:
            # save file
            print ("Save union sites")
#            if os.path.exists(dirname +'/output/4G_union.csv'):
#                os.remove(dirname +'/output/4G_union.csv')
#                outputfile = open(dirname +'/output/4G_union.csv', 'x')
#            else:
#                outputfile = open(dirname +'/output/4G_union.csv', 'x')

            outpufile = dirname +'/output/4G_union.csv'
            df_union.to_csv(outputfile, index = None, header=True)

            #sending file to WA
            sitefiletoWA(dirname +'/output/4G_union.csv')

            # sending statistics to WA
            statistics = df_union.groupby(['remark']).size() # Series data type
            for idx in range(len(statistics)):
                temp_str = str(statistics.index[idx]) + ': ' + str(statistics[idx])
                sendTexttoWA(temp_str)

def charting4G3G2G():

    if os.path.exists(dirname +'/output/4Gchart.png'):
        os.remove(dirname +'/output/4Gchart.png')
    #if os.path.exists(dirname +'/output/4Gchart_thp.png'):
    #    os.remove(dirname +'/output/4Gchart_thp.png')
    sqlscript_query = SQLdict.getSQLScript("chart4G")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
    df = pd.DataFrame(queryresult,columns=fieldnames)
    df["xdate"] = pd.to_datetime(df["xdate"],format="%Y-%m-%d")
    df["xHour"] = pd.to_timedelta(df['xHour'], unit='H')#.astype(str), format='%H')

    df['Date_hour'] =df['xdate'] + df['xHour']
    dfCJRO = df[df['REGION'].str.contains("CJRO")]
    dfEJRO = df[df['REGION'].str.contains("EJRO")]
    dfKRO= df[df['REGION'].str.contains("KRO")]
    dfNSRO= df[df['REGION'].str.contains("NSRO")]
    dfSSRO= df[df['REGION'].str.contains("SSRO")]

    plt.plot( 'Date_hour', 'Total_Payload', data=dfCJRO, label = "CJRO")
    plt.plot( 'Date_hour', 'Total_Payload', data=dfEJRO, label = "EJRO")
    plt.plot( 'Date_hour', 'Total_Payload', data=dfKRO, label = "KRO")
    plt.plot( 'Date_hour', 'Total_Payload', data=dfNSRO, label = "NSRO")
    plt.plot( 'Date_hour', 'Total_Payload', data=dfSSRO, label = "SSRO")
    plt.suptitle("4G Total_Payload")
    plt.legend()

    plt.savefig(dirname +'/output/4Gchart.png')
    sitefiletoWA(dirname +'/output/4Gchart.png')
    plt.clf()
    plt.cla()
    plt.close()
    #===================================================================================
    if os.path.exists(dirname +'/output/4Gchart_band.png'):
        os.remove(dirname +'/output/4Gchart_band.png')
    #if os.path.exists(dirname +'/output/4Gchart_thp.png'):
    #    os.remove(dirname +'/output/4Gchart_thp.png')
    sqlscript_query = SQLdict.getSQLScript("chart4G_band")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
    df = pd.DataFrame(queryresult,columns=fieldnames)
    df["xdate"] = pd.to_datetime(df["xdate"],format="%Y-%m-%d")
    df["xHour"] = pd.to_timedelta(df['xHour'], unit='H')#.astype(str), format='%H')

    df['Date_hour'] =df['xdate'] + df['xHour']
    df1800 = df[df['BAND'].str.contains('1800')]
    df2100 = df[df['BAND'].str.contains('2100')]
    df900= df[df['BAND'].str.contains('900')]


    plt.plot( 'Date_hour', 'Total_Payload', data=df1800, label = "1800")
    plt.plot( 'Date_hour', 'Total_Payload', data=df2100, label = "2100")
    plt.plot( 'Date_hour', 'Total_Payload', data=df900, label = "900")

    plt.suptitle("4G Total_Payload")
    plt.legend()

    plt.savefig(dirname +'/output/4Gchart_band.png')
    sitefiletoWA(dirname +'/output/4Gchart_band.png')
    plt.clf()
    plt.cla()
    plt.close()

    #plt.plot( 'Date_hour', 'LTE_IP_User_Throughput_DL', data=dfCJRO, label = "CJRO")
    #plt.plot( 'Date_hour', 'LTE_IP_User_Throughput_DL', data=dfEJRO, label = "EJRO")
    #plt.plot( 'Date_hour', 'LTE_IP_User_Throughput_DL', data=dfKRO, label = "KRO")
    #plt.plot( 'Date_hour', 'LTE_IP_User_Throughput_DL', data=dfNSRO, label = "NSRO")
    #plt.plot( 'Date_hour', 'LTE_IP_User_Throughput_DL', data=dfSSRO, label = "SSRO")
    #plt.suptitle("4G LTE_IP_User_Throughput_DL")
    #plt.legend()

    #plt.savefig(dirname +'/output/4Gchart_thp.png')
    #sitefiletoWA(dirname +'/output/4Gchart_thp.png')

    #sendTexttoWA("charting4G completed ")
    #plt.clf()
    #plt.cla()
    #plt.close()
#=================================================================
    if os.path.exists(dirname +'/output/3Gchart.png'):
        os.remove(dirname +'/output/3Gchart.png')
    if os.path.exists(dirname +'/output/3Gchart_CS.png'):
        os.remove(dirname +'/output/3Gchart_CS.png')
    sqlscript_query = SQLdict.getSQLScript("chart3G")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
    df = pd.DataFrame(queryresult,columns=fieldnames)
    df["xdate"] = pd.to_datetime(df["xdate"],format="%Y-%m-%d")
    df["xHour"] = pd.to_timedelta(df['xHour'], unit='H')#.astype(str), format='%H')

    df['Date_hour'] =df['xdate'] + df['xHour']
    dfCJRO = df[df['REGION'].str.contains("CJRO")]
    dfEJRO = df[df['REGION'].str.contains("EJRO")]
    dfKRO= df[df['REGION'].str.contains("KRO")]
    dfNSRO= df[df['REGION'].str.contains("NSRO")]
    dfSSRO= df[df['REGION'].str.contains("SSRO")]

    plt.plot( 'Date_hour', 'Traffic_PS_Mbit', data=dfCJRO, label = "CJRO")
    plt.plot( 'Date_hour', 'Traffic_PS_Mbit', data=dfEJRO, label = "EJRO")
    plt.plot( 'Date_hour', 'Traffic_PS_Mbit', data=dfKRO, label = "KRO")
    plt.plot( 'Date_hour', 'Traffic_PS_Mbit', data=dfNSRO, label = "NSRO")
    plt.plot( 'Date_hour', 'Traffic_PS_Mbit', data=dfSSRO, label = "SSRO")
    plt.suptitle("3G Traffic_PS_Mbit")
    plt.legend()

    plt.savefig(dirname +'/output/3Gchart.png')
    sitefiletoWA(dirname +'/output/3Gchart.png')
    plt.clf()
    plt.cla()
    plt.close()

    plt.plot( 'Date_hour', 'Traffic_CS', data=dfCJRO, label = "CJRO")
    plt.plot( 'Date_hour', 'Traffic_CS', data=dfEJRO, label = "EJRO")
    plt.plot( 'Date_hour', 'Traffic_CS', data=dfKRO, label = "KRO")
    plt.plot( 'Date_hour', 'Traffic_CS', data=dfNSRO, label = "NSRO")
    plt.plot( 'Date_hour', 'Traffic_CS', data=dfSSRO, label = "SSRO")
    plt.suptitle("3G Traffic_CS")
    plt.legend()

    plt.savefig(dirname +'/output/3Gchart_CS.png')
    sitefiletoWA(dirname +'/output/3Gchart_CS.png')

    #sendTexttoWA("charting3G completed ")
    plt.clf()
    plt.cla()
    plt.close()
#==================================================================
    if os.path.exists(dirname +'/output/2Gchart.png'):
        os.remove(dirname +'/output/2Gchart.png')
    sqlscript_query = SQLdict.getSQLScript("chart2G")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
    df = pd.DataFrame(queryresult,columns=fieldnames)
    df["xdate"] = pd.to_datetime(df["xdate"],format="%Y-%m-%d")
    df["xHour"] = pd.to_timedelta(df['xHour'], unit='H')#.astype(str), format='%H')

    df['Date_hour'] =df['xdate'] + df['xHour']
    dfCJRO = df[df['region'].str.contains("CJRO")]
    dfEJRO = df[df['region'].str.contains("EJRO")]
    dfKRO= df[df['region'].str.contains("KRO")]
    dfNSRO= df[df['region'].str.contains("NSRO")]
    dfSSRO= df[df['region'].str.contains("SSRO")]

    plt.plot( 'Date_hour', 'TCH_Traffic_trf_24c', data=dfCJRO, label = "CJRO")
    plt.plot( 'Date_hour', 'TCH_Traffic_trf_24c', data=dfEJRO, label = "EJRO")
    plt.plot( 'Date_hour', 'TCH_Traffic_trf_24c', data=dfKRO, label = "KRO")
    plt.plot( 'Date_hour', 'TCH_Traffic_trf_24c', data=dfNSRO, label = "NSRO")
    plt.plot( 'Date_hour', 'TCH_Traffic_trf_24c', data=dfSSRO, label = "SSRO")
    plt.suptitle("2G TCH_Traffic")
    plt.legend()

    plt.savefig(dirname +'/output/2Gchart.png')
    sitefiletoWA(dirname +'/output/2Gchart.png')
    #sendTexttoWA("charting2G completed ")
    plt.clf()
    plt.cla()
    plt.close()
#==================================================================
    if os.path.exists(dirname +'/output/3Gprl.png'):
        os.remove(dirname +'/output/3Gprl.png')
    sqlscript_query = SQLdict.getSQLScript("prl3Gchart")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
    df = pd.DataFrame(queryresult,columns=fieldnames)
    df["xdate"] = pd.to_datetime(df["xdate"],format="%Y-%m-%d")
    df['xHour'] = pd.to_timedelta(df['xHour'], unit='H')
    df['Date_hour'] =df['xdate'] + df['xHour']

    dfCJRO = df[df['region'].str.contains("CJRO")]
    dfEJRO = df[df['region'].str.contains("EJRO")]
    dfKRO= df[df['region'].str.contains("KRO")]
    dfNSRO= df[df['region'].str.contains("NSRO")]
    dfSSRO= df[df['region'].str.contains("SSRO")]

    plt.plot( 'Date_hour', 'Numsites', data=dfCJRO, label = "CJRO")
    plt.plot( 'Date_hour', 'Numsites', data=dfEJRO, label = "EJRO")
    plt.plot( 'Date_hour', 'Numsites', data=dfKRO, label = "KRO")
    plt.plot( 'Date_hour', 'Numsites', data=dfNSRO, label = "NSRO")
    plt.plot( 'Date_hour', 'Numsites', data=dfSSRO, label = "SSRO")
    plt.suptitle("# 3G sites having PRL more than 10 %")
    plt.legend()

    plt.savefig(dirname +'/output/3Gprl.png')
    sitefiletoWA(dirname +'/output/3Gprl.png')
    plt.clf()
    plt.cla()
    plt.close()
#==================================================================
    if os.path.exists(dirname +'/output/4Gprl.png'):
        os.remove(dirname +'/output/4Gprl.png')
    sqlscript_query = SQLdict.getSQLScript("prl4Gchart")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
    df = pd.DataFrame(queryresult,columns=fieldnames)
    df["xdate"] = pd.to_datetime(df["xdate"],format="%Y-%m-%d")
    df['xhour'] = pd.to_timedelta(df['xhour'], unit='H')
    df['Date_hour'] =df['xdate'] + df['xhour']

    dfCJRO = df[df['region'].str.contains("CJRO")]
    dfEJRO = df[df['region'].str.contains("EJRO")]
    dfKRO= df[df['region'].str.contains("KRO")]
    dfNSRO= df[df['region'].str.contains("NSRO")]
    dfSSRO= df[df['region'].str.contains("SSRO")]

    plt.plot( 'Date_hour', 'Numsites', data=dfCJRO, label = "CJRO")
    plt.plot( 'Date_hour', 'Numsites', data=dfEJRO, label = "EJRO")
    plt.plot( 'Date_hour', 'Numsites', data=dfKRO, label = "KRO")
    plt.plot( 'Date_hour', 'Numsites', data=dfNSRO, label = "NSRO")
    plt.plot( 'Date_hour', 'Numsites', data=dfSSRO, label = "SSRO")
    plt.suptitle("# 4G sites having PRL more than 10 %")
    plt.legend()

    plt.savefig(dirname +'/output/4Gprl.png')
    sitefiletoWA(dirname +'/output/4Gprl.png')
    plt.clf()
    plt.cla()
    plt.close()
    print('endPrinting')

def todaytask():
    currentDate = datetime.datetime.today()- datetime.timedelta(hours =24)
    sendTexttoWA("Scheduled task :")
    sendTexttoWA("Cell Level Mycom Statistic at 09:00")
    sendTexttoWA("Dashboard network level at 09:10 ")
    sendTexttoWA("Network Performance Resume ( " + currentDate.strftime("%Y-%m-%d") + " ) at 12:00")
    sendTexttoWA("Golden Parameter Check at 09:30 ")
    sendTexttoWA("Zero traffic Check at 09:30 ")

def criticalparam():
    window.wm_title("critical parameter is running.. ")
    currentDate = datetime.datetime.today()- datetime.timedelta(hours =24)
    sendTexttoWA("critical parameter check is on progress...  ")
    #booleanmycom = bool(1)

    #schedule.every(120).seconds.do(exit_data)
    fieldnames = []
    if not os.path.exists(dirname + "/output"):
        os.makedirs(dirname + "/output")


    #============================================================================
    if os.path.exists(dirname +'/output/4Gcritical_parameter.csv'):
        os.remove(dirname +'/output/4Gcritical_parameter.csv')
        outputfile = open(dirname +'/output/4Gcritical_parameter.csv', 'x')
    else:
        outputfile = open(dirname +'/output/4Gcritical_parameter.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("4Gcritical")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2G = pd.DataFrame(queryresult,columns  = fieldnames)
    df_2G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/4Gcritical_parameter.csv')
    #============================================================================
    #============================================================================
    if os.path.exists(dirname +'/output/3Gcritical_parameter.csv'):
        os.remove(dirname +'/output/3Gcritical_parameter.csv')
        outputfile = open(dirname +'/output/3Gcritical_parameter.csv', 'x')
    else:
        outputfile = open(dirname +'/output/3Gcritical_parameter.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("3Gcritical")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2G = pd.DataFrame(queryresult,columns  = fieldnames)
    df_2G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/3Gcritical_parameter.csv')
    #============================================================================
    #============================================================================
    if os.path.exists(dirname +'/output/2GcriticalBTS_parameter.csv'):
        os.remove(dirname +'/output/2GcriticalBTS_parameter.csv')
        outputfile = open(dirname +'/output/2GcriticalBTS_parameter.csv', 'x')
    else:
        outputfile = open(dirname +'/output/2GcriticalBTS_parameter.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("2GcriticalBTS")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2G = pd.DataFrame(queryresult,columns  = fieldnames)
    df_2G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/2GcriticalBTS_parameter.csv')
    #============================================================================
    #============================================================================
    if os.path.exists(dirname +'/output/2GcriticalPOC_parameter.csv'):
        os.remove(dirname +'/output/2GcriticalPOC_parameter.csv')
        outputfile = open(dirname +'/output/2GcriticalPOC_parameter.csv', 'x')
    else:
        outputfile = open(dirname +'/output/2GcriticalPOC_parameter.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("2GcriticalPOC")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2G = pd.DataFrame(queryresult,columns  = fieldnames)
    df_2G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/2GcriticalPOC_parameter.csv')
    #============================================================================
    #============================================================================
    if os.path.exists(dirname +'/output/2GcriticalHOC_parameter.csv'):
        os.remove(dirname +'/output/2GcriticalHOC_parameter.csv')
        outputfile = open(dirname +'/output/2GcriticalHOC_parameter.csv', 'x')
    else:
        outputfile = open(dirname +'/output/2GcriticalHOC_parameter.csv', 'x')
    sqlscript_query = SQLdict.getSQLScript("2GcriticalHOC")
    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report",ipheidi,userheidi,passwodjeidi)
    df_2G = pd.DataFrame(queryresult,columns  = fieldnames)
    df_2G.to_csv(outputfile, header=None, index=None, mode='a')
    outputfile.close()
    sitefiletoWA(dirname +'/output/2GcriticalHOC_parameter.csv')
    #============================================================================
    sendTexttoWA("critical parameter check completed ")
    window.wm_title("critical parameter completed ")

def Thread_performance():
    #schedule.every().day.at("07:00").do(todaytask)
    #print("start")
    schedule.every().day.at("09:15").do(run_threaded1,mycomstat)
    #schedule.every().day.at("09:00").do(run_threaded1,iin_dashboards)
    #schedule.every().day.at("09:20").do(run_threaded1,GPcheck)
    schedule.every().day.at("09:30").do(run_threaded1,getzerotraffic)
    #schedule.every().monday.at("09:40").do(run_threaded1,criticalparam)
    #schedule.every().day.at("09:20").do(run_threaded1,searchSuffix)

    schedule.every().day.at("07:20").do(charting4G3G2G)

    schedule.every().day.at("20:20").do(charting4G3G2G)


    schedule.every().day.at("02:30").do(run_threaded1,updatetabletraffic4G_dummy)

    schedule.every().day.at("03:00").do(run_threaded1,updatetabletraffic4G)
    schedule.every().day.at("07:15").do(run_threaded1,updatetabletraffic4G)
    schedule.every().day.at("13:15").do(run_threaded1,updatetabletraffic4G)
    schedule.every().day.at("20:15").do(run_threaded1,updatetabletraffic4G)
    

    schedule.every().day.at("03:00").do(create_temp_tbl_yesterday)
    schedule.every().day.at("09:00").do(searchSuffix)
    #print("Thread_performance")
    while True:
        schedule.run_pending()
        time.sleep(60)

def run_threaded1(threadtarget):
#    current_process = psutil.Process()
#    children = current_process.children(recursive=True)
    if __name__ == "__main__":
        job_thread1= threading.Thread(target=threadtarget)
        job_thread1.daemon = True
        job_thread1.start()


def testhread():
    global WAIT_TIME_SECONDS
    WAIT_TIME_SECONDS = 2

#    print('testing')
#    schedule.every(4).minutes.do(charting4G3G2G)
#    print('do charting')
#    format = "%(asctime)s: %(message)s"
#    logging.basicConfig(format=format, level=logging.INFO,
#                        datefmt="%H:%M:%S")
#    while True:
#        schedule.run_pending()
#        time.sleep(60)

    while True:


        #run_threaded1(charting4G3G2G)
        #sprint("tes GPcheck")
        #time.sleep(60)
#        run_threaded1(charting4G3G2G) # done
#        run_threaded1(updatetabletraffic4G) # done
        run_threaded1(searchSuffix) # done

        #print("TES searchingSuffix")

#        run_threaded1(charting4G3G2G) # done

        print("done")
        time.sleep(2300)


def runschedule():
    global ipheidi
    ipheidi = e1.get()
    global userheidi
    userheidi = e2.get()
    global passwodjeidi
    passwodjeidi = e4.get()
    global outputadd
    outputadd = e3.get()
    tessconnection_result = suportingsystem.test_con(ipheidi,userheidi,passwodjeidi)

    if tessconnection_result == "ok":

        #timeshcedule = combotime.get()
        #marginDegradationavail = combomarginavail.get()
        if ipheidi == "" or userheidi == ""  or passwodjeidi == ""  or outputadd == "" :
            messagebox.showinfo("SUSY","User input is required")
        else:
            #sendTexttoWA("Surveillance system is now on line")
            #print("Thread started")
            window.wm_title("Thread started")
            #print(threading.active_count())
            #print("-----")
            if __name__ == "__main__":
                #print(threading.active_count())

#                t1 = threading.Thread(target=Thread_performance)
                t1 = threading.Thread(target=testhread)
                #t1 = threading.Thread(target=Thread_performance)
                t1.daemon = True
                t1.start()
                #print(os.getpid())
            #t1.Join()

            #t2 = threading.Thread(target=Thread_two)
            #t2.daemon = True
            #t2.start()
            #b6.config(state="disabled")


    else:
        messagebox.showinfo("SUSY","SQL connection fail")

    #time.sleep(2)

def stopschedule():
    sendTexttoWA("Surveillance system terminated")
    messagebox.showinfo("SUSY", "Program terminated")
    driver.close()
    sys.exit()

def basicsetup():
    e1.delete(0, END)
    e1.insert(0,"10.158.234.215")
    e2.delete(0, END)
    e2.insert(0,"npdimas")
    e3.delete(0, END)
    e3.insert(0,"My Number")
    e4.delete(0, END)
    e4.insert(0,"brv7ac")
    window.wm_title("Status : SQL server default setup is loaded")
    #l5.config(text="Status : SQL server default setup is loaded")
    #l5.grid(row=2,column=1)


def tes_con():

    tessconnection_result = suportingsystem.test_con(ipheidi,userheidi,passwodjeidi)
    if tessconnection_result == "ok":
        messagebox.showinfo("SUSY","SQL connection success")
    else:
        messagebox.showinfo("SUSY","SQL connection fail")


window = Tk()

window.wm_title("SUSY (idle)")
l1=Label(window,text="IP address")
l1.grid(row=0,column=0)

l2=Label(window,text="User")
l2.grid(row=0,column=2)

l3=Label(window,text="Output")
l3.grid(row=1,column=0)

l4=Label(window,text="Password")
l4.grid(row=1,column=2)

#l5=Label(window,text="Processing Schedule")
#l5.grid(row=2,column=1)

#l5=Label(window,text="80% availaility Margin")
#l5.grid(row=3,column=1)



IPadd =StringVar()
e1=Entry(window,textvariable=IPadd)
e1.grid(row=0,column=1)

user =StringVar()
e2=Entry(window,textvariable=user)
e2.grid(row=0,column=3)

output =StringVar()
e3=Entry(window,textvariable=output)
e3.grid(row=1,column=1)

userpass =StringVar()
e4=Entry(window,textvariable=userpass, show="*")
e4.grid(row=1,column=3)

#combotime = ttk.Combobox(window,values=['05:00','07:00','09:00','10:00','12:00','14:00','16:00','18:00','20:00'])
#combotime.grid(row=2, column=2,columnspan=2, sticky=W)



b1=Button(window,text="Test SQL Connection", width=12, command=tes_con)
b1.grid(row=0,column=6, padx=10,pady=10)

b1=Button(window,text="Run", width=12, command=runschedule)
b1.grid(row=1,column=6, padx=10,pady=10)

b2=Button(window,text="Stop", width=12,command=stopschedule)
b2.grid(row=2,column=6, padx=10,pady=10)

b3=Button(window,text="SQL setup", width=12,command=basicsetup)
b3.grid(row=3,column=6, padx=10,pady=10)


#b6=Button(window,text="close", width=12,command=window.destroy)
#b6.grid(row=7,column=4, pady=20)
window.mainloop()
