from sklearn.feature_extraction.text import CountVectorizer

document = ["One Geek helps Two Geeks", "Two Geeks help Four Geeks", "Each Geek helps many other Geeks at GeeksforGeeks."]

#Create a Vectorizer Object
vect = CountVectorizer()

vect.fit(document)

print("Vocabulary:", vect.vocabulary_)

vector = vect.transform(document)

print("Encoded document is:")
print(vector.toarray())