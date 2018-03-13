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
from italiansubstitutes import *
from amer_cheese import *
from spices import *
import danparser

def transform_to_Italian(ingredients): #need to get it to only print the ingredients once with the substitutes
									# also only changes the meat, but should be chaning cheese and spice as well
	replace_spice = []
	replace_meat= []
	replace_cheese =[]

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


	for ingredient in ingredients:
		for m in meats:
			if m in ingredient._name:
				print (ingredient._name)
				if ingredient._name not in replace_meat:
					ingredient._name = 'Italian sausage'
					ingredient._descriptor = 'Italian'
					replace_meat.append(ingredient._name)

		for c in cheeses: #having issues with ascii 
			if c in ingredient._name:
				#print (ingredient._name)
				if ingredient._name not in replace_cheese:
					ingredient._name = 'mozzarella cheese'
					ingredient._descriptor = 'n/a'
					replace_cheese.append(ingredient._name)	

		for s in spices:
			if s in ingredient._name:

				if ingredient._name not in replace_spice:
					ingredient._name = 'basil'
					ingredient._descriptor = 'leaves'
					replace_spice.append(ingredient._name)


	return ingredients

def transform_to_American(ingredients):
	
	cheeses = []
	cheese_text = open("cheeses.txt", "r")
	cheese_lines = cheese_text.readlines()
	for c in cheese_lines:
		temp = c.rstrip('\n')
		cheeses.append(str(temp.lower()))	

	replace_cheese = []
	replace_spice = []

	for ingredient in ingredients:
		for s in ingredient._name:
			if ingredient._name not in replace_spice:
				ingredient._name = 'black pepper'
				ingredient._descriptor = 'black'
				replace_spice.append(ingredient._name)

		for c in ingredient._name: #having issues with ascii 
			if ingredient._name not in replace_cheese:
				ingredient._name = 'American cheese'
				ingredient._descriptor = 'n/a'
				replace_cheese.append(ingredient._name)

		return ingredients



#print (transform_to_Italian(danparser.ingredient_info('https://www.allrecipes.com/recipe/9044/tomato-chicken-parmesan/?internalSource=streams&referringId=1985&referringContentType=recipe%20hub&clickId=st_trending_s')))

