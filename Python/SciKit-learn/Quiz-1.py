import sklearn.preprocessing as preprocessing

x = [[7.8], [1.3], [4.5], [0.9]]
print(preprocessing.Binarizer().fit(x).transform(x).shape)


#Output: (4, 1)