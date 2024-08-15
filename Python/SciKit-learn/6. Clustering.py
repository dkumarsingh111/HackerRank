# Welcome to Machine Learning Using Scikit-Learn | 6 | Clustering

#Write your code here
from sklearn import metrics
from sklearn import datasets
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering 
from sklearn.cluster import AffinityPropagation
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.metrics import homogeneity_score

# Task 1
iris = load_iris()

km_cls = KMeans(n_clusters=3, random_state=42)
km_labels = km_cls.fit_predict(iris.data)

km_h_score = homogeneity_score(iris.target, km_labels)

print('{:.4f}'.format(km_h_score))

# Task 2
agg_cls = AgglomerativeClustering(n_clusters=3)
agg_labels = agg_cls.fit_predict(iris.data)

agg_h_score = homogeneity_score(iris.target, agg_labels)

print('{:.4f}'.format(agg_h_score))

# Task 3
af_cls = AffinityPropagation()
af_labels = af_cls.fit_predict(iris.data)

af_h_score = homogeneity_score(iris.target, af_labels)

print('{:.4f}'.format(af_h_score))