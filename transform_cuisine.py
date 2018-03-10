from textblob import TextBlob
import nltk
import json
from nltk import ne_chunk, pos_tag, word_tokenize
import string
import re
import pprint
#from urllib.request import urlopen
import urllib
from bs4 import BeautifulSoup
import random

def scrape_ingredients(url):
    webUrl = url
    webFile = urlopen(webUrl) #edited for me
    webHtml = webFile.read()
    soup = BeautifulSoup(webHtml,"html.parser")
    webAll = soup.findAll("label", {"ng-class": "{true: 'checkList__item'}[true]"})
    ingredients = []
    for item in webAll:
        #print (item['title']) 
        ingredients.append(item['title'])
    return ingredients
    
def scrape_directions(url):
    webUrl = url
    webFile = urlopen(webUrl) #edited for me
    webHtml = webFile.read()
    soup = BeautifulSoup(webHtml,"html.parser")
    webAll = soup.findAll("span", {"class": "recipe-directions__list--item"})
    directions = []
    for description in webAll:
        print (description.string)
        directions.append(description.string)
    return directions

 def to_Mexican(ingredients): #add salsa, guac, sour cream, chicken/beef, corn tortilla, 



 test_ingredients = ("https://www.allrecipes.com/recipe/235151/crispy-and-tender-baked-chicken-thighs/")