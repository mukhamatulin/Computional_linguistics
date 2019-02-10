#!/usr/bin/python
import nltk
import requests
from bs4 import BeautifulSoup
from nltk.stem.snowball import RussianStemmer

from index import Index

base_url = 'http://lit.lib.ru'


def parse_genre(genre_url, genre_name):
    resp = requests.get(genre_url)
    genre_soup = BeautifulSoup(resp.text, u"lxml")
    text_links_tags = genre_soup.select('dd > dl > dt > li > a:nth-of-type(2)')
    count = 0
    for text_tag in text_links_tags:
        text_url = base_url + text_tag.get('href')
        text_name = text_tag.text
        resp_text = requests.get(text_url)
        text_soup = BeautifulSoup(resp_text.text, u"lxml")
        text = text_soup.text
        index.add(text_url, text)
        print(text_url)
        count += 1
        if count == 5:
            break
    search_query = input()
    print(index.lookup(search_query))
    exit(0)


index = Index(nltk.word_tokenize,
              RussianStemmer(),
              nltk.corpus.stopwords.words('russian'))
resp = requests.get(base_url)
main_soup = BeautifulSoup(resp.text, u"lxml")
genre_tags = main_soup.select('table[align="right"] > tr:nth-of-type(2) > td:nth-of-type(1) > a')
for tag in genre_tags:
    genre_url = base_url + tag.get('href')
    genre_name = tag.text
    parse_genre(genre_url, genre_name)
