#!/bin/python3

import math
import os
import random
import re
import sys
import zipfile

os.environ['NLTK_DATA'] = os.getcwd() + "/nltk_data"
from nltk.corpus import gutenberg
from nltk.text import Text


#
# Complete the 'filterWords' function below.
#
# 
#

import math
import os
import random
import re
import sys
import zipfile

os.environ['NLTK_DATA'] = os.getcwd() + "/nltk_data"
from nltk.corpus import gutenberg
from nltk.text import Text


#
# Complete the 'filterWords' function below.
#


def filterWords(text):
    # Write your code here
    
    # Task 1:
    # Filter the words ending with 'ing' from the set of unique words of 'text', and store into 'ing_words' variable as a list.
    unique_word= set(text)
    ing_words= [ words for words in unique_word if words.endswith('ing') ]
     
    # Task 2:
    # Filter the words whose length is greater then 15 from the complete set of 'text', and store into 'large_words' variable as a list.
    large_words= [ words for words in text if len(words.strip())>15]
    
    # Task 3:
    # Filter the words having all letters in upper case from the set of unique words of 'text', and store into 'upper_words' variable as a list.
    upper_words= [ words for words in unique_word if  (type(words) == str and words.isupper())]   
    
    return ing_words,large_words,upper_words

if __name__ == '__main__':
    text = input()
    if not os.path.exists(os.getcwd() + "/nltk_data"):
        with zipfile.ZipFile("nltk_data.zip", 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
            
    text = Text(gutenberg.words(text))

    ing_words, big_words, upper_words = filterWords(text)

    print(sorted(ing_words))
    print(sorted(big_words))
    print(sorted(upper_words))
