import requests
import pandas as pd
import arrow
import datetime
import time


class Stockbot:
  def __init__(self, stock_name, interval):
    self.ohlc = []
    self.error = 0
    self.startdate = ""
    self.enddate = ""
    self.setup = ""
    self.interval = interval
    self.stock_name = stock_name
    self.url = 'https://query1.finance.yahoo.com/v8/finance/chart/'

    print(self.stock_name,"", self.interval)


    # stock_name = input("Enter Stock name: ")

    # self.date_duration = input("Enter Time duration (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y , 3y): ")

  def date_range_setup(self):
      self.startdate = int(time.mktime(datetime.datetime.strptime(self.startdate,"%d/%m/%Y").timetuple()))
      self.enddate = int(time.mktime(datetime.datetime.strptime(self.enddate,"%d/%m/%Y").timetuple())) 
      self.res = requests.get(self.url+str(self.stock_name)+'?&interval='+str(self.interval)+'&includePrePost=true&events=div%2Csplit&period1='+str(self.startdate)+'&period2='+str(self.enddate))

  def default_setup(self):
      self.date_duration = "1d"
      self.res = requests.get(self.url+str(self.stock_name)+'?&interval='+str(self.interval)+'&includePrePost=true&events=div%2Csplit&range='+str(self.date_duration))


  def request_data(self):
      if self.interval =="":
        self.interval = "1m"

      # pd.options.display.max_rows = 2000

      print(self.res.url)
      data = self.res.json()

      try:
        body = data['chart']['result'][0]    
      except:
        # print(data['chart']['error']['code'])
        self.error = data['chart']['error']['description']
        return

      try:
        dt = datetime.datetime
        dt = pd.Series(map(lambda x: arrow.get(x).to('Asia/Calcutta').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
      except Exception as e:
        print(e)

      self.table = pd.DataFrame(body['indicators']['quote'][0], index=dt)
      dg = pd.DataFrame(body['timestamp'])    
      self.table = self.table.loc[:, ('open', 'high', 'low', 'close', 'volume')]
      self.table.dropna(inplace=True)     #removing NaN rows
      self.table.columns = ['OPEN', 'HIGH','LOW','CLOSE','VOLUME']    #Renaming columns in pandas


  def main(self,setupp,sdate=0,edate=0):
    self.setup = setupp
    self.startdate = sdate
    self.enddate = edate

    if self.setup == "default":
      self.default_setup()
    if self.setup == "date":
      self.date_range_setup()

    self.request_data()

    if str(type(self.error)) == "<class 'str'>":
      return self.error
    else:
      print(self.table)
      min_OPEN = -99999
      for open_item in self.table['OPEN']:
        min_OPEN = open_item
        break
        
      max_HIGH = -99999
      for item in self.table['HIGH']:
        if item > max_HIGH:
          max_HIGH = item

      min_LOW = 999999
      for item in self.table['LOW']:
        if item < min_LOW:
          min_LOW = item

      sum_candles = candles= 0
      close = -999999
      for item in self.table['CLOSE']:
        sum_candles = item + sum_candles
        candles = candles+1
        close = item

      self.ohlc.extend([min_OPEN, max_HIGH, min_LOW, close, candles, sum_candles,self.table])
      return self.ohlc


  # TODAY 
  # OPEN = HIGH   (INDICATE STCK NAME SALE) 
  # OPEN = LOW    (INDICATE STCK NAME BUY) pehli 5m ki candle ke upar
  # INTERVAL 1m
# obj = Stockbot("sbin.ns","1d")
# obj.main()