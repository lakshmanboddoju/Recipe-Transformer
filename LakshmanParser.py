from textblob import TextBlob
import nltk
import json
from nltk import ne_chunk, pos_tag, word_tokenize
import string
import re
import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup


tool_list = open('tools.txt').read().split('\n')
measurement_list = open('measurements.txt').read().split('\n')

recipe_ingredients=[]

class Ingredient:
	def __init__(self):
		self._quantity = ""
		self._measurement = ''
		self._name = ''
		self._descriptor = []
		self._preparation = ""

	def __repr__(self):
		#return self.__dict__
		return "Name: %s\nQuantity: %s\nMeasurement: %s\nDescription: %s\nPreparation: %s\n" %(self._name, self._quantity, self._measurement, self._descriptor, self._preparation)


def getTools(url):
	webUrl = url
	webFile = urlopen(webUrl)
	webHtml = webFile.read()
	soup = BeautifulSoup(webHtml,"html.parser")
	webAll = soup.findAll("span", {"class": "recipe-directions__list--item"})
	tools=[]

	for step in webAll:
		for tool in tool_list:
			if tool in step.text:
				tools.append(tool)


	print("Tools: %s" %(tools))
	return tools

def ingredient_info(url):
	webUrl = url
	webFile = urlopen(webUrl)
	webHtml = webFile.read()
	soup = BeautifulSoup(webHtml,"html.parser")
	ingredient_list = soup.findAll("label", {"ng-class": "{true: 'checkList__item'}[true]"})
	p=re.compile(r'([0-9]+)\s?(([./0-9]+)?)')
	q=re.compile(r'[0-9/]')
	

	for line in ingredient_list:
		ingredientLine = line['title']
		print(line['title'])
		
		ingredient_name=""
		quantity=""
		measurement=""
		
		anIngredient = Ingredient()


		#quantity
		number=p.search(ingredientLine)
		if (number):
			anIngredient._quantity=number.group()
		else:
			anIngredient._quantity= "n/a"

		#get measurement unit
		hasMeasurement=False
		for measurement_list_item in measurement_list: 
			if (measurement_list_item in ingredientLine.lower() and hasMeasurement==False):
				hasMeasurement=True
				measurement=measurement_list_item
				mregex= r'(\s*)' + re.escape(measurement)  + r'(\s*)'
				m=re.compile(mregex)
				ingredientLine=m.sub('', ingredientLine)
				anIngredient._measurement=measurement

			#if no measurement included, say 'no measurement'
		if (hasMeasurement==False):
			anIngredient._measurement= "n/a"

		#remove numbers
		ingredient_name=q.sub("", ingredientLine)

		#find descriptors
		ingredients_tokened = nltk.word_tokenize(ingredient_name)
		tagged_ingredients = nltk.pos_tag(ingredients_tokened)
		descriptors=[word for word, pos in tagged_ingredients \
			if (pos=='JJ' or pos=='JJR' or pos=='JJS' or pos=='RB' or pos=='VBG' or pos=='VB')]

		past_tense=[word for word, pos in tagged_ingredients \
			if (pos == 'VBD' or pos =='VBN')]

		if(past_tense):
			for x in past_tense:
				dreg = r'(\s*)' +re.escape(x)
				d = re.compile(dreg)
				ingredient_name = d.sub('', ingredient_name)
		else: 
			past_tense = ["n/a"]

		#remove descriptors from ingredients, leaving just the name

		if(descriptors):
			for x in descriptors:
				dregex=r'(\s*)' + re.escape(x) 
				d=re.compile(dregex)
				ingredient_name=d.sub('',ingredient_name)
		else:
			descriptors=["n/a"]

		anIngredient._descriptor=', '.join(descriptors)
		anIngredient._preparation=', '.join(past_tense)
		anIngredient._name=ingredient_name

		recipe_ingredients.append(anIngredient)

	#pp=pprint.PrettyPrinter(indent=4)
	#pp.pprint  (recipe_ingredients)
	return recipe_ingredients

def get_quantities(directs):
	quantities =[]
	
	for i in directs:
		p = re.compile(r'([0-9]+)\s?(([./0-9]+)?)')
		#number = re.search("([0-9]+)\s?(([./0-9]+)?))", anything)
		number = p.search(i)
		quantities.append(number.group())
	print (quantities)	
	return quantities


#pp=pprint.PrettyPrinter(indent=4)
#pp.pprint(ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/"))
#getTools("https://www.allrecipes.com/recipe/8372/black-magic-cake/")

#RECIPES
"""
https://www.allrecipes.com/recipe/49355/gin-and-tonic/
https://www.allrecipes.com/recipe/8372/black-magic-cake/
https://www.allrecipes.com/recipe/235151/crispy-and-tender-baked-chicken-thighs/
"""
	