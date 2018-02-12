import telegram

# 播放聊天信息配置
user_silent = dict()
# 播放新闻
tmp_news = dict()
news_options = []
# 全局辅助键盘
top_menu = telegram.ReplyKeyboardMarkup([['人民日报国际新闻'], ['开灯', '关灯'], ['读出聊天信息', '不读出聊天信息'], ['当前状态']])