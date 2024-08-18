import nltk 
nltk.download('punkt')
text = "Python is an interpreted high-level programming language for general-purpose programming. Created by Guido van Rossum and first released in 1991."
sentences = nltk.sent_tokenize(text)
words = nltk.word_tokenize(text)
print(sentences)
print(words)


wordfreq = nltk.FreqDist(words)
print(wordfreq.most_common(2))