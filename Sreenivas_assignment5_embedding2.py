# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 20:37:57 2017

@author: krish
"""

#Name: Krishna Sreenivas
#Student ID: 800984436

import re
import string
import math
from math import *
from gensim.models import KeyedVectors #library to load embeddings in word2vec format
import operator #to iterate through keys in dictionary
from sklearn.metrics.pairwise import cosine_similarity #to obtain cosine similarity between 2 vectors 

#finding analogies between the selected categories
categories = [': capital-world', ': currency', ': city-in-state', ': family', ': gram1-adjective-to-adverb',
              ': gram2-opposite', ': gram3-comparative', ': gram6-nationality-adjective',': cellphones',': national-animals']
#termporary flag to check if the category is already present as key in dctionary
insert = False
analogy = {} #dictionary to hold analogies of selected categories
analogyVocab = {}#dictionary to hold unique words of selected categories of analogies
#loading the test file in to an list
file = open('analogies.txt', 'r').read()
lines = file.splitlines()
for i in range(len(lines)):
    if re.match('^\:', lines[i]): #checking if line starts with ':'
        if lines[i] in categories: #if line has ':' making that line as key
            key = lines[i]
            insert = True
            analogy[key] = [] 
            analogyVocab[key] = set()
        else:
            insert = False
    elif not re.match('^\:', lines[i]) and insert is True: #if line doesn't start with ':' append the line to the analogy dictionary
        analogy[key].append(lines[i].lower()) 
        for word in lines[i].split(' '):
            analogyVocab[key].add(word.replace('\t', '').lower()) #removing tab spaces and lowering the words
            
#loading the glove embeddings in word2vec format      
word_vectors = KeyedVectors.load_word2vec_format('lexvec.commoncrawl.300d.W.pos.neg3.txt', binary=False)

#performing Vd = Vb - Va + Vc
def get_compound(word1, word2, word3):
    temp_return = 0
    #if words present in the embeddings
    if word1 in word_vectors.vocab and word2 in word_vectors.vocab and word3 in word_vectors.vocab:
      #if yes then performing the calculation Vb - Va + Vc
        temp_return = [y - x + z for x, y, z in zip(word_vectors[word1], word_vectors[word2], word_vectors[word3])]
    return temp_return

#calculating cosine similarity between Vd and the 4th word of the analogy
def predict_word(word1, word2, word3, analogy_section):
    cosine_sim = {}
    #iterating and obtaining the vector for all words present in the vocab dictionary
    for each_section in analogyVocab[analogy_section]:
        return_value = get_compound(word1, word2, word3)
        if return_value != 0 and each_section in word_vectors.vocab:
          #calculating the cosine similarity between Vd and vectors of all words present in the vocab dictionary
            cosine_sim[each_section] = cosine_similarity([word_vectors[each_section]], [return_value])
        else:
            cosine_sim[each_section] = 0
    #choosing the max cosine value and getting its key
    return max(cosine_sim.items(), key=operator.itemgetter(1))[0]

#function to calculate the accuracy and predicts the 4th word in the analogy
def main():
  #variables to hold the count and accuracy values 
  acc=0
  sum=0
  for section in categories:
      for value in analogy[section]:
          splits = value.split(" ") #splitting the analogies into individual terms
          if splits[3] == predict_word(splits[0], splits[1], splits[2], section): #checking if the 4th word is similar to predicted word
              acc += 1
  for value in analogy.values():
    sum+=len(value)
  print("Accuracy using Lexvec embeddings is: ",((acc/sum)*100)) #printing the final accuracy values
  
main()
