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

#measurements=[teaspoon, tsp, tablespoon, tbl, tbs, tbsp, "fluid ounce", "fl oz", cup, c, 
#	litre, litre, L, pound, lb, ounce, oz, mg, milligram, gram, g, kg, kilogram, mm, 
#	millimeter, cm, centimeter, m, meter, inch, "in"]

def scrape_ingredients(url):
    webUrl = url
    webFile = urllib.urlopen(webUrl)
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
    webFile = urlopen(webUrl)
    webHtml = webFile.read()
    soup = BeautifulSoup(webHtml,"html.parser")
    webAll = soup.findAll("span", {"class": "recipe-directions__list--item"})
    directions = []
    for description in webAll:
        print (description.string)
        directions.append(description.string)
    return directions
    
def get_quantities(directs):
	quantities =[]
	
	for i in directs:
		p = re.compile(r'([0-9]+)\s?(([./0-9]+)?)')
		#number = re.search("([0-9]+)\s?(([./0-9]+)?))", anything)
		number = p.search(i)
		quantities.append(number.group())
	print (quantities)	
	return quantities

def transformer(list_of_ingredients):
    meat = ['chicken', 'beef', 'pork']
    alt = 'tofu blocks'
    for i in list_of_ingredients:
        for m in meat:
            if m in i:
                #if meat in i: 
                new_ingredient = i.replace(m, alt) #could alsos use re.sub -> regex
                return new_ingredient
            else:
                return i

#get_quantities(scrape_ingredients("https://www.allrecipes.com/recipe/82487/chicken-avocado-pizza/?internalSource=staff%20pick&referringId=1036&referringContentType=recipe%20hub"))
get_quantities(scrape_ingredients("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))
#print(scrape_ingredients("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))
#print(scrape_directions("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))