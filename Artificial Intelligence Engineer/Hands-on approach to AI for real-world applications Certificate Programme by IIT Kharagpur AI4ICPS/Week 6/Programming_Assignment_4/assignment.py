# ==========================================================
# IIT KHARAGPUR AI4ICPS HUB FOUNDATION
# Hands-on Approach to AI, Cohort-4, November 2025
# Programming Assignment 4
# Assignment submitted by Deepak Singh
# ==========================================================

"""
This program finds the best value of K in KMeans algorithm using Silhouette Coefficient for 'housing.csv' dataset. The range of K values to analyze is provided as a command line parameter.
Syntax: python template.py <number> <number>

For example, to search best K between 3 and 6 the command line input should be:
python template.py 3 6
"""

# importing the libraries

"""  DO NOT MODIFY  """
import sys
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
"""  DO NOT MODIFY  """

def find_best_kmeans(data, min_k, max_k):

    """  write from here  """

        # Initialize the K-Means model
        # Use the data and calculate Silhouette Coefficient for the range of K provided
        # Return the best K with respect to Silhouette Coefficient 

    X = data.select_dtypes(include=['number']).dropna()

    if X.shape[0] == 0 or X.shape[1] == 0:
        return -1

    best_k = None
    best_score = -1.0  # silhouette score ranges from -1 to 1

    n_samples = X.shape[0]

    for k in range(min_k, max_k + 1):
        if k < 2 or k >= n_samples:
            continue

        kmeans = KMeans(n_clusters=k, n_init='auto', random_state=0)

        labels = kmeans.fit_predict(X)

        try:
            score = metrics.silhouette_score(X, labels)
        except Exception:
            continue

        if score > best_score:
            best_score = score
            best_k = k

    if best_k is None:
        return -1

    return best_k
        
    """        End        """


"""  DO NOT MODIFY  """
if __name__ == '__main__':

    """
    ALERT: * * * No changes are allowed in this section  * * *
    """
 
    if len(sys.argv) == 2:
        print("Usage: python assignment.py <number> <number>")
        sys.exit(1)

    input_data_one = sys.argv[1].strip()
    input_data_two = sys.argv[2].strip()
    
    """  Call to function that will perform the computation. """
    if input_data_one.isdigit() and input_data_two.isdigit():

        min_k = int(input_data_one)
        max_k = int(input_data_two)
        if min_k>=2 and max_k>min_k:
            data =pd.read_csv("./housing.csv")
            print(find_best_kmeans(data, min_k, max_k)) 
        else:
           print("Invalid input")
    else:
        print("Invalid input")
 
    
    """ End to call """