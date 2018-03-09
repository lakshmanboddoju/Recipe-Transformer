from textblob import TextBlob
import nltk
import json
from nltk import ne_chunk, pos_tag, word_tokenize
import string
import re
import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random

def scrape_recipe_name(url):
	webUrl = url
	webFile = urlopen(webUrl)
	webHtml = webFile.read()
	soup = BeautifulSoup(webHtml,"html.parser")
	webAll = soup.find("h1", {"class": "recipe-summary__h1"})
	name = webAll.string
	return name

def scrape_ingredients(url):
	webUrl = url
	webFile = urlopen(webUrl)
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
		#print (description.string)
		directions.append(description.string)
	return directions

#print("\nRecipe: \n\n", scrape_recipe_name("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))
#print("\nIngredients:\n\n", scrape_ingredients("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))
#print("\nDirections:\n\n", scrape_directions("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))

meat_to_vegetarian_dict = {'chicken breasts': 'paneer', 'chicken': 'paneer', 'beef': 'paneer', 'turkey': 'paneer', 'fish': 'paneer'}
meat_to_vegan_dict = {'chicken breasts': 'tofu', 'chicken breast': 'tofu', 'chicken': 'tofu', 'beef': 'tofu', 'turkey': 'tofu', 'fish': 'tofu', 'pork butt': 'tofu', 'pork': 'tofu'}
#print (meat_to_vegan_dict['chicken'])
#print(meat_to_vegetarian_dict['chicken'])

def make_vegetarian(ingredients):
	new_ingredients = []
	replaced = []
	for line in ingredients:
		for item in list(meat_to_vegetarian_dict.keys()):
			if item in line:
				#print(meat_to_vegetarian_dict[item])
				if line.replace(item, meat_to_vegetarian_dict[item]) not in new_ingredients:
					new_ingredients.append(line.replace(item, meat_to_vegetarian_dict[item]))
					replaced.append(line)
					new_ingredients.remove(line)
			else:
				if line not in new_ingredients and line not in replaced:
					new_ingredients.append(line)

	return new_ingredients

def make_vegan(ingredients):
	new_ingredients = []
	replaced = []
	for line in ingredients:
		for item in list(meat_to_vegan_dict.keys()):
			if item in line:
				#print(meat_to_vegetarian_dict[item])
				if line.replace(item, meat_to_vegan_dict[item]) not in new_ingredients:
					new_ingredients.append(line.replace(item, meat_to_vegan_dict[item]))
					replaced.append(line)
					if line in new_ingredients:
						new_ingredients.remove(line)
					break
			else:
				if line not in new_ingredients and line not in replaced:
					new_ingredients.append(line)

	return new_ingredients







#print("\n\n", scrape_ingredients("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/"))
#print("\n\n", make_vegan(scrape_ingredients("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")))

print("\n\n", scrape_ingredients("https://www.allrecipes.com/recipe/239786/crispy-pork-carnitas/"))
print("\n\n", make_vegan(scrape_ingredients("https://www.allrecipes.com/recipe/239786/crispy-pork-carnitas/")))

