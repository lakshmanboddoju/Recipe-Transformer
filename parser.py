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

	#onlyComma = re.compile(r'[\w, ]+')	
	#print  ("Tools: %s" %(onlyComma.search(tools).group()))
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
		ingredient = line['title']
		#line_tokened = nltk.word_tokenize(ingredient)

		name=""
		quantity=""
		measurement=""

		#quantity
		number=p.search(ingredient)
		if (number):
			number=number.group()
		else:
			number= "n/a"

		#ingredient_no_number=q.sub("", ingredient)


		hasMeasurement=False
		"""for token in line_tokened:

			#get units
			if (token.lower() in measurement_list):
				hasMeasurement=True
				line_tokened.remove(token)
				measurement=token.lower()"""

		for measurement_list_item in measurement_list: 
			if (measurement_list_item in ingredient.lower() and hasMeasurement==False):
				hasMeasurement=True
				measurement=measurement_list_item
				mregex= r'(\s*)' + re.escape(measurement)  + r'(\s*)'
				m=re.compile(mregex)
				ingredient=m.sub('', ingredient)

			#if no measurement included, say 'no measurement'
		if (hasMeasurement==False):
			measurement= "n/a"


		#remove numbers
		ingredient_no_number=q.sub("", ingredient)

		#whatever is left is the ingredient name

		print("Name: %s" %(ingredient_no_number))
		print ("Quantity: %s" % (number))
		print ("Measurement: %s\n" %(measurement))



	return 0

def get_quantities(directs):
	quantities =[]
	
	for i in directs:
		p = re.compile(r'([0-9]+)\s?(([./0-9]+)?)')
		#number = re.search("([0-9]+)\s?(([./0-9]+)?))", anything)
		number = p.search(i)
		quantities.append(number.group())
	print (quantities)	
	return quantities



ingredient_info("https://www.allrecipes.com/recipe/49355/gin-and-tonic/")
getTools("https://www.allrecipes.com/recipe/8372/black-magic-cake/")

#RECIPES
"""
https://www.allrecipes.com/recipe/49355/gin-and-tonic/
https://www.allrecipes.com/recipe/8372/black-magic-cake/
https://www.allrecipes.com/recipe/235151/crispy-and-tender-baked-chicken-thighs/
"""
	