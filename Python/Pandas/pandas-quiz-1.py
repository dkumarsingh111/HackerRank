import pandas as pd

s = pd.Series([89.2, 76.4, 98.2, 75.9], index=list('abcd'))
print(s[['c', 'a']])