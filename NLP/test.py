import nltk 
nltk.download('punkt')
text = "Python is an interpreted high-level programming language for general-purpose programming. Created by Guido van Rossum and first released in 1991."
sentences = nltk.sent_tokenize(text)
print(len(sentences))