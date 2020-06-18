import yfinance as yf
from pandas import DataFrame
from .Auction import *


class Stock:
    """Class that represents a Stock object"""
    def __init__(self, symbol, period="max"):
        self.Symbol = symbol
        self.Period = period
        self.History = None
        self._downloadStock()

    def _downloadStock(self):
        self.History = yf.download(self.Symbol, period=self.Period)
        self.History.dropna(inplace=True)
        self.History["Date"] = self.History.index
        self.History.insert(0,"id",range(0,len(self.History.index)))
        self.History.set_index(self.History["id"],inplace=True)
    
    def _getDict(self, property, value="Close"):
        auxDict = dict()
        aList = getattr(self, property)
        for a in aList:
            auxDict[a.Date] = getattr(a, value)
        return auxDict


    @property
    def Hammer(self):
        aux = []
        for i, r in self.History.iterrows():
            if i>0 and i<len(self.History.index)-1:
                a = Auction(r)
                a_1 = Auction(self.History.iloc[i-1])
                a1 = Auction(self.History.iloc[i+1])
                # if a_1.Down:
                if a.Tail >= 2 * a.Body and a.Tail > a.Nose:            
                    if a.Nose < a.Body: 
                        if a1.Up and a1.Open >= max([a.Open,a.Close]) and a1.Close >= a.Close:
                            aux.append(a)
        return aux
    @property
    def InvertedHammer(self):
        aux = []
        for i, r in self.History.iterrows():
            if i>0 and i<len(self.History.index)-1:
                a = Auction(r)
                a_1 = Auction(self.History.iloc[i-1])
                a1 = Auction(self.History.iloc[i+1])
                # if a_1.Down:
                if a.Nose >= 2 * a.Body and a.Nose > a.Tail:                
                    if a.Tail < a.Body:
                        if a1.Up and a1.Open >= max([a.Open,a.Close]) and a1.High >= a.High:
                            aux.append(a)
        return aux


    @property
    def ShootingStar(self):
        aux = []
        for i, r in self.History.iterrows():
            if i>0 and i<len(self.History.index)-1:
                a = Auction(r)
                a_1 = Auction(self.History.iloc[i-1])
                a1 = Auction(self.History.iloc[i+1])
                # if a_1.Up:
                if a.Nose >= 2 * a.Body and a.Nose > a.Tail:                
                    if a.Tail < a.Body:
                        if a1.Open <= min([a.Open,a.Close]) and a1.Close <= a.Close:
                            aux.append(a)
        return aux
    @property
    def HangingMan(self):
        aux = []
        for i, r in self.History.iterrows():
            if i>0 and i<len(self.History.index)-1:
                a = Auction(r)
                a_1 = Auction(self.History.iloc[i-1])
                a1 = Auction(self.History.iloc[i+1])
                # if a_1.Up:
                if a.Tail >= 2 * a.Body and a.Tail > a.Nose:                 
                    if a.Nose < a.Body:
                        if a1.Open <= min([a.Open,a.Close]) and a1.Close <= a.Close:
                            aux.append(a)
        return aux


    @property
    def MorningStar(self):
        aux = []
        for i, r in self.History.iterrows():
            if i>0 and i<len(self.History.index)-1:
                a1 = Auction(self.History.iloc[i-1])
                a2 = Auction(r)
                a3 = Auction(self.History.iloc[i+1])
                if a1.Down and a1.BigBody:
                    if a2.SmallBody and a2.Max <= a1.Min:
                        if a3.Up and a3.Max >= a1.Min: 
                            aux.append(a2)
        return aux      
    @property
    def EveningStar(self):
        aux = []
        for i, r in self.History.iterrows():
            if i>0 and i<len(self.History.index)-1:
                a1 = Auction(self.History.iloc[i-1])
                a2 = Auction(r)
                a3 = Auction(self.History.iloc[i+1])
                if a1.Up and a1.BigBody:
                    if a2.SmallBody and a2.Min <= a1.Max:
                        if a3.Down and a3.Min >= a1.Max: 
                            aux.append(a2)
        return aux


    @property
    def BullishEngulfing(self):
        aux = []
        for i, r in self.History.iterrows():
            if i>0 and i<len(self.History.index)-1:     
                a_1 = Auction(self.History.iloc[i-1])     
                a = Auction(r)
                a1 = Auction(self.History.iloc[i+1])
                if a.Down and a1.Up:
                    #if a.Low < a_1.Low:
                    if a1.Open <= a.Close and a1.Close > a.Open:
                        aux.append(a)
        return aux     
    @property
    def BearishEngulfing(self):
        aux = []
        for i, r in self.History.iterrows():
            if i>0 and i<len(self.History.index)-1:
                a_1 = Auction(self.History.iloc[i-1])
                a = Auction(r)
                a1 = Auction(self.History.iloc[i+1])
                if a.Up and a1.Down:
                    #if a.High > a_1.High:
                    if a1.Close <= a.Open and a1.Open > a.Close:
                        aux.append(a)
        return aux 


    @property
    def Top(self):
        aList = []
        for i, r in self.History.iterrows():
            if i>1 and i<len(self.History.index)-2:  
                a_2 = Auction(self.History.iloc[i-2])
                a_1 = Auction(self.History.iloc[i-1])   
                a = Auction(r)                    
                a1 = Auction(self.History.iloc[i+1])
                a2 = Auction(self.History.iloc[i+2])                   
                if a.High > max(a1.High,a2.High) and a.High > max(a_1.High,a_2.High):
                    aList.append(a)
        return aList
    
    @property
    def Bottom(self):
        aList = []
        for i, r in self.History.iterrows():
            if i>1 and i<len(self.History.index)-2:      
                a_2 = Auction(self.History.iloc[i-2])
                a_1 = Auction(self.History.iloc[i-1])
                a = Auction(r)
                a1 = Auction(self.History.iloc[i+1])      
                a2 = Auction(self.History.iloc[i+2])   
                if a.Low < min(a1.Low,a2.Low) and a.Low < min(a_1.Low,a_2.Low):
                    aList.append(a)
        return aList


    def Multiplier(self, number):
        return 2/(number+1) 
    
    def SMA(self, number): 
        avgDict = dict()
        for i, r in self.History.iterrows():   
            if i>=number-1:         
                avg = 0
                for j in range(i, i-number, -1):
                    a = Auction(self.History.iloc[j])
                    avg += a.Close
                avgDict[r.Date] = avg/number
        return avgDict

    def EMA(self, number):    
        avgDict = dict()
        m = self.Multiplier(number)
        for i, r in self.History.iterrows():
            if i==number-1:            
                avg = 0
                for j in range(i, i-number, -1):
                    a = Auction(self.History.iloc[j])
                    avg += a.Close                    
                avgDict[r.Date] = avg/number
            elif i>number-1:
                EMAy = avgDict[self.History.iloc[i-1].Date]
                at = Auction(r)
                EMAt = (at.Close - EMAy) * m + EMAy
                avgDict[r.Date] = EMAt
        return avgDict

    def MACD(self):
        auxDict = dict()   
        EMA12 = self.EMA(12)
        EMA26 = self.EMA(26)
        for k, v in EMA26.items():
            v26 = v
            v12 = EMA12[k]
            aux = v12-v26
            auxDict[k] = aux
        return auxDict

    def MACD9(self):
        auxDict = dict()
        MACD = self.MACD()
        m = self.Multiplier(9)
        i = 0
        for k, v in MACD.items():
            if i==(9-1):
                auxList = list(MACD.values())[0:9]
                auxDict[k] = sum(auxList)/9
            elif i>(9-1):
                EMAy = list(auxDict.values())[-1]
                MACDt = v
                EMAt = (MACDt - EMAy) * m + EMAy
                auxDict[k] = EMAt
            i += 1            
        return auxDict

    def MACD_diff(self,filter=""):
        auxDict = dict()
        MACD = self.MACD()
        MACD9 = self.MACD9()
        for k, v in MACD9.items():
            aux = MACD9[k] - MACD[k]
            auxDict[k] = aux
        if filter=="+":
            return dict((k, v) for k, v in auxDict.items() if v >= 0) 
        if filter=="-":
            return dict((k, v) for k, v in auxDict.items() if v < 0)
        else:
            return auxDict

    def Variation(self):
        varDict = dict()
        for i, r in self.History.iterrows():
            if i>0:
                a = Auction(r)
                a_1 = Auction(self.History.iloc[i-1])
                var = a.Close - a_1.Close
                varDict[a.Date] = var
        return varDict

    def RSI(self, number=14):
        auxDict = dict()
        Variation = self.Variation()
        i = 0
        for k, v in Variation.items():
            if i>=number-1+1:
                gain, loss, m, n = 0, 0, 0, 0
                for j in range(i, i-number, -1):
                    a = Auction(self.History.iloc[j])
                    var = Variation[a.Date]
                    if var > 0:
                        gain += var
                        m += 1
                    elif var < 0:
                        loss += abs(var)
                        n += 1
                avgGain = gain / m
                avgLoss = loss / n
                if avgLoss == 0:
                    RS = 1.0
                else:
                    RS = avgGain / avgLoss
                RSI = 100 - 100/(1+RS)
                auxDict[k] = RSI
            i += 1
        return auxDict
        
                            
        