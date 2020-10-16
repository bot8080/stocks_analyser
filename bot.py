# import _thread
# import time

# # Define a function for the thread
# def print_time( threadName, delay):
#    count = 0
#    while count < 4:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# # Create two threads as follows
# try:
#    _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-2", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-3", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-4", 2, ) )
#    _thread.start_new_thread( print_time, ("--------", 2, ) )
#    _thread.start_new_thread( print_time, ("--------", 2, ) )


# except Exception as ss:
#    print (ss)

# print("DONE")

# while 1:
# 	pass

import telebot
import time
import stocks
import os
import requests
from stocks import Stockbot
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

# from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

setup_name = "default"

try:
	bot_token = "1397494341:AAHlbj8WVMUBr9MxD8eGhBGq2OKC1VE1qGY"

	bot = telebot.TeleBot(token=bot_token)

except Exception as pp:
	print(pp)

print("BOT STARTED")

def get_stock_name(message,msg):
  # for text in msg:
    if msg.startswith("@"):
      bot.reply_to(message, "Stock name {}".format(msg))
      return msg[1:]

def get_interval(message,msg):
  for text in msg:
    if text[0].isdigit() or text:
      bot.reply_to(message, "Interval {}".format(text))
      return text


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(messag):
    result, key, step = DetailedTelegramCalendar().process(messag.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",messag.message.chat.id,messag.message.message_id,reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",messag.message.chat.id,messag.message.message_id)

@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "Welcome to patialabot 😇 \nA personal stock 🤖 BOT")


@bot.message_handler(commands=['restart'])
def restart(message):
    os.system('python "C:/Users/angel/Desktop/stocks.py"')
    bot.reply_to(message, "Server restarted.")


@bot.message_handler(commands=['search'])
def search(message):
    try:
      res = requests.get('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='+message.text.split(" ", 1)[1]+'&lang=en')
      bot.reply_to(message, res.json()['ResultSet']['Result'][0]['symbol'])
    except Exception as ee:
      print(ee)
      bot.reply_to(message, "Enter valid company name after /search ")
      pass

@bot.message_handler(commands=['setup_default'])
def default(message):
    global setup_name
    setup_name = "default"

@bot.message_handler(commands=['setup_date'])
def date(message):
    global setup_name
    setup_name = "date"

@bot.message_handler(commands=['help'])
def send_welcome(message):
  bot.reply_to(message, "1. To use this bot, send stock name like this '@SBI.NS 1d' or '@SBIN.NS 1m' or '@SBI.NS 1mo' etc.\n2. search - Search stocks symbol (/search apple) \n3. restart - In case of failure (/restart) \n4. setup - Two setups - Default (for latest date) and Date \n5. help - How to use bot? (/help)")


@bot.message_handler(func=lambda msg: msg.text is not None and ("@" in msg.text or "#" in msg.text))
def at_answer(message):
  global setup_name
  ohlc = []
  ohlc.clear()
  flag = False
  error = False

  input_value = message.text.split(" ")
  # Eg. input_value = ['stock name', 'interval', 'date']
  
  if len(input_value)>1 and len(input_value)<5:
    try:
      stock_name = get_stock_name(message,input_value[0]) 
      obj = Stockbot(stock_name,input_value[1])
      
      print(setup_name)

      if setup_name == "default":
        ohlc = obj.main("default")
        pass

      if setup_name == "date":
        date = input_value[2]
        month = input_value[3]

        # calendar, step = DetailedTelegramCalendar().build()
        # bot.send_message(message.chat.id,f"Select {LSTEP[step]}",reply_markup=calendar)
        
        ohlc = obj.main("date",date,month)

    except Exception as e:
      print(e)
      pass

    # if flag == "True":
    if str(type(ohlc)) == "<class 'str'>":
	    bot.reply_to(message, ohlc)
    else:
	      # ohlc.append(min_OPEN, max_HIGH, min_LOW, close, candles, sum_candles)
	      try:
	        bot.reply_to(message, "OPEN      -> {:.2f}\nHIGH      -> {:.2f}\nLOW       -> {:.2f}\nCLOSE     -> {:.2f}\nTOTAL CANDLES  -> {}".format(ohlc[0], ohlc[1], ohlc[2], ohlc[3], ohlc[4]))
	        bot.reply_to(message, "\nCLOSED MEAN VALUE -> {:.2f}".format(ohlc[5]/ohlc[4]))
	        bot.reply_to(message, "------------{}".format(ohlc[6]))
	        bot.reply_to(message, "-------------------------------------")
	        bot.reply_to(message, setup_name + ": setup")

	      except Exception as ww:
	        print(ww)
	        bot.reply_to(message, "Error: Date format may be wrong")
	        pass
  else:
  	bot.reply_to(message, "Error: Synmbol candles date month (Eg.  SBIN.NS 1d 8 10)")

while True:
  try:
    bot.polling()
  except Exception:
    time.sleep(15)

