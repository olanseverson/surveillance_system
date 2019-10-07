import tkinter as tk
from tkinter import filedialog
import pandas as pd

_SUFF1 = 'XXX'
_SUFF2 = 'XYX'

def isAdaSuff(name):
# fungsi untuk mengecek apakah ada suffix atau tidak
# suffix dianggap jika ada XYX dan posisinya paling belakang
    idx1 = name.find(_SUFF1)
    idx2 = name.find(_SUFF2)
    if ((idx1!=-1 and idx1 == len(name)-3) or (idx2!=-1 and idx2 == len(name)-3)):
        return True;
    else:
        return False;
    
def isFound(array, value):
#fungsi untuk mengecek apakah ada 'value' di sebuah 'array
#mengembalikan posisi dimana 'value itu berada
    found = False;
    for row in array:
        if ((str(row)).find(value)!= -1):
            found = True;
            break;
    if (found):
        return row
    else:    
        return '0'

def main():
# program utama
    nama = []
    stat = []
    gen = 4     # dapat diganti untuk memilih antara 4G, 3G, DAN 2G
    
    
#====== BUKA EXCEL FILE ============================
    if gen == 2:
        df1 = pd.read_csv('2G_12.csv')
        df2 = pd.read_csv('2G_13.csv')
    
    if gen == 3:
        df1 = pd.read_csv('3G_12.csv')
        df2 = pd.read_csv('3G_13.csv')
        
    if gen == 4:
        df1 = pd.read_csv('4G_12.csv')
        df2 = pd.read_csv('4G_13.csv')    
#============================================    
    
#============== SEARCHING: MENAMBAHKAN 'STATUS' DI AKHIR ==================
    for after in df2['NAME']:
        if (isAdaSuff(after)): # ada suffix
            name = str(after)[:len(after)-3]
            if (name[-1]=='_'):     # HAPUS '_' JIKA ADA SUFFIXNYA
                name = name[:-1]
            suff = str(after)[len(after)-3:len(after)]
            
            temp = isFound(df1['NAME'], str(name))
            if(temp!= '0'):                             # site lama
                if (isAdaSuff(temp)):
                    if(temp.find(suff)!=-1):
#                        print('1statis: ', after)
                        nama.append(after)
                        stat.append('STATIS')
                    else:
#                        print('1suffix berubah: ' + after)
                        nama.append(after)
                        stat.append('CHG_SUFF')
                else:                                   # nambah suffix
#                    print('1nambah suffix: ' + after)
                    nama.append(after)
                    stat.append('ADD_SUFF')
            else:                                       # site baru
#                print('1baru muncul: ' + after)
                nama.append(after)
                stat.append('NEW SITE')
                
        else: #tidak ada suffix
            temp = isFound(df1['NAME'], str(after))
            if (temp!= '0'):                            #site lama
                if (isAdaSuff(temp)):
#                    print('2removal: ' + temp)
                    nama.append(after)
                    stat.append('DEL_SUFF')
                else:
#                    print('2statis: ', after)
                    nama.append(after)
                    stat.append('STATIS')
            else:                                       #ada site yg baru muncul
#                print('2baru muncul: ' + after)
                nama.append(after)
                stat.append('NEW SITE')
#===================================================================
                
#============== MEMBUAT DICTIONARY  ==================
    data ={}
    for x in df2.columns:
        data[x] = df2[x]
    data["status"] = stat
    
    df = pd.DataFrame(data)
#===================================================================
    
#================== MENGHAPUS ROW YANG NILAINYA TIDAK BERUBAH ======
    df3 = df[df.status!= 'STATIS']
#===================================================================
#============== MENYIMPAN KE DALAM EXCEL (DIALOG) ==================
    root= tk.Tk()
    canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
    canvas1.pack()

    def exportCSV ():
        export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
        df3.to_csv (export_file_path, index = None, header=True)

    saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
    canvas1.create_window(150, 150, window=saveAsButton_CSV)

    root.mainloop()
#===================================================================
if __name__ == '__main__':
   main()
   
   
   
   
#def isAdaSuff(name):
#    # fungsi untuk mengecek apakah ada suffix atau tidak
#        # suffix dianggap jika ada XYX dan posisinya paling belakang
#        idx1 = name.find(_SUFF1)
#        idx2 = name.find(_SUFF2)
#        if ((idx1!=-1 and idx1 == len(name)-3) or (idx2!=-1 and idx2 == len(name)-3)):
#            return True;
#        else:
#            return False;
#    
#    def isFound(array, value):
#    #fungsi untuk mengecek apakah ada 'value' di sebuah 'array
#    #mengembalikan posisi dimana 'value itu berada
#        found = False;
#        for row in array:
#            if ((str(row)).find(value)!= -1):
#                found = True;
#                break;
#        if (found):
#            return row
#        else:    
#            return '0'
#    
#    # data for today
#    if (gen == '2G'):    
#        sqlscript_query = SQLdict.getSQLScript("2G_now_searching")
#    elif (gen == '3G'):
#        sqlscript_query = SQLdict.getSQLScript("3G_now_searching")
#    elif (gen == '4G'):
#        sqlscript_query = SQLdict.getSQLScript("4G_now_searching")
#    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
#    dfnow = pd.DataFrame(queryresult,columns=fieldnames)
#    
#    # data for yesterday
#    if (gen == '2G'):    
#        sqlscript_query = SQLdict.getSQLScript("2G_yesterday_searching")
#    elif (gen == '3G'):
#        sqlscript_query = SQLdict.getSQLScript("3G_yesterday_searching")
#    elif (gen == '4G'):    
#        sqlscript_query = SQLdict.getSQLScript("4G_yesterday_searching")
#    queryresult,fieldnames = suportingsystem.query_command(sqlscript_query,"feedback","isat_report","10.158.234.215","npdimas","brv7ac")
#    dfyesterday = pd.DataFrame(queryresult,columns=fieldnames)
#    
#    print (dfnow['name'])
#    print (dfyesterday['name'])
#    
#    _SUFF1 = 'XXX'
#    _SUFF2 = 'XYX'
#    nama = []
#    stat = []
#    for after in dfnow['name']:
#        if (isAdaSuff(after)): # ada suffix
#            name = str(after)[:len(after)-3]
#            if (name[-1]=='_'):     # HAPUS '_' JIKA ADA SUFFIXNYA
#                name = name[:-1]
#            suff = str(after)[len(after)-3:len(after)]
#            
#            temp = isFound(dfyesterday['name'], str(name))
#            if(temp!= '0'):                             # site lama
#                if (isAdaSuff(temp)):
#                    if(temp.find(suff)!=-1):
#                        nama.append(after)
#                        stat.append('STATIS')
#                    else:
#                        nama.append(after)
#                        stat.append('CHG_SUFF')
#                else:                                   # nambah suffix
#                    nama.append(after)
#                    stat.append('ADD_SUFF')
#            else:                                       # site baru
#                nama.append(after)
#                stat.append('NEW SITE')
#                
#        else: #tidak ada suffix
#            temp = isFound(dfyesterday['name'], str(after))
#            if (temp!= '0'):                            #site lama
#                if (isAdaSuff(temp)):
#                    nama.append(after)
#                    stat.append('DEL_SUFF')
#                else:
#                    nama.append(after)
#                    stat.append('STATIS')
#            else:                                       #ada site yg baru muncul
#                nama.append(after)
#                stat.append('NEW SITE')                
#    print(stat)
#    
#    # add new 'key' namely "status"
#    dfnow["status"] = stat
#    print (dfnow)
#    
#    # remove row with value "STATIS"
#    df_final = dfnow[dfnow.status!= 'STATIS']
#    print(df_final)
#    
#    # save file in local repo
#    if (gen == '2G'):    
#        file_path = r'C:\Users\Olan\Desktop\python\output\2G_suffix.csv'
#    elif (gen == '3G'):
#        file_path = r'C:\Users\Olan\Desktop\python\output\3G_suffix.csv'
#    elif (gen == '4G'):    
#        file_path = r'C:\Users\Olan\Desktop\python\output\4G_suffix.csv'
#    df_final.to_csv(file_path, index = None, header=True)
#    print ("Save to local storage")
#    
#    #sending file to WA
#    sitefiletoWA(file_path)
#    
#    # sending statistics to WA
#    statistics = df_final.groupby(['status']).size() # Series data type
#    for idx in range(len(statistics)):
#        temp_str = str(statistics.index[idx]) + ': ' + str(statistics[idx])
#        sendTexttoWA(temp_str) 
#    if (gen == '2G'):    
#        sendTexttoWA("2G sent.") 
#    elif (gen == '3G'):
#        sendTexttoWA("3G sent.") 
#    elif (gen == '4G'):    
#        sendTexttoWA("4G sent.") 