#What is the output of the following code?

import numpy as np

x = np.arange(30).reshape(5,6)
print(x.argmax(axis=1))

#Output: [5 5 5 5 5]