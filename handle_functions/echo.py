import telegram
import requests
from src.speak import speak
from src.rmrb import rmrb_news
from src.data import user_silent, tmp_news, news_options, top_menu


class CommandLists:
    read_news = "读出聊天信息"
    do_not_read_news = "不读出聊天信息"
    get_status = "当前状态"
    read_renminribao = "人民日报国际新闻"
    turn_on_light = "开灯"
    turn_off_light = "关灯"


def echo(bot, update):
    msg = update.message.text.replace('"', "'")
    if msg == CommandLists.read_news:
        user_silent[update.message.chat_id] = False
    elif msg == CommandLists.do_not_read_news:
        user_silent[update.message.chat_id] = True
    elif msg == CommandLists.get_status:
        if not user_silent.get(update.message.chat_id):
            status = '现在会朗读你的消息。'
        else:
            status = '现在不会朗读你的消息。'
        bot.send_message(chat_id=update.message.chat_id, text=status)
    elif msg == CommandLists.turn_on_light:
        requests.get("https://maker.ifttt.com/trigger/ouvrir_l'ampoule/with/key/dV_L-I4SuFsBUNn-So3JNh")
    elif msg == CommandLists.turn_off_light:
        requests.get("https://maker.ifttt.com/trigger/eteindre_l'ampoule/with/key/dV_L-I4SuFsBUNn-So3JNh")
    elif msg == CommandLists.read_renminribao:
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
