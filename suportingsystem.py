import mysql.connector
from mysql.connector import Error
import os
import datetime
dictionary_KPI_now = {}
dictionary_KPI_past = {}
dirname, filename = os.path.split(os.path.abspath(__file__))

def test_con(ipheidi,userheidi,passwodheidi):
    #ipheidi = e1.get()
    #userheidi = e2.get()
    #passwodheidi = e4.get()
    try:
       mySQLconnection = mysql.connector.connect(host=ipheidi,
                                 database='isat_cm',
                                 user=userheidi,
                                 password=passwodheidi)
       #sql_select_Query = "select oss from lncel limit 1"
       cursor = mySQLconnection .cursor()
       #cursor.execute(sql_select_Query)
       return "ok"
    except Error as e :
        return "SQL Connection fail"


def query_command(SqlScript,feedback,DBname,IP,userheidi,passwordheidy):
    #IP = "10.158.234.215"#e1.get()
    #userheidi = "npdimas"#e2.get()
    #passwordheidy = "brv7ac"#e4.get()
    field_names=[]

    try:
       mySQLconnection = mysql.connector.connect(host=IP,
                                 database=DBname,
                                 user=userheidi,
                                 password=passwordheidy)
       sql_select_Query = SqlScript
       cursor = mySQLconnection .cursor()
       cursor.execute(sql_select_Query)
       if feedback != "nofeedback":
           records = cursor.fetchall()
           field_names = [i[0] for i in cursor.description]
           #print(field_names)
       cursor.close()
    except Error as e :
        currentDate = datetime.datetime.today()
        if os.path.exists('history.txt'):
            outputfileHistory = open("history.txt", "a")
        else:
            outputfileHistory = open("history.txt", "x")
        outputfileHistory.write('Error while connecting to MySQL\n' + currentDate.strftime("%Y-%m-%d"))
        outputfileHistory.close()
        records = "error"
    if feedback != "nofeedback":
        return(records,field_names)

def queryPostProcessing1(records,field_names,datenow,id): # compare post and now
    #print(datenow)
    if not os.path.exists(dirname + "/output"):
        os.makedirs(dirname + "/output")

    if os.path.exists(dirname +'/output/comparasion_output' + id + '.txt'):
        os.remove(dirname +'/output/comparasion_output' + id + '.txt')
        outputfilecompere = open(dirname +'/output/comparasion_output' + id + '.txt', 'x')
    else:
        outputfilecompere = open(dirname +'/output/comparasion_output' + id + '.txt', 'x')

    dictionary_KPI_now.clear()
    dictionary_KPI_past.clear()
    #print(records)
    #print(datenow)
    for row in records:
        #print(str(row))
        if row[0].strftime("%Y-%m-%d") == datenow:
            #print('masuk now')
            if row[1] is not None:
                dictionary_KPI_now[row[1]] = dict(zip(field_names, row))#[row[1]]= row[2]
        #    print(row)
        else:
            #print('masuk past')
            if row[1] is not None:
                dictionary_KPI_past[row[1]] = dict(zip(field_names, row))

    JAVdata=[]
    KALdata=[]
    SUMdata=[]
    SSdata=[]
    JAVdataPercentage=[]
    KALdataPercentage=[]
    SUMdataPercentage=[]
    SSdataPercentage=[]

    for Region in dictionary_KPI_past:
        stringtoWrite = ""
        temporarivalue = []
        temporarivaluepercentage = []
        #print(str(dictionary_KPI_now[Region]))
        for kpi in dictionary_KPI_past[Region]:
            #print(kpi)
            if "xDate" not in kpi:
                if "oss" not in kpi:
                    #print(kpi)
                    #stringHeadertoWrite = stringHeadertoWrite + "\t" + kpi
                    #print(dictionary_KPI_now[Region][kpi])
                    #print(dictionary_KPI_past[Region][kpi])
                    if  dictionary_KPI_now[Region][kpi] is None and dictionary_KPI_past[Region][kpi] is None:
                        #print("Data Not available")
                        temporarivalue.append( "Data Not available")
                        temporarivaluepercentage.append( "NA")
                    elif dictionary_KPI_now[Region][kpi] is not None and dictionary_KPI_past[Region][kpi] is None:
                        #print("pass is none")
                        temporarivalue.append( strip(str(round(dictionary_KPI_now[Region][kpi],1))))
                        temporarivaluepercentage.append( "NA")
                    elif dictionary_KPI_past[Region][kpi] is not None and dictionary_KPI_now[Region][kpi] is not None:
                        delta = dictionary_KPI_now[Region][kpi]  - dictionary_KPI_past[Region][kpi]
                        if delta == 0 :
                            percentage = 0
                        else:
                            percentage = round((delta/dictionary_KPI_past[Region][kpi])*100,1)
                        temporarivalue.append( str(round(dictionary_KPI_now[Region][kpi],1)))
                        temporarivaluepercentage.append( str(percentage) + "%")
                        #stringtoWrite = stringtoWrite + "|" + str(round(dictionary_KPI_now[Region][kpi],1)) + " (" + str(percentage) + ")"
                            #stringtoWrite = stringtoWrite + "|" + str(round(dictionary_KPI_now[Region][kpi],1)) + " ( NA )"
                    else:
                        #print("Data Not available all")
                        temporarivalue.append( "Data Not available")
                        temporarivaluepercentage.append( "NA")
                            #stringtoWrite = stringtoWrite + "|Data Not available ( NA )"
        #perKPI stop here
        if str(Region) == "JAV":
            #print("JAV:")
            JAVdata = temporarivalue
            JAVdataPercentage = temporarivaluepercentage
        elif str(Region) == "KLM":
            #print("KA:")
            KALdata = temporarivalue
            KALdataPercentage = temporarivaluepercentage
        elif str(Region) == "SMT":
            #print("SMT:")
            SUMdata = temporarivalue
            SUMdataPercentage = temporarivaluepercentage
        elif str(Region) == "SS":
            #print("SS:")
            SSdata = temporarivalue
            SSdataPercentage = temporarivaluepercentage
    #per region stop here
        #outputfilecompere.write(stringtoWrite + '\n')
    outputfilecompere.write("       KPI          JAV        KAL         SMT         SS"+ '\n')
    i = 0
    for header in field_names [2:]:
        if len(header) < 15 :
            stringheader = addspace(header,15 - len(header))
        #---------------------------------------------------------------
        if len(JAVdata) > 0 :
            if len(str(JAVdata[i])) < 12 :
                stringJAV = addspace(str(JAVdata[i]),12-len(str(JAVdata[i])))
            else:
                stringJAV = JAVdata[i]
        else:
            stringJAV = "     NA     "
        #---------------------------------------------------------------
        #print(KALdata)
        if len(KALdata)> 0 :
            #print(KALdata[i])
            if len(str(KALdata[i])) < 12 :
                stringKAL = addspace(str(KALdata[i]),12-len(str(KALdata[i])))
            else:
                stringKAL = KALdata[i]
        else:
            stringKAL = "     NA     "
            #---------------------------------------------------------------
        if len(SUMdata)> 0 :
            if len(str(SUMdata[i])) < 12 :
                stringSUM = addspace(str(SUMdata[i]),12-len(str(SUMdata[i])))
            else:
                stringSUM = SUMdata[i]
        else:
            stringSUM = "     NA     "
        #---------------------------------------------------------------
        if len(SSdata)> 0 :
            if len(str(SSdata[i])) < 12 :
                stringSS = addspace(str(SSdata[i]),12-len(str(SSdata[i])))
            else:
                stringSS = SSdata[i]
        else:
            stringSS = "     NA     "
        i += 1
        #---------------------------------------------------------------
            #print(i)
            #print(stringKAL)
            #print(stringSUM)
        outputfilecompere.write(str(stringheader) + str(stringJAV) + str(stringKAL) + str(stringSUM) + str(stringSS) + '\n')

    outputfilecompere.write('_     Comparation Result     _' + '\n')
    i = 0
    for header in field_names [2:]:
        if len(header) < 15 :
            stringheader = addspace(header,15 - len(header))
        #---------------------------------------------------------------
        if len(JAVdataPercentage) > 0 :
            if len(str(JAVdataPercentage[i])) < 12 :
                stringJAV = addspace(str(JAVdataPercentage[i]),12-len(str(JAVdataPercentage[i])))
            else:
                stringJAV = JAVdataPercentage[i]
        else:
            stringJAV = "     NA     "
        #---------------------------------------------------------------
        if len(KALdataPercentage)> 0 :

            if len(str(KALdataPercentage[i])) < 12 :
                stringKAL = addspace(str(KALdataPercentage[i]),12-len(str(KALdataPercentage[i])))
            else:
                stringKAL = KALdataPercentage[i]
        else:
            stringKAL = "     NA     "
            #---------------------------------------------------------------
        if len(SUMdataPercentage)> 0 :
            if len(str(SUMdataPercentage[i])) < 12 :
                stringSUM = addspace(str(SUMdataPercentage[i]),12-len(str(SUMdataPercentage[i])))
            else:
                stringSUM = SUMdataPercentage[i]
        else:
            stringSUM = "     NA     "
        #---------------------------------------------------------------
        if len(SSdataPercentage)> 0 :
            if len(str(SSdataPercentage[i])) < 12 :
                stringSS = addspace(str(SSdataPercentage[i]),12-len(str(SSdataPercentage[i])))
            else:
                stringSS = SSdataPercentage[i]
        else:
            stringSS = "     NA     "
        i += 1
        #---------------------------------------------------------------
            #print(i)
            #print(stringKAL)
            #print(stringSUM)
        outputfilecompere.write(str(stringheader) + str(stringJAV) + str(stringKAL) + str(stringSUM) + str(stringSS) + '\n')

    return(dirname +'/output/comparasion_output' + id + '.txt')
    outputfilecompere.close()

def addspace(textori,spacecar):
    i = 1
    while i < spacecar+1:
      textori = textori + " "
      i += 1
    return(textori)


