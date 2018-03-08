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
def parser(url):
	webUrl = url
	webFile = urlopen(webUrl)
	webHtml = webFile.read()
	soup = BeautifulSoup(webHtml,"html.parser")
	webAll = soup.findAll("span", {"class": "recipe-directions__list--item"})


	for step in webAll:
		for x in tool_list:
			if x in step.text:
				print  ("Tool: %s" %(x))

parser("https://www.allrecipes.com/recipe/235151/crispy-and-tender-baked-chicken-thighs/")


	