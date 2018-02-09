import logging
from configparser import ConfigParser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from handle_functions.echo import echo
from handle_functions.start import start

cfg = ConfigParser()
cfg.read('config')
TOKEN = cfg.get('Bot', 'token')
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


start_handler = CommandHandler('open_keyboard', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

