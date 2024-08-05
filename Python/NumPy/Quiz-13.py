#What is the output of the following code?

import numpy as np

x = np.arange(30).reshape(3,5,2)
print(x[-1, 2:-1, -1])


#Output: [25 27]