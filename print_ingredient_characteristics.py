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

#measurements=[teaspoon, tsp, tablespoon, tbl, tbs, tbsp, "fluid ounce", "fl oz", cup, c, 
#	litre, litre, L, pound, lb, ounce, oz, mg, milligram, gram, g, kg, kilogram, mm, 
#	millimeter, cm, centimeter, m, meter, inch, "in"]


#find a way to put all the functions of get items together with classes

def scrape_ingredients(url):
    webUrl = url
    webFile = urllib.urlopen(webUrl) #edited for me
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
    webFile = urllib.urlopen(webUrl) #edited for me
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

def get_name(directs):
	return

def get_measurements(directs):
	# measurements = []

	# for i in directs:
	# 	p = re.compile(r'([0-9]+)\s?(([./0-9]+)?) ([A-Za-z]*)')
	# 	m = p.search(i)
	# 	measurements.append(m.group(1))
	# print (measurements)
	# return measurements

def get_descriptor(directs):
	return

def get_preparation(directs):
	return

def get_tools(directs):

def print_all(directs):

def get_cooking_method(directs):
	#roast, bake, saute


test_ingredients = ['chicken breast', 'salt', 'pepper', 'tomatoes', 'peppers'] # test b/c haven't parsed actual ingredients yet

def meat_transformer(list_of_ingredients): #simple meat transformer

	alt = ['tofu', 'tempeh', 'seitan', 'mushrooms', 'eggplant'] #need actual vegetarian options, this is just a test
	meat_ingredient = []
	replacement = random.choice(alt)

	#turns meat.txt into list of strings of the meats
	meat_list = []
	meat_txt = open('meats.txt', 'r')
	meat_line = meat_txt.readlines()
	for m in meat_line:
		temp = m.rstrip('\n')
		meat_list.append(str(temp.lower()))

		#replaces meat ingredient with vegetarian ingredient
		for i in list_of_ingredients:
			if i in meat_list:
				list_of_ingredients[list_of_ingredients.index(i)] = replacement
				return list_of_ingredients


scraped_ingredients = scrape_ingredients("https://www.allrecipes.com/recipe/42579/asiago-sun-dried-tomato-pasta/?internalSource=rotd&referringId=95&referringContentType=recipe%20hub")
#print_all(scraped_ingredients)

get_measurements(scraped_ingredients)

#get_quantities(scrape_ingredients("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))

#get_quantities(scrape_ingredients("https://www.allrecipes.com/recipe/42579/asiago-sun-dried-tomato-pasta/?internalSource=rotd&referringId=95&referringContentType=recipe%20hub"))

#print (meat_transformer(scraped_ingredients))

#print(scrape_ingredients("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))
#print(scrape_directions("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))