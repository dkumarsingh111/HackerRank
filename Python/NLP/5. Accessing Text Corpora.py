#Welcome to NLP Using Python - Accessing Text Corpora

#!/bin/python3

import math
import os
import random
import re
import sys
import nltk


#
# Complete the 'createUserTextCorpora' function below.
#
# The function accepts following parameters:
#  1. STRING filecontent1
#  2. STRING filecontent2
#
# from nltk.corpus import inaugural
from nltk.corpus import PlaintextCorpusReader
def createUserTextCorpora(filecontent1, filecontent2):
    # Write your code here

    # Task 1:
    # Create a text file name called 'content1.txt', and write content 'filecontent1' inside the nltk_data folder.
    #
    with open(os.path.join('nltk_data/', 'content1.txt'), "w") as f:
        f.write(filecontent1)
        f.close()
    
    # Task 2:
    # Create a text file name called 'content2.txt', and write content 'filecontent2' inside the nltk_data folder.
    #
    with open(os.path.join('nltk_data/', 'content2.txt'), "w") as f2:
        f2.write(filecontent2) 
        f2.close() 
     
    # Task 3:
    # Convert your collection of text files inside the 'nltk_data' folder into a text corpus, store it into the 'text_corpus' variable.
    #
    corpus_root_directory = 'nltk_data/'
    text_corpus = PlaintextCorpusReader(corpus_root_directory,r'.*\.txt')
    
    
    p1= text_corpus.words('content1.txt')
    p2= text_corpus.words('content2.txt')
    
    # Task 4:
    # Compute the number of words and number of unique words of all the file IDs associated with the text corpus,
    # And store into 'no_of_words_corpus1', 'no_of_unique_words_corpus1', 'no_of_words_corpus2', 'no_of_unique_words_corpus2', variable.
    #
    wordfreq = nltk.FreqDist(p1)
    g= list(wordfreq.elements())

    no_of_words_corpus1 = len(g)
    no_of_unique_words_corpus1 =  len(set(g))
    
    wordfreq2 = nltk.FreqDist(p2)
    g2= list(wordfreq2.elements())
    no_of_words_corpus2 =  len(g2)
    no_of_unique_words_corpus2 =  len(set(g2))
    
    return text_corpus, no_of_words_corpus1, no_of_unique_words_corpus1, no_of_words_corpus2, no_of_unique_words_corpus2
       
    

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