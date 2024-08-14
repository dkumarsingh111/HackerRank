# Welcome to Machine Learning Using Scikit-Learn | 1 | Preprocessing

#Write your code here
from sklearn import datasets
from sklearn import preprocessing
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import Imputer
import numpy as np

# Task 1:
# Load Popular iris data set from sklearn.datasets module and assign  it to variable 'iris'.
iris = datasets.load_iris()

# Perform Normalization on iris.data with l2 norm and save the transformed data in variable iris_normalized.
iris_normalized = preprocessing.Normalizer(norm= 'l2').fit(iris.data)
iris_normalized = iris_normalized.transform(iris.data)

# Print the mean of every column using the below command.
# print(iris_normalized.mean(axis=0))
print(iris_normalized.mean(axis=0))


# Task 2:
# Convert the categorical integer list iris.target into three binary attribute representation and store the result in variable 'iris_target_onehot'.
enc = preprocessing.OneHotEncoder()
iris_target_onehot = enc.fit_transform(iris.target.reshape(-1, 1))

# Execute the following print statement  print(iris_target_onehot.toarray()[[0, 50, 100]])
print(iris_target_onehot.toarray()[[0, 50, 100]])


# Task 3:
# Set first 50 row values of iris.data to Null values. Use numpy.nan.
iris.data[0:50, :]= np.nan

# Perform Imputation on 'iris.data' and save the transformed data in variable 'itis_imputed'
inputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0)
inputer = inputer.fit(iris.data)
iris_imputed = inputer.transform(iris.data)
"""Alternative way, use this only if above statement will not work:
imputer = SimpleImputer(missing_values='NaN', strategy='mean')
imputer = imputer.fit(iris.data)
iris_imputed = imputer.transform(iris.data)"""

# Print the mean of every column using the below command. 
# print(iris_imputed.mean(axis=0))
print(iris_imputed.mean(axis=0))
