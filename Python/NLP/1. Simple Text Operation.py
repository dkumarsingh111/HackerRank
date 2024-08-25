#Welcome to NLP Using Python - Simple Text Operation

#!/bin/python3

import math
import os
import random
import re
import sys

import zipfile

os.environ['NLTK_DATA'] = os.getcwd()+"/nltk_data"
from nltk.corpus import gutenberg
from nltk.text import Text

#
# Complete the 'calculateWordCounts' function below.
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
# Complete the 'calculateWordCounts' function below.
#

def calculateWordCounts(text):
    # Write your code here
    
    # Task 1:
    # Find the number of words in 'text', and print the result.
    total_word= len(text)
    print(total_word)
    
    # Task 2:
    # Find the number of unique words in 'text', and print the result.
    unique_word= len(set(text))
    print(unique_word)
    
    # Task 3:
    # Calculate the word coverage of 'text' obtained from the number of words and number of unique words,and print the result.
    average= total_word/unique_word
    print(math.floor(average))
    

if __name__ == '__main__':
    text = input()
    if not os.path.exists(os.getcwd()+"/nltk_data"):
        with zipfile.ZipFile("nltk_data.zip", 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())
    
    text = Text(gutenberg.words(text))

    calculateWordCounts(text)
