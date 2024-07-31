#What is the output of the following code?

import numpy as np

x = np.arange(4).reshape(2,2)

y = np.vsplit(x,2)
print(y[0])