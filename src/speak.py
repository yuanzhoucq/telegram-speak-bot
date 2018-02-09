import os
from urllib.parse import quote
import requests


def speak(text):
    # get token
    try:
        with open("baiduyuyin_token.txt", "r") as f:
            token = f.read()
    except FileNotFoundError:
        token = requests.get("https://ilangbd.azurewebsites.net/token.txt").text

    voice_url = "http://tsn.baidu.com/text2audio?tex={0}&lan=zh&per=0&cuid=784f436aa242&ctp=1&tok={1}"  \
        .format(quote(text), token)
    os.system('mpg123 -q "%s"' % voice_url)
