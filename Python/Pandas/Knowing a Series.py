import pandas as pd
import numpy as np
temp = pd.Series(28 + 10*np.random.randn(10))
print(temp.describe())