import pandas as pd
from pandas.tseries.offsets import *

maxMarks = 12
today = pd.Timestamp.today()
firstMonth = today + DateOffset(months =- maxMarks +8)
dateList = pd.date_range(firstMonth, periods = maxMarks, freq='M')
dlist = pd.DatetimeIndex(dateList).normalize()
tags = {}
datevalues = {}
x = 1
for i in dlist: 
    tags[x] = (i+DateOffset(months =1)).strftime('%b')
    datevalues[x] = i
    x=x+1