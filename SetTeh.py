import openpyxl,io,pymysql
from Classes import Integral
from datetime import date, timedelta
TimeLine = ["'040000'","'060000'","'080000'","'100000'",
"'120000'","'140000'","'160000'","'180000'","'200000'","'220000'","'000000'","'015900'"]

def UpdateTehRej(NameOfFile,conn,QuantityOfFields,nameOfTable):
    with open(NameOfFile, "rb") as f:
        in_mem_file = io.BytesIO(f.read())
    wb = openpyxl.load_workbook(in_mem_file,read_only=True,data_only=True)
    ws = wb.active
    Data = []

    temp = ws['C8:H8']
    for i in temp[0]:
        Data.append(i.value)
    cur = conn.cursor()
    for i in range(QuantityOfFields):
        for j in range(12):
            cur.execute(('UPDATE '+nameOfTable+' SET jidkTehRej='+str(Data[3*i+0])+',neftTehRej='+str(Data[3*i+1])+',tehRejSdacha='+str(Data[3*i+2])+
               ',jidkTehRejNakl='+str((j+1)*Data[3*i+0])+',neftTehRejNakl='+str((j+1)*Data[3*i+1])+',tehRejSdachaNakl='+str((j+1)*Data[3*i+2]) 
        		+ ' WHERE mrID='+str(i) +' AND time='+TimeLine[j]))

    conn.commit()
    cur.close()
