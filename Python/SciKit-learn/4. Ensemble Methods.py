# Welcome to Machine Learning Using Scikit-Learn | 4 | Ensemble Methods


#Write your code here
import numpy as np
from sklearn import datasets
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Task 1:
# Import numpy and set random seed to 100
np.random.seed(100)

# Load popular Boston Dataset from sklearn.datasets module and assign it to variable boston.
boston = datasets.load_boston()

# Split boston.data into two sets names X_train and X_test. 
# Also, split boston.target into two sets Y_train and  Y_test.
# Set random_state to 30.
X_train, X_test, Y_train, Y_test = train_test_split(boston.data,
boston.target,   random_state=30 )

# Print the shape of X_train dataset.
print(X_train.shape)

# Print the shape of X_test dataset.
print(X_test.shape)

# Task 2:
# Build a Random Forest Regressor model from X_train set and Y_train labels, with default parameters.
# Name the model as rf_reg
rfr = RandomForestRegressor()
rf_reg = rfr.fit(X_train, Y_train) 

# Evaluate the model accuracy on training data set and print it's score.
print(rf_reg.score(X_train, Y_train))

# Evaluate the model accuracy on testig data set and print it's score.
print(rf_reg.score(X_test, Y_test))

# Predict the housing price for first two samples of X_test set and print them.
print( rf_reg.predict(X_test[:2] ))

# Task 3:
# Build multiple Random forest Regressor on X_train set and  Y_train labels with max_depth parameters
# value changing from 3 to 5 and also setting n_estimators to  one of 50,100,200 values.
starting_index = 3
ending_index = 5

c_estimators = [50,100,200]
test_accuracy = []

# Evaluate each model accuracy on testing data set. Hint: Use for Loop.
for i in range(starting_index , ending_index+1):
    rfr = RandomForestRegressor(n_estimators =c_estimators[1] , max_depth=i)    
    #Fit the model
    rfr_fit= rfr.fit(X_train, Y_train)
    test_accuracy.append(rfr_fit.score(X_test, Y_test)) 

# Print the parameter value in the form of tuple (a,b).
# 'a' refers to max_depth value and 'b' refers to n_estimators.
index = test_accuracy.index(max(test_accuracy))+ starting_index
print((index,c_estimators[1]))