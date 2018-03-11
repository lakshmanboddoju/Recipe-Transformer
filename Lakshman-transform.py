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
import LakshmanParser
from fractions import Fraction

unhealthy_list = ['ghee', 'oil', 'butter', 'salt', 'sugar', 'fat']

def make_healthy(ingredients):
	new_ingredients = []
	replaced = []
	for ingredient in ingredients:
		for unhealthy_item in unhealthy_list:
			if unhealthy_item in ingredient._name:
				print (unhealthy_item)
				if ingredient._quantity != 'n/a' and ingredient._name not in replaced:
					ingredient._quantity = 0.5 * float(sum(Fraction(s) for s in ingredient._quantity.split()))
					replaced.append(ingredient._name)
	return ingredients

print(make_healthy(LakshmanParser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")))
