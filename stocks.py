import requests
import pandas as pd
import arrow
import datetime
import time


class Stockbot:
  def __init__(self, stock_name, interval):
    self.startdate = ""
    self.enddate = ""
    self.ohlc = []
    self.error = 0
    self.time_duration = "1d"

   

    self.stock_name = stock_name
    self.interval = interval

    print(self.stock_name," ", self.interval)

    # stock_name = input("Enter Stock name: ")

    # self.time_duration = input("Enter Time duration (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y , 3y): ")


  def request_data(self):
      if self.interval =="":
          self.interval = "1m"

      # startdate = int(time.mktime(datetime.datetime.strptime(startdate,"%d/%m/%Y").timetuple()))
      # enddate = int(time.mktime(datetime.datetime.strptime(enddate,"%d/%m/%Y").timetuple()))

      # pd.options.display.max_rows = 2000

      # res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{stock_name}?range={data_range}&interval={interval}&period1={start_date}&period2={end_date}&includePrePost=true&events=div%2Csplit'.format(**locals()))
      
      # res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/'+str(stock_name)+'?&interval='+str(interval)+'&includePrePost=true&events=div%2Csplit&period1='+str(startdate)+'&period2='+str(enddate)')
      res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/'+str(self.stock_name)+'?&interval='+str(self.interval)+'&includePrePost=true&events=div%2Csplit&range='+str(self.time_duration))
      
      print(res.url)
      data = res.json()

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


  def main(self):
    self.request_data()
    if str(type(self.error)) == "<class 'str'>":
      return self.error
    else:
      print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
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
