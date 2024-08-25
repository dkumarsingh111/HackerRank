import nltk

s = 'Python is awesome'
print(nltk.pos_tag(nltk.word_tokenize(s)))


#[('Python', 'NNP'), ('is', 'VBZ'), ('awesome', 'JJ')]