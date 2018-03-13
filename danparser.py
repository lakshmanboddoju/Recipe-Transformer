from textblob import TextBlob
import nltk
import json
from nltk import ne_chunk, pos_tag, word_tokenize
import string
import re
import pprint
import urllib
#from urllib.request import urlopen
from bs4 import BeautifulSoup
import pprint


tool_list = open('tools.txt').read().split('\n')
measurement_list = open('measurements.txt').read().split('\n')
descriptors_list = open('descriptors.txt').read().split('\n')
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
		return "Name: %s\nQuantity: %s\nMeasurement: %s\nDescription: %s\nPreparation: %s\n\n" %(self._name, self._quantity, self._measurement, self._descriptor, self._preparation)


def getTools(url):
	webUrl = url
	webFile = urllib.urlopen(webUrl)
	webHtml = webFile.read()
	soup = BeautifulSoup(webHtml,"html.parser")
	webAll = soup.findAll("span", {"class": "recipe-directions__list--item"})
	tools=[]
	finalString=""
	count=0

	for step in webAll:
		for tool in tool_list:
			if tool in step.text:
				tools.append(tool)

	for x in tools:
		count+=1
		finalString +=  "%d. %s " %(count, x)
	
	print("Tools: %s" %(finalString))
	return tools

	if(number):
			number = p.search(i)
			quantities.append(number.group())
			count+=1

	quantities= (', %d.'.join(quantities) %(count))	
	return quantities





def ingredient_info(url):
	webUrl = url
	webFile = urllib.urlopen(webUrl)
	webHtml = webFile.read()
	soup = BeautifulSoup(webHtml,"html.parser")
	ingredient_list = soup.findAll("label", {"ng-class": "{true: 'checkList__item'}[true]"})
	p=re.compile(r'([0-9]+)\s?(([./0-9]+)?)')
	punct=re.compile(r'[^\w\s]|[0-9/]')
	less=re.compile(r'(\w+less)')


	for line in ingredient_list:
		ingredient_name = line['title']
		#print(line['title'])
		
		quantity=""
		measurement=""
		descriptors=[]
		toRemove=[]
		preparation=[]
		anIngredient = Ingredient()



		#get measurement unit, checking against list, scraped
		hasMeasurement=False
		for measurement_list_item in measurement_list: 
			if (measurement_list_item in ingredient_name.lower() and hasMeasurement==False):
				hasMeasurement=True
				measurement=measurement_list_item
				mregex= r'(\s*)' + re.escape(measurement)  #+ r'(\s*)'
				m=re.compile(mregex)
				ingredient_name=m.sub('', ingredient_name)
				anIngredient._measurement=measurement

		#if no measurement included, say 'no measurement'
		if (hasMeasurement==False):
			anIngredient._measurement= "n/a"



		#--------starting to use more nltk

		tokened_ingredients=nltk.word_tokenize(ingredient_name)
		tagged_ingredients=nltk.pos_tag(tokened_ingredients)
		

		#quantities
		numbers= [num for num, pos in tagged_ingredients \
			if (pos=='CD')]
		if (numbers):
			anIngredient._quantity=', '.join(numbers)
			toRemove.extend(numbers)
		else:
			anIngredient._quantity="1"



		#descriptors
		for descriptors_item in descriptors_list:				#looking for hard coded descriptors, like 'to taste'
			if (descriptors_item in ingredient_name.lower()):
				descriptors.append(descriptors_item)
				descRegex= r'(\s*)' + re.escape(descriptors_item)  #+ r'(\s*)'
				descRegex=re.compile(descRegex)
				ingredient_name=descRegex.sub('', ingredient_name)


		descriptors+=[word for word, pos in tagged_ingredients \
			if (pos=='JJ' or pos=='JJR' or pos=='JJS' or pos=='RB' or pos=='VBG' or pos=='VB')]

		blanklessAdj=less.findall(ingredient_name)	#nltk thinks 'skinless' is an adj, so hardcoding this regex for _less adjs
		if(blanklessAdj):
			descriptors.extend(blanklessAdj)

		if(descriptors):
			anIngredient._descriptor=', '.join(descriptors)
			toRemove.extend(descriptors)

		else:
			anIngredient._descriptor="n/a"



		#preparation
		enumerated_tag_list=list(enumerate(tagged_ingredients))
		phrase=""

		for i, (word, pos) in enumerated_tag_list:
			if(enumerated_tag_list[i][1][1]=='VBD' or enumerated_tag_list[i][1][1]=='VBN'):		#if word is verb/participle
				if (i<len(enumerated_tag_list)-1 and enumerated_tag_list[i+1][1][1]=='IN'): 	#if verb/participle is part of a phrase
					j=i
					while (j<len(enumerated_tag_list)-1 and not (enumerated_tag_list[j][1][1]=='NN' or enumerated_tag_list[j][1][1]=='NNS')): #find the noun the phrase ends with
						phrase+="%s " %(enumerated_tag_list[j][1][0])
						toRemove.append(enumerated_tag_list[j][1][0]) #add each individual string in phrase to remove list
						j+=1
					phrase+="%s" %(enumerated_tag_list[j][1][0])
					toRemove.append(enumerated_tag_list[j][1][0])
					preparation.append(phrase)
				else:
					preparation.append(enumerated_tag_list[i][1][0])

		
		if(preparation):
			anIngredient._preparation=', '.join(preparation)
			toRemove.extend(preparation)	
		else: 
			anIngredient._preparation = "n/a"
		
		
		#remove numbers, descriptors, preparation
		if(toRemove):
			for x in tokened_ingredients:
				if (x in toRemove):
					removeRegex= re.escape(x)+  r'(\s*)'
					r=re.compile(removeRegex)
					ingredient_name=r.sub('',ingredient_name)
					


		#further fixing the name
		pregex=re.compile(punct)							#remove punctuation, numbers
		ingredient_name=pregex.sub('',ingredient_name)		

		name_tokened=nltk.word_tokenize(ingredient_name)	#remove conjunctions, determiners
		name_tagged=nltk.pos_tag(name_tokened)
		throwaway=[word for word, pos in name_tagged \
			if(pos=='CC' or pos=='DT')]

		if (throwaway):
			for x in throwaway:
				preg=r'(\s*)' + re.escape(x)
				preg= re.compile(preg)
				ingredient_name=preg.sub('', ingredient_name)


		
		anIngredient._name=ingredient_name		#name is whatever is left over

		recipe_ingredients.append(anIngredient)
			

	pp=pprint.PrettyPrinter(indent=4)
	pp.pprint  (recipe_ingredients)
	getTools(url)
	return recipe_ingredients

def get_quantities(directs):
	quantities =[]
	
	for i in directs:
		p = re.compile(r'([0-9]+)\s?(([./0-9]+)?)')
		number = p.search(i)
		quantities.append(number.group())
	print (quantities)	
	return quantities



ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")
#getTools("https://www.allrecipes.com/recipe/8372/black-magic-cake/")

#RECIPES
"""
https://www.allrecipes.com/recipe/49355/gin-and-tonic/
https://www.allrecipes.com/recipe/8372/black-magic-cake/
https://www.allrecipes.com/recipe/235151/crispy-and-tender-baked-chicken-thighs/
"""
