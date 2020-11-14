# -*- coding: utf-8 -*-
"""Feature_extraction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e60QrMguIyGyTUPoNMC7U9r8mkHJQgH5
"""

import json
file = r'./train.json'
with open(file) as train_file:
    dict_train = json.load(train_file)

print(dict_train[0])

#Construct dictionary of ingredients
ingredients = {}
for i in range(len(dict_train)):
  for ing in dict_train[i]['ingredients']:
    if ing in ingredients:
      ingredients[ing] = ingredients[ing] + 1
    else:
      ingredients[ing] = 1

sorted_ing = sorted(ingredients.items(), key=lambda x: x[1])
nb = 0
i = 0
features = {}
for element in sorted_ing:
  nb = nb + 1
  if nb > 5714:
    features[element[0]] = i
    i = i + 1

len(features)

with open('features.json', 'w') as outfile:
    json.dump(features, outfile)

#Define encoding process
import numpy as np
def encode (list_of_ingredients):
  encoding = np.zeros(1000)
  for x in list_of_ingredients:
    if x in features:
      encoding[features[x]] = 1
    else:
      encoding[999] = 1
  return encoding

#create sample user history
sample_user_history = {}
sample_user_history[1001] = [['tomatoes', 'eggs', 'pepper', 'shellfish'], 5]
sample_user_history[1004] = [['tomatoes', 'chicken', 'fresh ginger', 'cayenne pepper'], 4]
sample_user_history[1006] = [['carrots', 'milk', 'lime', 'zucchini'], 2]

sample_user_history

#construct user preference representation
def encode_preference(sample_user_history):
  encoding = np.zeros(1000)
  for order in sample_user_history:
    rating = sample_user_history[order][1]
    if rating >= 3:
      encoding = encoding + (rating * encode(sample_user_history[order][0]))
    else:
      encoding = encoding - ((5-rating) * encode(sample_user_history[order][0]))
  return (encoding)

def score(offer):
  offer_encoding = encode(offer)
  user_preference = encode_preference(sample_user_history)
  score_matrix = np.multiply(offer_encoding, user_preference)
  score = np.sum(score_matrix)
  return score

offer = ['carrots', 'chicken', 'fresh ginger', 'cayenne pepper']
score(offer)