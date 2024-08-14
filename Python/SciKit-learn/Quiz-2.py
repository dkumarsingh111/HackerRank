import sklearn.preprocessing as preprocessing

x = [[0, 0], [0, 1], [1,0]]
enc = preprocessing.OneHotEncoder()
print(enc.fit(x).transform([[1, 1]]).toarray())


#Output: [[0. 1. 0. 1.]]