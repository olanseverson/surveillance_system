# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 15:59:14 2019

@author: Olan
"""

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import os
import schedule
import threading,time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import SQLdict
import pandas as pd

import suportingsystem
from bs4 import BeautifulSoup as bs
from timeloop import Timeloop
from datetime import timedelta
import logging
from queue import Queue


## %% Initiate logger for DEBUGGING

logging.basicConfig(level = logging.WARNING,)
#logging.root.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter("[%(levelname)s] => (%(name)s||%(threadName)-s):  %(message)s")
logger_handler = logging.StreamHandler() # handler
logger_handler.setFormatter(FORMATTER)

logger = logging.getLogger(__name__)

# change DEBUG to another value to remove the debug logger
logger.setLevel(logging.DEBUG)
## %% Open webdriver
dirname, filename = os.path.split(os.path.abspath(__file__))

driver = webdriver.Chrome(dirname + '/chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 100)

# for python bot
target = '"Bot Nokia"'
prevChat = {}
isMainBusy = False
isNeedReply = False
BUF_SIZE = 10
q = Queue(BUF_SIZE) # queue to store received command in bot
running_procedure = ""
## %%

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
        attach=driver.find_element_by_css_selector('input[type="file"]')
        attach.send_keys(fileToSend)
        time.sleep(5)
        send=driver.find_element_by_xpath("//div[contains(@class, 'iA40b')]")
        send.click()

def sendTexttoWA(messageText):
    x_arg = '//span[contains(@title,' + target + ')]'
    group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
    group_title.click()
    message = driver.find_elements_by_xpath('//*[@contenteditable="true"]')[-1]
    message.send_keys(messageText + '\n')

def mycomstat():
    window.wm_title("mycom statistic is running.. ")
    currentDate = datetime.datetime.today()- datetime.timedelta(hours =24)
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

# def searchSuffix():
#     print('2g')
#     searching ('2G')
#     print('3g')
#     searching ('3G')
#     print('4g')
#     searching ('4G')

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
    if (gen == '2G' or gen == '2g'):

        # create table today
        print('create table today')
        sqlscript_query = SQLdict.getSQLScript("2G_today_create_table")
        suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")

        # get missing sites from DB
        print('get missing file')
        sqlscript_query = SQLdict.getSQLScript("get_missing_2G")
        queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
        dfmissed = pd.DataFrame(queryresult,columns=fieldnames)
    #    print (dfmissed)
    #    print (dfmissed.columns)

        # save file
        print ("Save missing sites")
        outputfile = r'C:\Users\Olan\Desktop\python\output\2G_missing.csv'
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
            outputfile = r'C:\Users\Olan\Desktop\python\output\2G_union.csv'
            df_union.to_csv(outputfile, index = None, header=True)

            #sending file to WA
            sitefiletoWA(dirname +'/output/2G_union.csv')

            # sending statistics to WA
            statistics = df_union.groupby(['Remark']).size() # Series data type
            for idx in range(len(statistics)):
                temp_str = str(statistics.index[idx]) + ': ' + str(statistics[idx])
                sendTexttoWA(temp_str)
    elif (gen == '3G'or gen == '3g'):
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
            outputfile = r'C:\Users\Olan\Desktop\python\output\3G_union.csv'
            df_union.to_csv(outputfile, index = None, header=True)

            #sending file to WA
            sitefiletoWA(dirname +'/output/3G_union.csv')

            # sending statistics to WA
            statistics = df_union.groupby(['Remark']).size() # Series data type
            for idx in range(len(statistics)):
                temp_str = str(statistics.index[idx]) + ': ' + str(statistics[idx])
                sendTexttoWA(temp_str)
    elif (gen == '4G' or gen == '4g'):
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
        outputfile = r'C:\Users\Olan\Desktop\python\output\4G_missing.csv'
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

def Thread_performance():
    schedule.every().day.at("07:20").do(charting4G3G2G)
    schedule.every().day.at("20:20").do(charting4G3G2G)
    schedule.every().day.at("02:30").do(run_threaded1,updatetabletraffic4G_dummy)
    schedule.every().day.at("03:00").do(run_threaded1,updatetabletraffic4G)
    schedule.every().day.at("07:15").do(run_threaded1,updatetabletraffic4G)
    schedule.every().day.at("13:15").do(run_threaded1,updatetabletraffic4G)
    schedule.every().day.at("20:15").do(run_threaded1,updatetabletraffic4G)
    schedule.every().day.at("03:00").do(create_temp_tbl_yesterday)
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


##%% Get Chat From WA

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

def isExistInDB(cmd, filename):
    isFound = False
    procedure_name = None
    isNeedReply = None
    data = pd.read_csv(filename) 
    for idx in range(len(data['command'])):
        if (data['command'][idx] == cmd):
        # if (cmd.find(data['command'][idx]) != -1):
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
    global running_procedure
    isFound, procedure_name, Reply= isExistInDB(command['text'].lower(), 'command.csv')
    if (isFound == True): # if command is a recognized command
        if (isMainBusy == True): # busy, doing another request
            if (isNeedReply == False):
                logger.info('busy')
                sendTexttoWA(running_procedure + " is running, please wait until finished!")
        else:
            isNeedReply = Reply
            isMainBusy  = True
            running_procedure = procedure_name
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
        sendTexttoWA("BOT:Unknown command for: "+ command['text'])
        
def echo():
    logger.setLevel(logging.DEBUG)# logger
    global isMainBusy
    logger.debug("START ECHO")
    sendTexttoWA("echo is running...")
    time.sleep(5)
    isMainBusy = False;
    logger.debug("isMainBusy :%d ", isMainBusy)
    logger.debug("TERMINATE ECHO")

def searchsuffix():
    global isMainBusy
    global isNeedReply
    isCmdComplete = False
    logger.debug('START SEARCHING')
    sendTexttoWA("What kind of network?(2g/3g/4g)")
    while isCmdComplete == False:
        if (q.empty() == True):
            pass
        message = q.get()
        logging.debug("Consumer storing message: %s (size=%d)", message, q.qsize())
        if (message == '2g' or message == '3g' or message == '4g'):
            sendTexttoWA(message + " suffix searching is running...")
            searching(message)
            logger.debug('message is : %s', message)
            isNeedReply = False;
            with q.mutex:
                q.queue.clear()
            isCmdComplete = True
        else:
            logger.debug('invalid respon')
        
    isMainBusy = False
    logger.debug("END SEARCHING")
    return;

def charting():
    global isMainBusy
    logger.debug('START CHARTING')
    sendTexttoWA("Charting is running...")
    charting4G3G2G()
    # time.sleep(8)
    isMainBusy = False
    logger.debug("END CHARTING")
    return;

def stats():
    global isMainBusy
    logger.debug('START COM STATUS')
    sendTexttoWA("Display Com Status is running...")
    mycomstat()
    # time.sleep(8)
    isMainBusy = False
    logger.debug("END COM STATUS")
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

def testhread():
    # schedule.every().day.at("07:20").do(charting4G3G2G)
    # schedule.every().day.at("20:20").do(charting4G3G2G)
    # schedule.every().day.at("03:00").do(run_threaded1,updatetabletraffic4G)
    # schedule.every().day.at("07:15").do(run_threaded1,updatetabletraffic4G)
    # schedule.every().day.at("13:15").do(run_threaded1,updatetabletraffic4G)
    # schedule.every().day.at("20:15").do(run_threaded1,updatetabletraffic4G)
    # schedule.every().day.at("03:00").do(create_temp_tbl_yesterday)

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
                print(str(isMainBusy) + " " + str(isNeedReply))
                prevChat = recentChat
                if (isMainBusy == True and isNeedReply == True):
                    # logger.debug('adding to queue')
                    logger.info('add command to queue')
                    if not q.full():
                        q.put(recentChat['text'])
                    logger.info('Putting ' + recentChat['text']
                            + ' : ' + str(q.qsize()) + ' items in queue')
                else:
                    print('here')
                    logger.debug("doCommand")
                    doCommand(recentChat)


        # DEBUGGING THREAD
        # schedule.run_pending()
        print("Total number of threads", threading.activeCount())
        # logger.debug("isMainBusy = " + str(isMainBusy))
        # logger.debug("isNeedReply = " + str(isNeedReply))
    #    print("List of threads: ", threading.enumerate())
    #    print("this thread: ", threading.current_thread)

    if __name__ == "__main__":
        tl.start(block=True)
        # while True:
            # schedule.run_pending()
            # print("here")


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
        if ipheidi == "" or userheidi == ""  or passwodjeidi == ""  or outputadd == "" :
            messagebox.showinfo("SUSY","User input is required")
        else:
            window.wm_title("Thread started")
            if __name__ == "__main__":
                t1 = threading.Thread(target=testhread)
                #t1 = threading.Thread(target=Thread_performance)
                t1.daemon = True
                t1.start()
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
    e3.insert(0,"Bot Nokia")
    e4.delete(0, END)
    e4.insert(0,"brv7ac")
    window.wm_title("Status : SQL server default setup is loaded")

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

b1=Button(window,text="Test SQL Connection", width=12, command=tes_con)
b1.grid(row=0,column=6, padx=10,pady=10)

b1=Button(window,text="Run", width=12, command=runschedule)
b1.grid(row=1,column=6, padx=10,pady=10)

b2=Button(window,text="Stop", width=12,command=stopschedule)
b2.grid(row=2,column=6, padx=10,pady=10)

b3=Button(window,text="SQL setup", width=12,command=basicsetup)
b3.grid(row=3,column=6, padx=10,pady=10)

window.mainloop()
