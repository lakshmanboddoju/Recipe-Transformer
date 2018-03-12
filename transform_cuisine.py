from textblob import TextBlob
import nltk
import json
from nltk import ne_chunk, pos_tag, word_tokenize
import string
import re
import pprint
from urllib.request import urlopen
#import urllib
from bs4 import BeautifulSoup
import random
from italiansubstitutes import *
from amer_cheese import *


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


def transform_to_Italian(ingredients): #add salsa, guac, sour cream, chicken/beef, corn tortilla, 

	new_ingredients = []
	replaced = []

	for line in ingredients:
		for item in list(italian_substitutes_dict.keys()):
			if item in line:
				if line.replace(item, italian_substitutes_dict[item]) not in new_ingredients:
					new_ingredients.append(line.replace(item, italian_substitutes_dict[item]))
					replaced.append(line)
					if line in new_ingredients:
						new_ingredients.remove(line)
					break
			else:
				if line not in new_ingredients and line not in replaced:
					new_ingredients.append(line)

	return new_ingredients

def transform_to_American(ingredients): #adds american cheese what else?

	new_ingredients = []
	replaced = []

	for line in ingredients: 
		for item in list(cheeses_dict.keys()):
			if item in line:
				#print(meat_to_vegetarian_dict[item])
				if line.replace(item, cheeses_dict[item]) not in new_ingredients:
					new_ingredients.append(line.replace(item, cheeses_dict[item]))
					replaced.append(line)
					if line in new_ingredients:
						new_ingredients.remove(line)
					break
			else:
				if line not in new_ingredients and line not in replaced:
					new_ingredients.append(line)

	return new_ingredients


test_ingredients = scrape_ingredients('https://www.allrecipes.com/recipe/9044/tomato-chicken-parmesan/?internalSource=streams&referringId=1985&referringContentType=recipe%20hub&clickId=st_trending_s')
test2 = scrape_ingredients('https://www.allrecipes.com/recipe/42579/asiago-sun-dried-tomato-pasta/?internalSource=rotd&referringId=95&referringContentType=recipe%20hub')


print (transform_to_American(test_ingredients)) #issues with parmesan cheese in both of these
print (transform_to_Italian(test_ingredients))
print (transform_to_American(test2))
print (transform_to_Italian(test2))

#