from src.data import top_menu


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!", reply_markup=top_menu)

