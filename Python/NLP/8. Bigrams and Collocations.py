#Welcome to NLP Using Python - Bigrams and Collocations

#!/bin/python3

import math
import os
import random
import re
import sys
import zipfile
os.environ['NLTK_DATA'] = os.getcwd() + "/nltk_data"

import nltk


#
# Complete the 'performBigramsAndCollocations' function below.
#
# The function accepts following parameters:
#  1. STRING textcontent
#  2. STRING word
#

import math
import os
import random
import re
import sys
import zipfile
os.environ['NLTK_DATA'] = os.getcwd() + "/nltk_data"

import nltk


#
# Complete the 'performBigramsAndCollocations' function below.
#
# The function accepts following parameters:
#  1. STRING textcontent
#  2. STRING word
#

#
from nltk.corpus import stopwords
def performBigramsAndCollocations(textcontent, word):
    # Write your code here
    
    # Task 1: Tokenize all the words given in 'textcontent'. The word should contain alphabetes or numbers or underscore. Store the tokenized list of words in 'tokenizedwords'
    reg_exp= r'([A-Za-z0-9\_]+)'
    tokenizedwords = nltk.regexp_tokenize(textcontent , pattern= reg_exp)
    
    # Task 2: Convert all the words into lowercase. Store the result in 'tokenizedwords'.
    tokenizedwords = [  word.lower() for word in tokenizedwords ]
    
    # Task 3: Compute bigrams of the list 'tokenizedwords'. Store the list of bigrams in 'tokenizedwordsbigrams'
    tokenizedwordsbigrams = nltk.bigrams(tokenizedwords)
    
    # Task 4:
    # Filter only the bigrams from 'tokenizedwordsbigrams', where the words are not part of 'stopwords'.
    # Store the result in  'tokenizednonstopwordsbigrams'.  
    
    sw = set(stopwords.words('english'))
    temp = list(tokenizedwordsbigrams)

    sw = set(stopwords.words('english'))

    tokenizedwordsbigrams = temp
    # print(tokenizedwordsbigrams)

    tokenizednonstopwordsbigrams = [ j   for j  in tokenizedwordsbigrams  if j[0] not in sw and  j[1] not in sw   ]
    
    # Task 5:
    # Compute the Conditional Frequency of 'tokenizednonstopwordsbigrams', where condition and event refer to the word.
    # Store the result in 'cfd_bigrams'.
    
    cfd_bigrams = nltk.ConditionalFreqDist(tokenizednonstopwordsbigrams)
    
    # Task 6:
    # Determine the three most frrerquent words occuring after the given 'word'.
    # Store the result in 'mostfrequentwordafter'.
    mostfrequentwordafter = cfd_bigrams[word].most_common(3)
    
    # Task 7:
    # Generate collocations from 'tokenizedwords'. Store list of collocations words in 'collocationwords'.
    collocation_list = nltk.Text(tokenizedwords).collocation_list() 
    collocationwords=  [ " ".join([s1,s2]) for s1,s2  in collocation_list  ] 
    
    return  mostfrequentwordafter, collocationwords

if __name__ == '__main__':
    textcontent = input()

    word = input()

    if not os.path.exists(os.getcwd() + "/nltk_data"):
        with zipfile.ZipFile("nltk_data.zip", 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())

    mostfrequentwordafter, collocationwords = performBigramsAndCollocations(textcontent, word)
    print(sorted(mostfrequentwordafter, key=lambda element: (element[1], element[0]), reverse=True))
    print(sorted(collocationwords))