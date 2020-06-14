import yfinance as yf
from pandas import DataFrame
from Auction import *


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
            if i<len(self.History.index)-1:
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
            if i<len(self.History.index)-1:
                a = Auction(r)
                a_1 = Auction(self.History.iloc[i-1])
                a1 = Auction(self.History.iloc[i+1])
                # if a_1.Up:
                if a.Tail >= 2 * a.Body and a.Tail > a.Nose:                 
                    if a.Nose < a.Body:
                        if a1.Open <= min([a.Open,a.Close]) and a1.Close <= a.Close:
                            aux.append(a)
        return aux   
                
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

    def MACD_diff(self):
        auxDict = dict()
        MACD = self.MACD()
        MACD9 = self.MACD9()
        for k, v in MACD9.items():
            aux = MACD9[k] - MACD[k]
            auxDict[k] = aux
        return auxDict

    def GetValuesDict(self, property, value="Close"):
        auxList = []
        df = self.History
        valueList = getattr(self,property)
        for i, v in df.iterrows():
            for a in valueList:
                if v["Date"] == a.Date:
                    auxList.append(v)
        auxDict = dict()
        dates = []
        values = []
        for h in auxList:
            dates.append(h["Date"])
            values.append(h[value])
        auxDict["Date"] = dates
        auxDict[value] = values 
        return auxDict

                            
        