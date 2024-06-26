import numpy as np

a = np.arange(1,10).reshape(3,3)

a.sum(axis=0)

print(a)

# Output:
#         [[[1 2 3] 
#         [4 5 6] 
#         [7 8 9]]