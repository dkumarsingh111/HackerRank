from nltk.book import *
import nltk

text1: "Moby Dick by Herman Melville 1851 - text2: Sense and Sensibility by Jane Austen 1811 - text3: The Book of Genesis - text4: Inaugural Address Corpus - text5: Chat Corpus - text6: Monty Python and the Holy Grail - text7: Wall Street Journal - text8: Personals Corpus - text9: The Man Who Was Thursday by G . K . Chesterton 1908"

print(type(text1))


#Determining Total Word Count
n_words = len(text1)
print(n_words) #260819

#Determining Unique Word Count
n_unique_words = len(set(text1))
print(n_unique_words) #19317


#Transforming Words
text1_lcw = [ word.lower() for word in set(text1) ]
n_unique_words_lc = len(set(text1_lcw))
print(n_unique_words_lc)  #17231

#Determining Word Coverage
word_coverage1 = n_words / n_unique_words
print(word_coverage1)


word_coverage2 = n_words / n_unique_words_lc
print(word_coverage2)


#Filtering Words
big_words = [word for word in set(text1) if len(word) > 15 ]
print(big_words)

sun_words = [word for word in set(text1) if word.startswith('Sun') ]
print(sun_words)

#Frequency Distribution
text1_freq = nltk.FreqDist(text1)
print(text1_freq['Sunday'])

#Now let's identify three frequent words from text1_freq distribution using most_common method.
top3_text1 = text1_freq.most_common(3)
print(top3_text1)

large_uncommon_words = [word for word in text1 if word.isalpha() and len(word) > 7 ]
text1_uncommon_freq = nltk.FreqDist(large_uncommon_words)
print(text1_uncommon_freq.most_common(3))