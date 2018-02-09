import requests
import xml.etree.ElementTree as ET
import re


def rmrb_news(start=0):
    response = requests.get('http://www.people.com.cn/rss/world.xml')
    root = ET.fromstring(response.content)
    items = root.iter('item')
    news = []
    for i in range(start):
        next(items)
    for i in range(3):
        item = next(items)
        title = item.find('title').text
        title = str(i + 1 + start) + ' ' + title
        content = item.find('description').text
        content = re.sub('<.+?>', '', content)  # todo remove the codes like &nbsp;
        news.append({'title': title, 'content': content})
    return news
