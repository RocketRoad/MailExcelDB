def extractData(CellPos,ws):
    temp = []
    for i in ws[CellPos][0]:
                if i.value!=None:
                        temp.append(i.value)
                else:
                    return temp
    return temp

def ExtrapolateData(Data,Number):
    try:
        Average = sum(Data)/len(Data)
    except ZeroDivisionError:
        Average = 0
    for i in range(Number-len(Data)):
        Data.append(Average)
def Integral(Data):
    Result = []
    Sum = 0
    for i in Data:
        Sum+=float(i)
        Result.append(Sum)
    return Result

class field:

    CurrentWaterExt = []
    AccumCurrentWaterExt = []
    YestWaterExt = []
    YestAccumWaterExt = []
    ws1 = []
    ws2 = []
    CurrentOilExt = []
    AccumCurrentOilExt = []
    YestOilExt = []
    YestAccumOilExt = []

    OilRelease = []
    AccumOilRelease = []
    YestOilRelease = []
    YestAccumOilRelease = []

    QuantityOfData = 0
    
    def __init__(self,ws1_,ws2_):
        self.ws1 = ws1_
        self.ws2 = ws2_

    def setAllCurrentData(self,CWE,COE,OR):
        self.CurrentWaterExt = extractData(CWE,self.ws1)
        ExtrapolateData(self.CurrentWaterExt,12)
        self.AccumCurrentWaterExt = Integral(self.CurrentWaterExt)

        self.CurrentOilExt = extractData(COE,self.ws2)
        self.QuantityOfData = len(self.CurrentOilExt)
        ExtrapolateData(self.CurrentOilExt,12)
        self.AccumCurrentOilExt = Integral(self.CurrentOilExt)

        self.OilRelease = extractData(OR,self.ws2)
        ExtrapolateData(self.OilRelease,12)
        self.AccumOilRelease = Integral(self.OilRelease)

    def setYesterdayData(self,pos):
        with open('jidkPred.txt') as f:
            lines = f.read().splitlines()
        self.YestWaterExt = lines[(12*(pos-1)):12*pos]
        self.YestAccumWaterExt = Integral(self.YestWaterExt)
        with open('neftPred.txt') as f:
            lines = f.read().splitlines()        
        self.YestOilExt = lines[(12*(pos-1)):12*pos]
        self.YestAccumOilExt = Integral(self.YestOilExt)
        with open('sdachaPred.txt') as f:
            lines = f.read().splitlines()  
        self.YestOilRelease = lines[(12*(pos-1)):12*pos]
        self.YestAccumOilRelease = Integral(self.YestOilRelease)
    def getListOfVariables(self):
        return [self.CurrentWaterExt,self.AccumCurrentWaterExt,self.YestWaterExt,self.YestAccumWaterExt,self.CurrentOilExt,self.AccumCurrentOilExt,self.YestOilExt,self.YestAccumOilExt,
        self.OilRelease,self.AccumOilRelease,self.YestOilRelease,self.YestAccumOilRelease]
