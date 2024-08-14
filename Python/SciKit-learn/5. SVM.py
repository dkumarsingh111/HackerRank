# Welcome to Machine Learning Using Scikit-Learn | 5 | SVM


#Write your code here
import numpy as np
from sklearn import datasets
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import sklearn.preprocessing as preprocessing

# Task 1: 
# Load popular digits dataset from sklearn.datasets module  and assign it to variable digits.
digits = datasets.load_digits()

# Split digits.data into two sets names X_train and X_test. 
# Also, split boston.target into two sets Y_train and  Y_test.
# Set random_state to 30.
X_train, X_test, Y_train, Y_test = train_test_split(digits.data,
digits.target, stratify= digits.target,  random_state=30 )

# Print the shape of X_train dataset.
print(X_train.shape)

# Print the shape of X_test dataset.
print(X_test.shape)


# Task 2:
# Build an SVm classifier from X_train set and Y_train labels,  with  default parameters. 
# Name the model as svm_clf
svm_classifier = SVC()
svm_clf = svm_classifier.fit(X_train, Y_train) 

# Evaluate the model accuracy on testing data set and print it's score.
print( svm_clf.score(X_test, Y_test))


# Task 3:
# Perform StandardScaler of digits.data and store the transformed data in variable digits_standardized.
pss = preprocessing.StandardScaler()
pas = pss.fit(digits.data)
digits_standardized = pss.transform(digits.data)

# Again, Split digits_standardized into two sets names X_train and X_test. 
# Also, split digits.target into two sets Y_train and  Y_test.
# Set random_state to 30; and perform stratified sampling.
X_train, X_test, Y_train, Y_test = train_test_split(digits_standardized,
digits.target, stratify= digits.target,  random_state=30 )

# Build another SVM classifier from X_train set and Y_train labels, with default parameters.
# Name the model as svm_clf2.
svm_clf2 = svm_classifier.fit(X_train, Y_train) 

# Evaluate the model accuracy on testing data set and print it's score.
print(svm_clf2.score(X_test, Y_test))