import pandas as pd

choices = pd.Series([1, 2, 3, 4, 5, 6])

draws = choices.sample(n=10, replace=True)

print (draws)

#Output:
# 2    3
# 2    3
# 1    2
# 3    4
# 1    2
# 0    1
# 0    1
# 2    3
# 5    6
# 5    6
# dtype: int64