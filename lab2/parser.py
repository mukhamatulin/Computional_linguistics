#!/usr/bin/python
import json
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import datetime
import locale
import re
import sqlite3

base_url = 'https://lenta.ru'
locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")
locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")
c = sqlite3.connect('db')


def parse_news_page(news_url):
    url = base_url + news_url
    if news_exists(news_url):
        return

    resp = requests.get(url)
    news_soup = BeautifulSoup(resp.text, u"lxml")

    posted_at = news_soup.select(u'.b-topic__info .g-date')
    posted_at = posted_at[0].text if len(posted_at) > 0 else None
    if posted_at != None:
        splitted_posted_at = posted_at.split(' ')
        posted_at = ''
        for part in splitted_posted_at:
            if re.match(u'^[а-яё]+$', part):
                part = part[:3]
            posted_at = posted_at + ' ' + part
        posted_at = posted_at.strip()
        posted_at = datetime.datetime.strptime(posted_at, '%H:%M, %d %b %Y')

    title = news_soup.select(u'.b-topic__title')
    title = title[0].text if len(title) > 0 else ''

    topic_rightcol = news_soup.select(u'.b-topic__info .b-topic__rightcol')
    topic_rightcol = topic_rightcol[0].text if len(topic_rightcol) > 0 else ''

    content = news_soup.select(u'.b-topic__content .b-text')
    content = content[0].text if len(content) > 0 else ''
    content = re.sub(u'\nМатериалы по теме.+\n', '', content)
    if posted_at is not None:
        posted_at = posted_at.strftime('%Y-%m-%d %H:%M:%S')
    news = {
        'url': news_url,
        'posted_at': posted_at,
        'title': title,
        'topic_rightcol': topic_rightcol,
        'content': content
    }
    add_news_to_db(news)


def add_news_to_db(news):
    query = "INSERT INTO news (url, posted_at, title, topic_rightcol, content) VALUES (?, ?, ?, ?, ?)"
    cur = c.cursor()
    cur.execute(query, (news['url'], news['posted_at'], news['title'], news['topic_rightcol'], news['content']))
    cur.close()
    c.commit()


def news_exists(url):
    cur = c.cursor()
    cur.execute('SELECT EXISTS(SELECT 1 FROM news WHERE url = ?)', (url,))
    result = cur.fetchone()[0]
    cur.close()
    return result

last_date = datetime.datetime.now()
curr_date = last_date

while (curr_date - last_date).days < 365:
    archive_url = base_url + '/' + '/'.join([str(last_date.year), str(last_date.month), str(last_date.day)])
    resp = requests.get(archive_url)
    archive_soup = BeautifulSoup(resp.text, "lxml")
    archive_items = archive_soup.select('div.item div.titles h3 a[href]')
    for item in archive_items:
        parse_news_page(item['href'])
last_date = last_date - datetime.timedelta(1)
