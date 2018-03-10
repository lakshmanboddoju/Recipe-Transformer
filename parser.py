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


tool_list = open('tools.txt').read().split('\n')
measurement_list = open('measurements.txt').read().split('\n')


def getTools(url):
	webUrl = url
	webFile = urllib.urlopen(webUrl)
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
	webFile = urllib.urlopen(webUrl)
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

		ingredient_no_number=q.sub("", ingredient)

		#print(ingredient_no_number)
		line_tokened = nltk.word_tokenize(ingredient_no_number)


		hasMeasurement=False
		for token in line_tokened:

			#get units
			if (token.lower() in measurement_list):
				hasMeasurement=True
				line_tokened.remove(token)
				measurement=token.lower()
				#print ("Measurement: %s\n" %(token.lower()))

			#if no measurement included, say 'no measurement'
		if (hasMeasurement==False):
			measurement= "n/a"

		# preparations
		ingredient_name = q.sub("", ingredient)

		prep_tokens = nltk.word_tokenize(ingredient_name)
		tagged = nltk.pos_tag(prep_tokens)
		past_tense= [word for word, pos in tagged \
			if (pos == 'VBD' or pos == 'VBN')]


		#preparation = str(past_tense)


		if(past_tense):
			for x in past_tense:
				dreg = r'(\s*)' +re.escape(x)
				d = re.compile(dreg)
				ingredient_name = d.sub('', ingredient_name)
		else: 
			past_tense = ["n/a"]


		#whatever is left is the ingredient name
		line_tokened= " ".join(line_tokened)
		print("Name: %s" %(line_tokened))
		print ("Quantity: %s" % (number))
		print ("Measurement: %s\n" %(measurement))
		print ("Preparation: %s\n" %(', '.join(past_tense)))



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



ingredient_info("https://www.allrecipes.com/recipe/235151/crispy-and-tender-baked-chicken-thighs/")
getTools("https://www.allrecipes.com/recipe/8372/black-magic-cake/")

	