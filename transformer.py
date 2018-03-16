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
import danparser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def transform_to_Italian(ingredients): #need to get it to only print the ingredients once with the substitutes
								
	non_italian_spices = ['cayenne pepper', 'fennel', 'cilantro', 'saffron', 'turmeric', 'ghee', 'garlic', 'ginger', 'curry powder', 'garam masala', 'cumin', 'masala', 'coriander', 'cilantro', 'mustard seeds', 'chilli pepper','garlic', 'ginger', 'curry powder', 'garam masala', 'cumin', 'masala', 'coriander', 'cilantro', 'mustard seeds', 'chilli pepper']

	replacement = []
	basil = 'basil'
	oregano = 'oregano'
	parmesan = 'parmesan cheese'

	meats = []
	meat_text = open("meats.txt", "r")
	meat_lines = meat_text.readlines()
	for m in meat_lines:
		temp = m.rstrip('\n')
		meats.append(str(temp.lower()))

	cheeses = []
	cheese_text = open("cheeses.txt", "r")
	cheese_lines = cheese_text.readlines()
	for c in cheese_lines:
		temp = c.rstrip('\n')
		cheeses.append(str(temp.lower()))

	removed_spices = []
	for ingredient in ingredients:
		for spice in non_italian_spices:
			if spice in ingredient._name and spice not in removed_spices:
				removed_spices.append(spice)
				ingredients.remove(ingredient)


	for ingredient in ingredients: #returns ingredient info with and without changes
		for m in meats:
			if m in ingredient._name:
				#print (ingredient._name)
				if ingredient._name not in replacement:
					ingredient._name = 'Italian sausage'
					ingredient._descriptor = 'Italian'
					replacement.append(ingredient._name)

		for c in cheeses: #having issues with ascii 
			if c in ingredient._name:
				#print (ingredient._name)
				if ingredient._name not in replacement:
					ingredient._name = 'mozzarella cheese'
					ingredient._descriptor = 'n/a'
					replacement.append(ingredient._name)	

	for ingredient in ingredients:
		if basil not in ingredient._name:
			new_ingredient = danparser.Ingredient()
			new_ingredient._name = 'basil'
			new_ingredient._quantity = '1'
			new_ingredient._measurement = 'teaspoon'
			new_ingredient._preparation = 'n/a'
			new_ingredient._descriptor = 'dried'
			ingredients.append(new_ingredient)


		if oregano not in ingredient._name:
			new_ingredient = danparser.Ingredient()
			new_ingredient._name = 'oregano'
			new_ingredient._quantity = '1'
			new_ingredient._measurement = 'teaspoon'
			new_ingredient._preparation = 'n/a'
			new_ingredient._descriptor = 'dried'
			ingredients.append(new_ingredient)

		if parmesan not in ingredient._name:
			new_ingredient = danparser.Ingredient()
			new_ingredient._name = 'parmesan cheese'
			new_ingredient._quantity = '2'
			new_ingredient._measurement = 'tablespoon'
			new_ingredient._preparation = 'n/a'
			new_ingredient._descriptor = 'n/a'
			ingredients.append(new_ingredient)		


	# for ingredient in ingredients:
	# 	for spice in non_italian_spices:
	# 		if spice._name in ingredient:
	# 			ingredient.remove(spice)			

		return ingredients




	return ingredients

def transform_to_American(ingredients):
	
	non_american_spices = ['cayenne pepper', 'fennel', 'cilantro', 'saffron', 'turmeric', 'ghee', 'garlic', 'ginger', 'curry powder', 'garam masala', 'cumin', 'masala', 'coriander', 'cilantro', 'mustard seeds', 'chilli pepper','garlic', 'ginger', 'curry powder', 'garam masala', 'cumin', 'masala', 'coriander', 'cilantro', 'mustard seeds', 'chilli pepper']

	cheeses = []
	cheese_text = open("cheeses.txt", "r")
	cheese_lines = cheese_text.readlines()
	for c in cheese_lines:
		temp = c.rstrip('\n')
		cheeses.append(str(temp.lower()))	

	replace_cheese = []
	replace_spice = []
	b = 'black pepper'

	removed_spices = []
	for ingredient in ingredients:
		for spice in non_american_spices:
			if spice in ingredient._name and spice not in removed_spices:
				removed_spices.append(spice)
				ingredients.remove(ingredient)

	for ingredient in ingredients:
		for c in cheeses:
			if c in ingredient._name: #having issues with ascii 
				if ingredient._name not in replace_cheese:
					ingredient._name = 'American cheese'
					ingredient._descriptor = 'n/a'
					replace_cheese.append(ingredient._name)

	for ingredient in ingredients:
		if b not in ingredient._name:
			new_ingredient = danparser.Ingredient()
			new_ingredient._name = 'black pepper'
			new_ingredient._quantity = '1'
			new_ingredient._measurement = 'teaspoon'
			new_ingredient._preparation = 'n/a'
			new_ingredient._descriptor = 'black'
			ingredients.append(new_ingredient)

		return ingredients


def scrape_recipe_name(url):
	webUrl = url
	webFile = urllib.urlopen(webUrl)
	webHtml = webFile.read()
	soup = BeautifulSoup(webHtml,"html.parser")
	webAll = soup.find("h1", {"class": "recipe-summary__h1"})
	name = webAll.string
	return name


def make_easy(recipe_name):
	#for every character
	recipe_name.replace(" ", "%20")

	full_url = "https://www.grubhub.com/search?orderMethod=delivery&locationMode=DELIVERY&facetSet=umamiV2&pageSize=20&hideHateos=true&searchMetrics=true&queryText="+recipe_name+"&latitude=41.87811279&longitude=-87.62979889&facet=open_now%3Atrue&variationId=default-impressionScoreBaseBuffed-20160317&sortSetId=umamiV2&sponsoredSize=2&countOmittingTimes=true"
	#%20
	return full_url

print (make_easy(scrape_recipe_name('https://www.allrecipes.com/recipe/9044/tomato-chicken-parmesan/?internalSource=streams&referringId=1985&referringContentType=recipe%20hub&clickId=st_trending_s')))

#print(transform_to_American(danparser.ingredient_info('https://www.allrecipes.com/recipe/9044/tomato-chicken-parmesan/?internalSource=streams&referringId=1985&referringContentType=recipe%20hub&clickId=st_trending_s')))

#print(transform_to_Italian(danparser.ingredient_info('https://www.allrecipes.com/recipe/9044/tomato-chicken-parmesan/?internalSource=streams&referringId=1985&referringContentType=recipe%20hub&clickId=st_trending_s')))
##

#