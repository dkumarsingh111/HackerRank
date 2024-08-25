#Welcome to NLP Using Python - Processing Raw Text

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
# Complete the 'processRawText' function below.
#
# The function accepts STRING textURL as parameter.
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
# Complete the 'processRawText' function below.
#
# The function accepts STRING textURL as parameter.
#
from urllib import request
def processRawText(textURL):
    # Write your code here
    
    # Task 1: 
    # Read the text content from the given link 'textURL'. Store the content in the variable 'textcontent'.
    #    
    url = textURL
    textcontent = request.urlopen(url).read()
    
    # Task 2:
    # Tokenize all the words in the 'textcontent', and convert them into lower case. Store the tokenized list of words in 'tokenizedlcwords'.
    #
    
    text_content1 = textcontent.decode('unicode_escape')  # Converts bytes to unicode
    tokens1 = nltk.word_tokenize(text_content1)
    wordfreq_m= nltk.FreqDist(tokens1)
    
    tokenizedlcwords =  [  word.lower()  for word in tokens1 ]
    
    # Task 3:
    # Find the number of words in 'tokenizedlcwords', and store the result in  'noofwords'.
    #
    noofwords = len(tokenizedlcwords)
    
    # Task 4:
    # Find the number of unique words in 'tokenizedlcwords', and store the result in  'noofunqwords'.
    #
    noofunqwords = len(set( tokenizedlcwords))   
    
    # Task 5 :
    # Calculate the word coverage of 'tokenizedlcwords' obtained from the number of words and number of unique words, Store the result in the 'wordcov'.
    #
    wordcov =  int( noofwords / noofunqwords)
    
    # Task 6:
    # Determine the frequency distribution of all words having only alphabets in 'tokenizedlcwords'. Store the result in the variable 'wordfreq'.
    wordfreq_list = [  word  for word in tokens1 if word.isalpha() ]
    wordfreq= len(wordfreq_list)

    # Task 7
    # Find the maximum frequent word of 'tokenizedlcwords'. Store the result in the variable 'maxfreq'   
    dict_of_word_frequency = { x: tokenizedlcwords.count(x) for x in tokenizedlcwords }
    maxfreq = max(dict_of_word_frequency, key= dict_of_word_frequency.get)
    
    # print()
    return noofwords, noofunqwords, wordcov,maxfreq
    
    

if __name__ == '__main__':
    textURL = input()

    if not os.path.exists(os.getcwd() + "/nltk_data"):
        with zipfile.ZipFile("nltk_data.zip", 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())

    noofwords, noofunqwords, wordcov, maxfreq = processRawText(textURL)
    print(noofwords)
    print(noofunqwords)
    print(wordcov)
    print(maxfreq)
