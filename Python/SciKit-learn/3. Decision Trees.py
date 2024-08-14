# Welcome to Machine Learning Using Scikit-Learn | 3 | Decision Trees


#Write your code here
import numpy as np
from sklearn import datasets
from sklearn import model_selection
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

# Task 1:
# Import numpy and set random seed to 100.
np.random.seed(100)

# Load popular Boston dataset from sklearn.datasets module and assign it to variable boston.
boston = datasets.load_boston()

# Split boston.data into two sets names  X_train X_test. Also, split boston.target into two sets Y_train and Y_test.
# Set random_state to 30.
X_train, X_test, Y_train, Y_test = train_test_split(boston.data,
boston.target, random_state=30)

# Print the shape of X_train dataset.
# Print the shape of X_test dataset.
print(X_train.shape)
print(X_test.shape)


# Task 2:
# Build a Decision tree Regressor model from X_train set  and Y_train labels, with default parameters.
# Name the model as dt_reg.
dt_reg = DecisionTreeRegressor()
dt_reg = dt_reg.fit(X_train, Y_train)

# Evaluate the model accuracy on training data set and print it's score.
print( dt_reg.score(X_train, Y_train))

# Evaluate the model accuracy on testing data set and print it's score.
print( dt_reg.score(X_test, Y_test))

# predict the housing proce for first two samples of X_test set and print them. (Hint: Use predict( function.)
print( dt_reg.predict(X_test[:2] ))


# Task 3:
# Fit multiple Decision tree regressors on X_train data and Y_train labels with max_depth parameters values changing from 2 to 5.
starting_index = 2
ending_index = 5

# Evaluate each model accuracy on testing data set. Hint: Make use of for loop.
test_accuracy = []
for i in range(starting_index , ending_index):
    knnn = DecisionTreeRegressor(max_depth = i)    
    #Fit the model
    knn= knnn.fit(X_train, Y_train)
     
    #Compute accuracy on the test set
    test_accuracy.append(knn.score(X_test, Y_test)) 


# Print the max_depth value of the model with highest accuracy.
print(test_accuracy.index(max(test_accuracy))+ starting_index)