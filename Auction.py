

class Auction:
    """Class that represents an Auction object"""
    def __init__(self, value):
        self.Date = value["Date"]
        self.Open = value["Open"]
        self.Close = value["Close"]
        self.High = value["High"]
        self.Low = value["Low"]

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
    def Up(self):
        return (self.Close > self.Open)


    @property
    def Down(self):
        return (self.Close < self.Open)


    @property
    def Equal(self):
        return (self.Close == self.Open)

