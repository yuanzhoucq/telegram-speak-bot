import logging
from configparser import ConfigParser

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from speak import speak
from rmrb import rmrb_news

cfg = ConfigParser()
cfg.read('config')

TOKEN = cfg.get('Bot', 'token')
updater = Updater(token=TOKEN)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!", reply_markup=top_menu)


def echo(bot, update):
    msg = update.message.text.replace('"', "'")
    if msg == '读出聊天信息':
        user_silent[update.message.chat_id] = False
    elif msg == '不读出聊天信息':
        user_silent[update.message.chat_id] = True
    elif msg == '当前状态':
        if not user_silent.get(update.message.chat_id):
            status = '现在会朗读你的消息。'
        else:
            status = '现在不会朗读你的消息。'
        bot.send_message(chat_id=update.message.chat_id, text=status)
    elif msg == '人民日报国际新闻':
        # 清空缓存
        tmp_news.clear()
        news = rmrb_news()
        news_options.clear()
        for item in news:
            title = item['title']
            content = item['content']
            tmp_news[title] = content
            news_options.append(['#'+title])
        news_options.append(['加载更多...', '结束浏览'])
        menu = telegram.ReplyKeyboardMarkup(news_options)
        bot.send_message(chat_id=update.message.chat_id, text="要收听哪条新闻？", reply_markup=menu)
    elif msg == '加载更多...':
        offset = len(tmp_news)
        news = rmrb_news(offset)
        news_options.clear()
        for item in news:
            title = item['title']
            content = item['content']
            tmp_news[title] = content
            news_options.append(['#' + title])
        news_options.append(['加载更多...', '结束浏览'])
        menu = telegram.ReplyKeyboardMarkup(news_options)
        bot.send_message(chat_id=update.message.chat_id, text="要收听哪条新闻？", reply_markup=menu)
    elif msg == '结束浏览':
        bot.send_message(chat_id=update.message.chat_id, text="Bonne lecture !", reply_markup=top_menu)
    elif msg[0] == '#':
        content = tmp_news[msg[1:]]
        menu = telegram.ReplyKeyboardMarkup(news_options)
        bot.send_message(chat_id=update.message.chat_id, text=content, reply_markup=menu)
        speak(content)
    else:
        if not user_silent.get(update.message.chat_id):
            speak(msg)


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


start_handler = CommandHandler('open_keyboard', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)


# 播放聊天信息配置
user_silent = dict()
# 播放新闻
tmp_news = dict()
news_options = []
# 全局辅助键盘
top_menu = telegram.ReplyKeyboardMarkup([['人民日报国际新闻'], ['读出聊天信息'], ['不读出聊天信息'], ['当前状态']])


updater.start_polling()
updater.idle()
