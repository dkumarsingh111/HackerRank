#Welcome to NLP Using Python - Stemming and Lemmatization

#!/bin/python3

import math
import os
import random
import re
import sys
import zipfile
os.environ['NLTK_DATA'] = os.getcwd()+"/nltk_data"
import nltk

#
# Complete the 'performStemAndLemma' function below.
#
# The function accepts STRING textcontent as parameter.
#

import math
import os
import random
import re
import sys
import zipfile
os.environ['NLTK_DATA'] = os.getcwd()+"/nltk_data"
import nltk

#
# Complete the 'performStemAndLemma' function below.
#
# The function accepts STRING textcontent as parameter.

from nltk.corpus import stopwords
def performStemAndLemma(textcontent):
    # Write your code here
    # Task 1:
    # Task 1: Tokenize all the words given in 'textcontent'. The word should contain alphabetes or numbers or underscore. Store the tokenized list of words in 'tokenizedwords'
    
    reg_exp= r'([A-Za-z0-9\_]+)'
    tokenizedwords = nltk.regexp_tokenize(textcontent , pattern= reg_exp)
    
    # Task 2: Convert all the words into lowercase. Store the result in 'tokenizedwords'.
    tokenizedwords = [  word.lower() for word in set(tokenizedwords) ]
    
    # Task 3:
    # Remove all the stop words from the 'tokenizedwords'. Store the result into the variable 'filteredwords'.
    sw = set(stopwords.words('english'))
    filteredwords = [ word for word in tokenizedwords if (word not in sw)]
    
    # Task 4: 
    # Stem each word present in 'filteredwords' with 'PorterStemmer', and store the resultin the list 'porterstemmedwords'.
    porterstemmedwords =   [  nltk.PorterStemmer().stem(word)  for word in filteredwords ]
    
    # Task 5:
    # Stem each word present in 'filteredwords' with 'LancasterStemmer', and store the resultin the list 'lancasterstemmedwords'.
    lancasterstemmedwords =  [  nltk.LancasterStemmer().stem(word)  for word in filteredwords ]  
    
    # Task 6:
    # Stem each word present in 'filteredwords' with 'WordNetLemmatizer', and store the resultin the list 'lemmatizedwords'.
    lemmatizedwords = [  nltk.WordNetLemmatizer().lemmatize(word)  for word in filteredwords ]
     
    
    return porterstemmedwords, lancasterstemmedwords, lemmatizedwords

if __name__ == '__main__':
    textcontent = input()

    if not os.path.exists(os.getcwd() + "/nltk_data"):
        with zipfile.ZipFile("nltk_data.zip", 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())

    porterstemmedwords, lancasterstemmedwords, lemmatizedwords = performStemAndLemma(textcontent)

    print(sorted(porterstemmedwords))
    print(sorted(lancasterstemmedwords))
    print(sorted(lemmatizedwords))
