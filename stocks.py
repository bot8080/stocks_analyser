import requests
import pandas as pd
import arrow
import datetime
import time

class Stockbot:
  def __init__(self, stock_name, interval):
    self.ohlc = []
    self.error = 0
    self.date = ""
    self.month = ""
    self.setup = ""
    self.interval = interval
    self.stock_name = stock_name
    self.url = 'https://query1.finance.yahoo.com/v8/finance/chart/'

    print(self.stock_name,"", self.interval)

  def date_range_setup(self):
      # 20/12/2020
      startdate = self.date+"/"+self.month+"/"+"2020"
      enddate = str(int(self.date)+1)+"/"+self.month+"/"+"2020"

      startdate = int(time.mktime(datetime.datetime.strptime(startdate,"%d/%m/%Y").timetuple()))
      enddate = int(time.mktime(datetime.datetime.strptime(enddate,"%d/%m/%Y").timetuple())) 

      try:
        self.res = requests.get(self.url+str(self.stock_name)+'?&interval='+str(self.interval)+'&includePrePost=true&events=div%2Csplit&period1='+str(startdate)+'&period2='+str(enddate))
      except Exception as ee:
        print("ERROR BLOCK: 222")
        print(ee)
        
  def default_setup(self):
      self.date_duration = "1d"
      self.res = requests.get(self.url+str(self.stock_name)+'?&interval='+str(self.interval)+'&includePrePost=true&events=div%2Csplit&range='+str(self.date_duration))


  def request_data(self):

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
        print("Error block :request_data 2")
        print(e)

      try:
        self.table = pd.DataFrame(body['indicators']['quote'][0], index=dt)
        dg = pd.DataFrame(body['timestamp'])    
        self.table = self.table.loc[:, ('open', 'high', 'low', 'close', 'volume')]
        self.table.dropna(inplace=True)     #removing NaN rows
        self.table.columns = ['OPEN', 'HIGH','LOW','CLOSE','VOLUME']    #Renaming columns in pandas
      except Exception as e:
        print("Error block :request_data 3")
        print(e)

  def get_ohlc(self):
    self.openn = -99999
    for open_item in self.table['OPEN']:
      self.openn = open_item
      break
      
    self.max_HIGH = -99999
    for item in self.table['HIGH']:
      if item > self.max_HIGH:
        self.max_HIGH = item

    self.min_LOW = 999999
    for item in self.table['LOW']:
      if item < self.min_LOW:
        self.min_LOW = item

    self.sum_candles = self.candles= 0
    self.close = -999999
    for item in self.table['CLOSE']:
      self.sum_candles = item + self.sum_candles
      self.candles = self.candles+1
      self.close = item


  def main(self,setupp,d=0,m=0):
    self.setup = setupp
    # self.startdate = sdate
    # self.enddate = edate
    self.date = d
    self.month = m

    if self.setup == "default":
      self.default_setup()
      self.request_data()

    if self.setup == "date":
      self.date_range_setup()
      self.request_data()

    if str(type(self.error)) == "<class 'str'>":
      return self.error
    else:
      self.get_ohlc()
      print(self.table)

      self.ohlc.extend([self.openn, self.max_HIGH, self.min_LOW, self.close, self.candles, self.sum_candles,self.table])
      return self.ohlc


  # TODAY 
  # OPEN = HIGH   (INDICATE STCK NAME SALE) 
  # OPEN = LOW    (INDICATE STCK NAME BUY) pehli 5m ki candle ke upar
  # INTERVAL 1m
# obj = Stockbot("sbin.ns","1d")
# obj.main()