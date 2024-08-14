# Welcome to Machine Learning Using Scikit-Learn | 2 | Nearest Neighbors


#Write your code here
from sklearn import datasets
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Task 1:
# Import popular iris data set from the sklearn.datasets module and  assign it to variable iris.
iris = datasets.load_iris()

# Split iris.data into two sets names X_train, X_test. 
# Also, split iris.target into two sets  Y_train, Y_test. Set the random_state to 30.
X_train, X_test, Y_train, Y_test = train_test_split(iris.data, iris.target,
stratify=iris.target, random_state=30)

# Print the shape of X_trian dataset.
# Print the shape of X_test dataset.
print(X_train.shape)
print(X_test.shape)

# Task 2
# Fit K nearest neighbors model on X_train data and Y_train labels, with default parameters.
# Name the model as knn_clf
knn_classifier = KNeighborsClassifier()  
knn_clf = knn_classifier.fit(X_train, Y_train) 

# Evaluate the model accuracy on training data set and print it's score.
# Evaluate the model accuracy on testing data set and print it's score.
print(knn_clf.score(X_train,Y_train))
print(knn_clf.score(X_test,Y_test))


# Task 3:
# Fit multiple K nearest neighbors models on X_train data and Y_train labels with
#  n_neighbors parameters value changing from 3 to 10.
starting_index = 3
ending_index = 10
neighbors = np.arange(starting_index, ending_index)
train_accuracy =np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

# Evaluate each model accuracy on testing data set. Hint: Use for loop.
for i,k in enumerate(neighbors):
    #Setup a knn classifier with k neighbors
    knn = KNeighborsClassifier(n_neighbors=k)
    
    #Fit the model
    knn.fit(X_train, Y_train)
    
    #Compute accuracy on the training set
    train_accuracy[i] = knn.score(X_train, Y_train)
    
    #Compute accuracy on the test set
    test_accuracy[i] = knn.score(X_test, Y_test) 

index_of_max_accuracy = list(np.where(test_accuracy== max(test_accuracy)))

# Print the n_neighbors value of the model with highest  accuracy.
f = index_of_max_accuracy[0][0]+starting_index
print(f)
   