import requests
import pandas as pd
import arrow
import datetime
import time

# stock_name = ""
interval = ""
startdate = ""
enddate = ""
temp_date = ""
temp_date2 = ""
time_duration = ""


def set_values(stock_name):
    global interval, startdate, enddate, temp_date, temp_date2, time_duration
    # stock_name = input("Enter Stock name: ")

    # time_duration = input("Enter Time duration (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y , 3y): ")
    time_duration = "1d"
    
    print(stock_name," ", interval)
    # interval = input("Enter Interval (1m, 5m, 60m, 1d, 1mo): ")

    # startdate = "12/10/2020"
    # enddate   = "13/10/2020"
    # temp_date = startdate
    # temp_date2 = enddate

    return stock_name


def get_quote_data(symbol):
    global startdate, enddate, interval
    if interval =="":
        interval = "1m"

    # startdate = int(time.mktime(datetime.datetime.strptime(startdate,"%d/%m/%Y").timetuple()))
    # enddate = int(time.mktime(datetime.datetime.strptime(enddate,"%d/%m/%Y").timetuple()))

    # pd.options.display.max_rows = 2000

    # res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={interval}&period1={start_date}&period2={end_date}&includePrePost=true&events=div%2Csplit'.format(**locals()))
    
    # res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/'+str(symbol)+'?&interval='+str(interval)+'&includePrePost=true&events=div%2Csplit&period1='+str(startdate)+'&period2='+str(enddate)')
    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/'+str(symbol)+'?&interval='+str(interval)+'&includePrePost=true&events=div%2Csplit&range='+str(time_duration))
    
    print(res.url)
    data = res.json()

    try:
        body = data['chart']['result'][0]    
    except:
        # print(data['chart']['error']['code'])
        return data['chart']['error']['description']

    dt = datetime.datetime
    dt = pd.Series(map(lambda x: arrow.get(x).to('Asia/Calcutta').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
    df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
    dg = pd.DataFrame(body['timestamp'])    
    df = df.loc[:, ('open', 'high', 'low', 'close', 'volume')]
    df.dropna(inplace=True)     #removing NaN rows
    df.columns = ['OPEN', 'HIGH','LOW','CLOSE','VOLUME']    #Renaming columns in pandas
    return df


def main(stock_name,interv):
    global interval
    interval = interv
    ohlc = []
    ohlc.clear()

    stock_name = set_values(stock_name)

    data = get_quote_data(stock_name)
    # In case of invalid input
    if str(type(data)) == "<class 'str'>":
        return data
    else:
        print(data)
        min_OPEN = -99999
        for open_item in data['OPEN']:
          min_OPEN = open_item
          break
          
        max_HIGH = -99999
        for item in data['HIGH']:
          if item > max_HIGH:
            max_HIGH = item

        min_LOW = 999999
        for item in data['LOW']:
          if item < min_LOW:
            min_LOW = item

        sum_candles = candles= 0
        close = -999999
        for item in data['CLOSE']:
          sum_candles = item + sum_candles
          candles = candles+1
          close = item

        ohlc.extend([min_OPEN, max_HIGH, min_LOW, close, candles, sum_candles,data])
        return ohlc


# TODAY 
# OPEN = HIGH   (INDICATE STCK NAME SALE) 
# OPEN = LOW    (INDICATE STCK NAME BUY) pehli 5m ki candle ke upar
# INTERVAL 1m