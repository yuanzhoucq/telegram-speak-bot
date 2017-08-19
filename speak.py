import os
from urllib.parse import quote


def speak(text):
    text_encoded = quote(text)
    with open("baiduyuyin_token.txt", "r") as f:
        token = f.read()
    voice_url = "http://tsn.baidu.com/text2audio?tex=" + text_encoded + "&lan=zh&per=0&cuid=784f436aa242&ctp=1&tok=" + token
    os.system('mpg123 "%s"' % voice_url)
