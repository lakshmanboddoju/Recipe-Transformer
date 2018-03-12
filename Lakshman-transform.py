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
import danparser
from fractions import Fraction

unhealthy_list = ['ghee', 'oil', 'butter', 'salt', 'sugar', 'fat']

def make_healthy(ingredients):
	replaced = []
	for ingredient in ingredients:
		for unhealthy_item in unhealthy_list:
			if unhealthy_item in ingredient._name:
				print (unhealthy_item)
				if ingredient._quantity != 'n/a' and ingredient._name not in replaced:
					ingredient._quantity = 0.5 * float(sum(Fraction(s) for s in ingredient._quantity.split()))
					replaced.append(ingredient._name)
	return ingredients

#print(make_healthy(LakshmanParser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")))



def make_vegetarian(ingredients):
	replaced = []
	meat_list = []
	meat_txt = open('meats.txt', 'r')
	meat_line = meat_txt.readlines()
	for m in meat_line:
		temp = m.rstrip('\n')
		meat_list.append(str(temp.lower()))

	for ingredient in ingredients:
		for meat_item in meat_list:
			if meat_item in ingredient._name:
				print (ingredient._name)
				if ingredient._name not in replaced:
					ingredient._name = 'Paneer'
					ingredient._descriptor = 'n/a'
					replaced.append(ingredient._name)
	return ingredients

def make_indian(ingredients):
	replaced = []
	

print(make_vegetarian(LakshmanParser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")))
