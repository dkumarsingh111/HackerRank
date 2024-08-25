#Welcome to NLP Using Python - Simple Text Operation

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
import nltk


#
# Complete the 'findWordFreq' function below.
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
import nltk


#
# Complete the 'findWordFreq' function below.
#
# 


def findWordFreq(text, word):
    # Write your code here
    
    # Task 1:
    # Find the frequency for the given 'word', and store it into the variable 'wordfreq'.
    textfreq = [word for word in text if word.isalpha()]
    FreqDist = nltk.FreqDist(textfreq)
    wordfreq=  FreqDist[word]
    
    # Task 2:
    # Find the word which has a maximum frequency from the 'textfreq', and store into the variable 'maxfreq'.
    max_value = max(FreqDist.values())    
    maxfreq= [ item for item in FreqDist if FreqDist[item]== max_value][0]
    
    return    wordfreq, maxfreq

if __name__ == '__main__':
    text = input()
    word = input()
    if not os.path.exists(os.getcwd() + "/nltk_data"):
        with zipfile.ZipFile("nltk_data.zip", 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())

    text = Text(gutenberg.words(text))

    word_freq, max_freq = findWordFreq(text, word)

    print(word_freq)
    print(max_freq)