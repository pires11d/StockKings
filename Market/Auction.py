

class Auction:
    """Class that represents an Auction object"""
    def __init__(self, entry):
        self.Date = entry["Date"]
        self.Open = entry["Open"]
        self.Close = entry["Close"]
        self.High = entry["High"]
        self.Low = entry["Low"]
        self.Volume = entry["Volume"]
        self.AdjClose = entry["Adj Close"]

    @property
    def Nose(self):
        return self.High - max([self.Open, self.Close])

    @property
    def Body(self):
        return abs(self.Open - self.Close)   

    @property
    def Tail(self):
        return min([self.Open, self.Close]) - self.Low                        

    @property
    def BigBody(self):
        return self.Body > self.Nose + self.Tail

    @property
    def SmallBody(self):
        return self.Body <= self.Nose + self.Tail

    @property
    def Up(self):
        return (self.Close > self.Open)                  

    @property
    def Down(self):
        return (self.Close < self.Open)                  

    @property
    def Equal(self):
        return (self.Close == self.Open)

    @property
    def Max(self):
        return max([self.Open, self.Close])

    @property
    def Min(self):
        return min([self.Open, self.Close])

    @property
    def Avg(self):
        return (self.Open + self.Close) / 2

