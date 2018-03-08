from textblob import TextBlob
import nltk
import json
from nltk import ne_chunk, pos_tag, word_tokenize
import string
import re
import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup



def scrape_ingredients(url):
    webUrl = url
    webFile = urlopen(webUrl)
    webHtml = webFile.read()
    soup = BeautifulSoup(webHtml,"html.parser")
    webAll = soup.findAll('th')
        #"th", {"scope": "row"})
        #"label", {"ng-class": "{true: 'checkList__item'}[true]"})
    ingredients = []
    for item in webAll:
        print (item.text)
        #ingredients.append(item['title'])
    return ingredients


scrape_ingredients("https://en.wikipedia.org/wiki/List_of_food_preparation_utensils")