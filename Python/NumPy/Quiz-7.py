#What is the output of the following code?


import numpy as np

x = np.arange(4).reshape(2,2)
print(np.isfinite(x))

#Output: [[ True  True] 
#         [ True  True]]