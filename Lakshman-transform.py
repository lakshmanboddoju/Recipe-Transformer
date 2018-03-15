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
			if unhealthy_item in ingredient._name.lower():
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
			if meat_item in ingredient._name.lower():
				print (ingredient._name)
				if ingredient._name not in replaced:
					ingredient._name = 'Paneer'
					ingredient._descriptor = 'n/a'
					replaced.append(ingredient._name)
	return ingredients

indian_list = []
indian_ing_1 = danparser.Ingredient()
indian_ing_1._name = 'garlic'
indian_ing_1._preperation = 'paste'
indian_ing_1._quantity = ''
indian_ing_1._descriptor = ["n/a"]
indian_list.append(indian_ing_1)

indian_ing_2 = danparser.Ingredient()
indian_ing_2._name = 'ginger'
indian_ing_2._preperation = 'paste'
indian_ing_2._quantity = ''
indian_ing_2._descriptor = ["n/a"]
indian_list.append(indian_ing_2)

indian_ing_3 = danparser.Ingredient()
indian_ing_3._name = 'curry powder'
indian_ing_3._preperation = 'n/a'
indian_ing_3._quantity = ''
indian_ing_3._descriptor = ["n/a"]
indian_list.append(indian_ing_3)

indian_ing_4 = danparser.Ingredient()
indian_ing_4._name = 'garam masala'
indian_ing_4._preperation = 'n/a'
indian_ing_4._quantity = ''
indian_ing_4._descriptor = ["n/a"]
indian_list.append(indian_ing_4)

indian_ing_5 = danparser.Ingredient()
indian_ing_5._name = 'cumin'
indian_ing_5._preperation = 'n/a'
indian_ing_5._quantity = ''
indian_ing_5._descriptor = ["n/a"]
indian_list.append(indian_ing_5)

indian_ing_6 = danparser.Ingredient()
indian_ing_6._name = 'coriander'
indian_ing_6._preperation = 'leaves'
indian_ing_6._quantity = ''
indian_ing_6._descriptor = ["n/a"]
indian_list.append(indian_ing_6)

indian_ing_7 = danparser.Ingredient()
indian_ing_7._name = 'mustard seeds'
indian_ing_7._preperation = 'n/a'
indian_ing_7._quantity = ''
indian_ing_7._descriptor = ["black"]
indian_list.append(indian_ing_7)

indian_ing_8 = danparser.Ingredient()
indian_ing_8._name = 'chilli pepper'
indian_ing_8._preperation = 'n/a'
indian_ing_8._quantity = ''
indian_ing_8._descriptor = ["dried", "red"]
indian_list.append(indian_ing_8)

#print (indian_list)

main_ingredient_list = ['chicken', 'turkey', 'beef', 'fish', 'tuna', 'paneer', 'tofu', 'mushroom', 'sausage', 'pork', 'samon', 'pig', 'tofu', '']

italian_list_names = ['basil', 'mozzarella', 'wine', 'ricotta', 'olive', 'parmesan', 'caper', 'balsamic', 'oregano', 'italian']


def make_indian(ingredients):
	replaced = []
	for ingredient in ingredients:
		for italian_list_item in italian_list_names:
			if italian_list_item.lower() in ingredient._name.lower() or italian_list_item in ingredient._descriptor.lower():
				ingredients.remove(ingredient)
	ingredients = ingredients+indian_list

	return ingredients

print(make_indian(danparser.ingredient_info("https://www.allrecipes.com/recipe/14592/italian-style-meatloaf-i/")))


	

#print(make_vegetarian(LakshmanParser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")))
