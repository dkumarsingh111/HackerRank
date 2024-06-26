import pandas as pd

date = pd.to_datetime("4th of July, 2019")
result = date.strftime('%A')
print(result)

#Output: Thursday