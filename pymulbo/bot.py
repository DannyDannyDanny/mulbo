from config import telegram_token, logging_format
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
print("test")

updater = Updater(token=telegram_token)
dispatcher = updater.dispatcher

logging.basicConfig(filename='example.log',
                    format=logging_format,
                    level=logging.INFO)
logger = logging.getLogger()
logging.info('starting machine')


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    logging.info('starting machine')


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


updater.stop()
updater.start_polling()
updater.idle()
