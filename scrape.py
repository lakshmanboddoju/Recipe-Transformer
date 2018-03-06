from textblob import TextBlob
import nltk
import json
from nltk import ne_chunk, pos_tag, word_tokenize
import string
import re
import pprint
#from urllib.request import urlopen
import urllib # use this instead of line above
from bs4 import BeautifulSoup



def scrape_recipe(url):
    webUrl = url
    webFile = urllib.urlopen(webUrl) #add urllib right before urlopen
    webHtml = webFile.read()
    soup = BeautifulSoup(webHtml,"html.parser")
    webAll = soup.findAll("label", {"ng-class": "{true: 'checkList__item'}[true]"})
    ingredients = []
    for item in webAll:
        print (item['title'])
        ingredients.append(item['title'])
    return ingredients
    
scraped_ingredients = scrape_recipe("https://www.allrecipes.com/recipe/23735/buffalo-style-chicken-pizza/?internalSource=rotd&referringId=1036&referringContentType=recipe%20hub")

#print scraped_ingredients

def transformer(list_of_ingredients):
    meat = ['skinless, boneless chicken breast halves', 'beef', 'pork']
    alt = 'tofu blocks'
    for i in list_of_ingredients:
        for m in meat:
            if m in i:
                #if meat in i: 
                new_ingredient = i.replace(m, alt) #could alsos use re.sub -> regex
                return new_ingredient
            else:
                return i
            #how to delete the original ingredient

def extract_quantity(list_of_ingredients):
    quantity = []
    measurement = []
    for i in list_of_ingredients:
        #temp = re.search('\d+', i) #  \( \) is how to find literal parentheses in regex
        temp = re.search('\d+', i)
        if temp:
            quantity.append(temp.group(0))
        else:
           quantity.append(1)
        
    return quantity

#look for all numbers in parentheses
#look for number in ()

print (extract_quantity(scraped_ingredients))

print (transformer(scraped_ingredients))
