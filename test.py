import telebot
import config
import pb
import datetime
import pytz
import json
import traceback

P_TIMEZONE = pytz.timezone(config.TIMEZONE)
TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME

TOKEN = "1397494341:AAHlbj8WVMUBr9MxD8eGhBGq2OKC1VE1qGY"

bot = telebot.TeleBot(config.TOKEN)
bot.polling(none_stop=True)

@bot.message_handler(commands=['start'])
def start_command(message):
   bot.send_message(
       message.chat.id,
       'Greetings! I can show you PrivatBank exchange rates.\n' +
       'To get the exchange rates press /exchange.\n' +
       'To get help press /help.'
   )