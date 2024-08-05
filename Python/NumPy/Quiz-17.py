#What is the output of the following code?


import numpy as np

x = np.array([[0, 1], [1, 1], [2, 2]])
y = x.sum(-1)
print(x[y < 2, :])





#Output: [[0 1]]