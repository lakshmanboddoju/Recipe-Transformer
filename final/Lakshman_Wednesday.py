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

def scrape_directions(url):
    webUrl = url
    webFile = urlopen(webUrl)
    webHtml = webFile.read()
    soup = BeautifulSoup(webHtml,"html.parser")
    webAll = soup.findAll("span", {"class": "recipe-directions__list--item"})
    directions = []
    for description in webAll:
        #print (description.string)
        directions.append(description.string)
    return directions

unhealthy_list = ['ghee', 'oil', 'butter', 'salt', 'sugar', 'fat']

def make_healthy(ingredients):
    replaced = []
    for ingredient in ingredients:
        for unhealthy_item in unhealthy_list:
            if unhealthy_item in ingredient._name.lower():
                #print (unhealthy_item)
                if ingredient._quantity != 'n/a' and ingredient._name not in replaced:
                    ingredient._quantity = 0.5 * float(sum(Fraction(s) for s in ingredient._quantity.split()))
                    replaced.append(ingredient._name)
    return ingredients

#print(make_healthy(LakshmanParser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")))

meat_to_veg_dict={"hamburger":"Veggie Burger", "beef broth":"vegetable broth", "chicken broth":"vegetable broth", "beef stock": "vegetable stock", "chicken stock":"vegetable stock", 
                  "chicken wings":"tofu", "chicken":"tofu","steak":"portabello mushrooms", "chorizo":"tofu", "hot dog": "soy dog", "turkey":"soy", "veal":"tofu","beef":"soy", 
                  "pork":"portabello mushrooms", "salmon":"tofu", "ham": "tofu", "pig": "tofu"}

meat_to_veg_directions_dict = {"beef": "soy", "chicken": "tofu", "steak": "portabello mushrooms", "turkey": "soy", "veal": "tofu", "chorizo": "tofu", "salmon": "tofu", 
                               "pork": "tofu", "pig": "tofu", "ham": "tofu"}

def make_vegetarian(ingredients, directs):
    replaced = []
    replaced_to = []
    for ingredient in ingredients:
        for meat_item in meat_to_veg_dict.keys():
            if meat_item.lower() in ingredient._name.lower():
                if ingredient._name not in replaced:
                    print ("\n\nReplacing:\t", ingredient._name)
                    replaced.append(meat_item)
                    ingredient._name = meat_to_veg_dict[meat_item]
                    ingredient._descriptor = 'n/a'
                    replaced_to.append(ingredient._name)

    meat_list = []
    meat_txt = open('meats.txt', 'r')
    meat_line = meat_txt.readlines()
    for m in meat_line:
        temp = m.rstrip('\n')
        meat_list.append(str(temp.lower()))

    meat_list_replaced = []
    for ingredient in ingredients:
        for meat_item in meat_list:
            if meat_item.lower() in ingredient._name.lower():
                print (ingredient._name)
                if meat_name not in replaced and meat_item not in meat_list_replaced:
                    ingredient._name = 'Paneer'
                    ingredient._descriptor = 'n/a'
                    meat_list_replaced.append(ingredient._name)

    print ("\nReplaced List:\t", replaced)
    print ("\nReplaced to:\t", replaced_to)
    '''for step in directs:
        #print ("\n", step)
        for item in replaced:
            if item is not None and step is not None:
                #print("item:\t", item)
                if item in step:
                    print(item)
                    print (directs[directs.index(step)].replace(item, replaced_to[replaced.index(item)]))
                    #print (step)'''

    for step in directs:
        #print("step\n", step)
        for meat_item in meat_to_veg_directions_dict.keys():
            if meat_item is not None and step is not None:
                if meat_item in step:
                    directs[directs.index(step)] = directs[directs.index(step)].replace(meat_item, meat_to_veg_directions_dict[meat_item])


    return ingredients, list(filter(None.__ne__, directs))

#print(danparser.ingredient_info("https://www.allrecipes.com/recipe/8372/black-magic-cake/"))



#print(danparser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/"))
#print(make_vegetarian((danparser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")), scrape_directions("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/"))[1])
#for direction in make_vegetarian((danparser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")), scrape_directions("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/"))[1]:
    #print("\n", direction, "\n")
#print(make_vegetarian((danparser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")), scrape_directions("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")))


indian_list = []
indian_ing_1 = danparser.Ingredient()
indian_ing_1._name = 'garlic'
indian_ing_1._preperation = 'paste'
indian_ing_1._quantity = ''
indian_ing_1._descriptor = "n/a"
indian_ing_1._measurement = 'teaspoon'
indian_list.append(indian_ing_1)

indian_ing_2 = danparser.Ingredient()
indian_ing_2._name = 'ginger'
indian_ing_2._preperation = 'paste'
indian_ing_2._quantity = ''
indian_ing_2._descriptor = "n/a"
indian_ing_2._measurement = 'teaspoon'
indian_list.append(indian_ing_2)

indian_ing_3 = danparser.Ingredient()
indian_ing_3._name = 'curry powder'
indian_ing_3._preperation = 'n/a'
indian_ing_3._quantity = ''
indian_ing_3._descriptor = "n/a"
indian_ing_3._measurement = 'tablespoon'
indian_list.append(indian_ing_3)

indian_ing_4 = danparser.Ingredient()
indian_ing_4._name = 'garam masala'
indian_ing_4._preperation = 'n/a'
indian_ing_4._quantity = ''
indian_ing_4._descriptor = "n/a"
indian_ing_4._measurement = 'tablespoon'
indian_list.append(indian_ing_4)

indian_ing_5 = danparser.Ingredient()
indian_ing_5._name = 'cumin'
indian_ing_5._preperation = 'n/a'
indian_ing_5._quantity = ''
indian_ing_5._descriptor = "n/a"
indian_ing_5._measurement = 'teaspoon'
indian_list.append(indian_ing_5)

indian_ing_6 = danparser.Ingredient()
indian_ing_6._name = 'coriander'
indian_ing_6._preperation = 'minced'
indian_ing_6._quantity = ''
indian_ing_6._descriptor = "n/a"
indian_ing_6._measurement = 'leaves'
indian_list.append(indian_ing_6)

indian_ing_7 = danparser.Ingredient()
indian_ing_7._name = 'mustard seeds'
indian_ing_7._preperation = 'n/a'
indian_ing_7._quantity = ''
indian_ing_7._descriptor = "black"
indian_ing_7._measurement = 'teaspoon'
indian_list.append(indian_ing_7)

indian_ing_8 = danparser.Ingredient()
indian_ing_8._name = 'chilli pepper'
indian_ing_8._preperation = 'n/a'
indian_ing_8._quantity = ''
indian_ing_8._descriptor = "dried, red"
indian_ing_8._measurement = 'tablespoon'
indian_list.append(indian_ing_8)

italian_list_names = ['basil', 'mozzarella', 'wine', 'ricotta', 'olive', 'parmesan', 'caper', 'balsamic', 'oregano', 'italian']

chinese_list_names = ['soy sauce', 'oyster sauce', 'sesame oil', 'rice vinegar', 'rice wine', 'chili sauce', 'soybean paste', 'star anise', 'five spice powder', 'sichaun peppercorn']

mexican_list_names = ['garlic powder', 'mexican oregano', 'onion powder', 'paprika', 'black pepper', 'cloves', 'coriander', 'cilantro']

mediterranean_list_names = ['basil', 'cilantro', 'coriander', 'chives', 'fennel', 'mint', 'parsley', 'rosemary', 'sage', 'saffron', 'thyme']

#indian_list_names = ['garlic', 'ginger', 'curry powder', 'garam masala', 'cumin', 'masala', 'coriander', 'cilantro', 'mustard seeds', 'chilli pepper']

combined_non_indian_list = list(set(italian_list_names)|set(chinese_list_names)|set(mexican_list_names)|set(mediterranean_list_names))

def make_indian(ingredients):
    replaced = []
    temp_count = 0
    quantity_of_indian = ''
    flag = 0
    for ingredient in ingredients:
        for combined_non_indian_list_item in combined_non_indian_list:
            if combined_non_indian_list_item.lower() in ingredient._name.lower() or combined_non_indian_list_item in ingredient._descriptor.lower():
                if combined_non_indian_list_item not in replaced:
                    if ingredient._measurement == 'teaspoon':
                        quantity_of_indian = ingredient._quantity
                    flag += 1
                    replaced.append(combined_non_indian_list_item)
                    if ingredient in ingredients:
                        ingredients.remove(ingredient)

    ingredients = ingredients+indian_list

    another_replaced = []

    '''for step in directs:
        #print("step\n", step)
        for combined_non_indian_list_item in combined_non_indian_list:
            if combined_non_indian_list_item is not None and step is not None:
                if (" "+combined_non_indian_list_item+" ") in step:
                    print("bobobob", combined_non_indian_list_item)
                    temp_count += 1
                    directs[directs.index(step)] = directs[directs.index(step)].replace(combined_non_indian_list_item, indian_list[temp_count]._name)'''

    return ingredients

#print(make_indian(danparser.ingredient_info("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/"), scrape_directions("https://www.allrecipes.com/recipe/228293/curry-stand-chicken-tikka-masala-sauce/")))
#print(make_indian(danparser.ingredient_info("https://www.allrecipes.com/recipe/233661/chef-johns-lasagna/"), scrape_directions("https://www.allrecipes.com/recipe/233661/chef-johns-lasagna/")))