# from telegram.ext import Updater, InlineQueryHandler, CommandHandler
# import requests
# import re

# def get_url():
#     contents = requests.get('https://random.dog/woof.json').json()    
#     url = contents['url']
#     return url

# def bop(bot, update):
#     url = get_url()
#     chat_id = "-376807218"
#     bot.send_photo(chat_id=chat_id, photo=url)

# def main():
#     updater = Updater('1397494341:AAHlbj8WVMUBr9MxD8eGhBGq2OKC1VE1qGY')
#     dp = updater.dispatcher
#     dp.add_handler(CommandHandler('bop',bop))
#     updater.start_polling()
#     updater.idle()

# if __name__ == '__main__':
#     main()

from telegram.replykeyboardremove import ReplyKeyboardRemove
from telegram.ext.commandhandler import CommandHandler
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from telegram.bot import Bot
import stocks

# initializing an updator
updater = Updater("1397494341:AAHlbj8WVMUBr9MxD8eGhBGq2OKC1VE1qGY",use_context=True)

# getting the dispatcher required to handle the command /start and send message back to the user
dispatcher: Dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    """
    method to handle the /start command and create keyboard
    """

    # defining the keyboard layout
    kbd_layout = [['Option 1', 'Option 2'], ['Option 3', 'Option 4'],["Option 5"]]
    kbd = ReplyKeyboardMarkup(kbd_layout)
    
    # sending the reply so as to activate the keyboard
    update.message.reply_text(text="Select Options", reply_markup=kbd)


def remove(update: Update, context: CallbackContext):
    """
    method to handle /remove command to remove the keyboard and return back to text reply
    """
    reply_markup = ReplyKeyboardRemove()

    # sending the reply so as to remove the keyboard
    update.message.reply_text(text="I'm back.", reply_markup=reply_markup)
    pass


def echo(update: Update, context: CallbackContext):
    print(update.message.text)
    # sending the reply message with the selected option
    update.message.reply_text("You just clicked on '%s'" % update.message.text)
    pass

def stock(update: Update, context: CallbackContext):
    # getting the bot from context
    # documentation: https://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html#telegram-bot
    bot: Bot = context.bot
    stocks.set_values()

    # sending message to the chat from where it has received the message
    # documentation: https://python-telegram-bot.readthedocs.io/en/latest/telegram.bot.html#telegram.Bot.send_message
    bot.send_message(chat_id=update.effective_chat.id,text="enter stock name")



# register a handler (here command handler)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("remove", remove))
updater.dispatcher.add_handler(CommandHandler("stock", stock))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(r"Option [0-9]"), echo))

# starting polling updates from Telegram
# documentation: https://python-telegram-bot.readthedocs.io/en/latest/telegram.ext.updater.html#telegram.ext.Updater.start_polling
updater.start_polling()