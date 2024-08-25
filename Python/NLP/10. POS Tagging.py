#Welcome to NLP Using Python - POS Tagging

#!/bin/python3


#
# Complete the 'tagPOS' function below.
#
# The function accepts following parameters:
#  1. STRING textcontent
#  2. STRING taggedtextcontent
#

import math
import os
import random
import re
import sys
import zipfile
os.environ['NLTK_DATA'] = os.getcwd() + "/nltk_data"
from nltk.corpus import brown
import nltk



#
# Complete the 'tagPOS' function below.
#
# The function accepts following parameters:
#  1. STRING textcontent
#  2. STRING taggedtextcontent
#

def tagPOS(textcontent, taggedtextcontent, defined_tags):
    # Write your code here
    
    # Task 1:
    # Tag the part of speech for the given 'textcontent' words, store the result into the variable 'nltk_pos_tags'.
    words = nltk.word_tokenize(textcontent)    
    nltk_pos_tags= nltk.pos_tag(words)
    
    # Task 2:
    # Tag the part of speech for the given 'taggedtextcontent' words using the 'Tagged Text method'. Store the result into the variable 'tagged_pos_tag'.
    tagged_pos_tag =  [ nltk.tag.str2tuple(word) for word in taggedtextcontent.split() ]
    
    # Task 3:
    # Tag the part of speech for the given 'textcontent' words and use 'defined_tags' as a model in the 'Lookup Tagger method'. Store the result into the variable 'unigram_pos_tag'.
    #
    words = nltk.word_tokenize(textcontent)
    baseline_tagger = nltk.UnigramTagger(model=defined_tags)
    
    unigram_pos_tag = baseline_tagger.tag(words) 
    
    return nltk_pos_tags, tagged_pos_tag, unigram_pos_tag

if __name__ == '__main__':
    textcontent = input()

    taggedtextcontent = input()
    
    if not os.path.exists(os.getcwd() + "/nltk_data"):
        with zipfile.ZipFile("nltk_data.zip", 'r') as zip_ref:
            zip_ref.extractall(os.getcwd())

    defined_tags = dict(brown.tagged_words(tagset='universal'))

    nltk_pos_tags, tagged_pos_tag, unigram_pos_tag = tagPOS(textcontent, taggedtextcontent, defined_tags)

    print(nltk_pos_tags)
    print(tagged_pos_tag)
    print(unigram_pos_tag)
