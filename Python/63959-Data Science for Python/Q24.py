import pandas as pd

A = pd.Series([2, 4, 6], index = [0, 1, 2])
B = pd.Series([1, 3, 5], index = [1, 2, 3])
print(A)
print(B)
C=A+B
print(C)
print(C[1])


#Output: 5.0