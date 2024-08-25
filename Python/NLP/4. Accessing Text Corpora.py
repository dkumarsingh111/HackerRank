#Welcome to NLP Using Python - Accessing Text Corpora

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
# Complete the 'accessTextCorpora' function below.
#
# The function accepts following parameters:
#  1. STRING fileid
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
# Complete the 'accessTextCorpora' function below.
#
# The function accepts following parameters:
#  1. STRING fileid
#  2. STRING word
#
from nltk.corpus import inaugural
def accessTextCorpora(fileid, word):
    # Write your code here
    
    # Task 1:
    # Compute the word coverage for the given 'field' associated with the text corpus 'Inaugural', and store the result into 'wordcoverage'. 
    
    text_to_word_list_convert =  inaugural.words(fileid)    
    wordfreq = nltk.FreqDist(text_to_word_list_convert)
    
    unique_word = wordfreq.items()
    unique_word_length = len(unique_word)    
    total_words = list(wordfreq.elements())
    total_words_length = len(list(wordfreq.elements()))
    
    wordcoverage = int(total_words_length/ unique_word_length)

    # Task 2:
    # Filter the words ending with 'ed' from the set of unique words for the given 'fileid' of 'Inaugural' corpus, and store it into 'ed_words' variable as a list.
    ed_words=   [  word for word in set(total_words) if word.endswith("ed") ]    
    
    # Task 3:
    # Convert all the words into 'lowercase'. Determine the frequency distribution of all the words having only alphabets for the given 'fileid' of 'Inaugural' corpus, and store it into a variable 'textfreq'. Find the frequency for the given 'word', and store it into 'wordfreq'.
    whole_word_lower= [  word.lower() for word in total_words  if word.isalpha()]   
    wordfreq=whole_word_lower.count(word)
    
    # Return wordcoverage, ed_words ,wordfreq
    return wordcoverage, ed_words ,wordfreq
    

if __name__ == '__main__':
    fileid = input()
    word = input()

    if not os.path.exists(os.getcwd() + "/nltk_data"):
        with zipfile.ZipFile("nltk_data.zip", 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())

    word_coverage, ed_words, word_freq = accessTextCorpora(fileid, word)

    print(word_coverage)
    print(sorted(ed_words))
    print(word_freq)