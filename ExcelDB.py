import openpyxl,sqlite3,io,pymysql,re
from Classes import field
from datetime import date, timedelta
from SetTeh import UpdateTehRej
TimeLine = ["'040000'","'060000'","'080000'","'100000'",
"'120000'","'140000'","'160000'","'180000'","'200000'","'220000'","'000000'","'015900'"]
ListOfVariables = ['jidkPrognoz','jidkPrognozNakl','jidkPredDnya','jidkDenNakl',
'neftPrognoz','neftPrognozNakl','neftPredDnya','neftDenNakl',
'sdachaPrognoz','sdachaPrognozNakl','sdachaPredDnya','sdachaDenNakl']

#pu,cdng ,mrID ,data ,time ,Tin ,
#jidkPredDnya ,jidkDenNakl ,jidkPrognoz ,jidkPrognozNakl , jidkTehRej , jidkTehRejNakl ,
#neftPredDnya ,neftDenNakl ,neftPrognoz ,neftPrognozNakl ,neftTehRej ,neftTehRejNakl ,
#sdachaPredDnya ,sdachaDenNakl ,sdachaPrognoz ,sdachaPrognozNakl 
def LoadDocument(NameOfFile,conn):
	nameOfTable = 'hoursDlc_copy2'
        if(NameOfFile=='Empty mail'):
            return
        mmg = re.compile('ММГ ЦППН ММГ.*')
        r = mmg.findall(NameOfFile)
        if(r==[]):
            plan = re.compile('План добычи.*')
            r = mmg.findall(NameOfFile)
            if(r==[]):
                return
            else:
            	UpdateTehRej(NameOfFile,conn,2,nameOfTable)
        with open(NameOfFile, "rb") as f:
                in_mem_file = io.BytesIO(f.read())
        wb = openpyxl.load_workbook(in_mem_file,read_only=True,data_only=True)

        Zhetibay = field(wb['показ.ПУН'],wb['ЦППН ЖМГ'])
        Zhetibay.setAllCurrentData('D13:O13','C38:N38','C34:N34')
        Zhetibay.setYesterdayData(1)
        Kalamkas = field(wb['показ.ПУН'],wb['ЦППН КМГ'])
        Kalamkas.setAllCurrentData('D22:O22','C81:N81','C77:N77')
        Kalamkas.setYesterdayData(2)	
        FIELDS = [Zhetibay,Kalamkas]



        ###############################SQL Part######################################################
        #conn = sqlite3.connect('DATA.db')
        
        today = date.today()
        p = 'w'
        for i in FIELDS:
                if(i.QuantityOfData==12):
                       with open('jidkPred.txt', p) as f:
                            for item in i.CurrentWaterExt:
                                f.write("%s\n" % item)
                       with open('neftPred.txt', p) as f:
                            for item in i.CurrentOilExt:
                                f.write("%s\n" % item)
                       with open('sdachaPred.txt', p) as f:
                            for item in i.OilRelease:
                                f.write("%s\n" % item)
                p = 'a'       
        cur = conn.cursor()
        Index = -1
        for i in FIELDS:
            Index+=1
            Temp = ["'020000'"]+TimeLine
            for j in range(13):
                cur.execute('UPDATE '+nameOfTable+' SET Tin='+str(i.QuantityOfData>(j-1))+',data='+
                	(today - ((i.QuantityOfData>10)*2-1)*timedelta((i.QuantityOfData>10)==(j<11))).strftime("'%Y-%m-%d'") + 
                   ' WHERE mrID='+str(Index) +' AND time='+Temp[j])

            for k in range(len(ListOfVariables)):
                for j in range(12):
                    cur.execute('UPDATE '+nameOfTable+' SET ' + ListOfVariables[k] +'=' + 
                      	str((i.getListOfVariables())[k][j]) 
                        + ' WHERE mrID='+str(Index) +' AND time='+TimeLine[j])


                

        conn.commit()
        cur.close()

