import telebot
import time
import stocks
import os
import requests
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

bot_token = "1397494341:AAHlbj8WVMUBr9MxD8eGhBGq2OKC1VE1qGY"
bot = telebot.TeleBot(token=bot_token)
print("BOT STARTED")

def get_stock_name(message,msg):
  for text in msg:
    if text.startswith("@"):
      bot.reply_to(message, "Stock name {}".format(text[1:]))
      return text[1:]


def get_interval(message,msg):
  for text in msg:
    if text[0].isdigit():
      bot.reply_to(message, "Interval {}".format(text))
      return text


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(message, "Welcome to patialabot 😇 \n A personal stock 🤖 BOT")


@bot.message_handler(commands=['restart'])
def restart(message):
    os.system('python "C:/Users/abhik/Desktop/stocks/bot/stocks.py"')
    bot.reply_to(message, "Server restarted.")


@bot.message_handler(commands=['search'])
def search(message):
    try:
      res = requests.get('http://d.yimg.com/autoc.finance.yahoo.com/autoc?query='+message.text.split(" ", 1)[1]+'&lang=en')
      bot.reply_to(message, res.json()['ResultSet']['Result'][0]['symbol'])
    except Exception as ee:
      print(ee)
      bot.reply_to(message, "Enter Company name after /search ")


@bot.message_handler(commands=['help'])
def send_welcome(message):
  bot.reply_to(message, "To use this bot, send stock name like this '@SBI.NS 1d' or '@SBIN.NS 1m' or '@SBI.NS 1mo' etc.")


@bot.message_handler(func=lambda msg: msg.text is not None and ("@" in msg.text))
def at_answer(message):
  ohlc = []
  ohlc.clear()
  stock = message.text.split(" ")
  stock_name = get_stock_name(message,stock)
  ohlc = stocks.main(stock_name, stock[1])

  if str(type(ohlc)) == "<class 'str'>":
    bot.reply_to(message, ohlc)

  # ohlc.append(min_OPEN, max_HIGH, min_LOW, close, candles, sum_candles)
  try:
    bot.reply_to(message, "OPEN      -> {:.2f}\nHIGH      -> {:.2f}\nLOW       -> {:.2f}\nCLOSE     -> {:.2f}\nTOTAL CANDLES  -> {}".format(ohlc[0], ohlc[1], ohlc[2], ohlc[3], ohlc[4]))
    bot.reply_to(message, "\nCLOSED MEAN VALUE -> {:.2f}".format(ohlc[5]/ohlc[4]))
    bot.reply_to(message, "------------{}".format(ohlc[6]))
    bot.reply_to(message, )

  except Exception as ww:
    print(ww)


while True:
  try:
    bot.polling()
  except Exception:
    time.sleep(15)

