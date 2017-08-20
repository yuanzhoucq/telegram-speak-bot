import requests
import xml.etree.ElementTree as ET
import re


def rmrb_news():
    response = requests.get('http://www.people.com.cn/rss/world.xml')
    root = ET.fromstring(response.content)
    items = root.iter('item')
    news = []
    for i in range(3):
        item = next(items)
        title = item.find('title').text
        title = str(i+1) + ' ' + title
        content = item.find('description').text
        content = re.sub('<.+?>', '', content)
        news.append({'title': title, 'content': content})
    return news
