import pandas as pd

result = pd.date_range("2020-01-01", "2020-12-01", freq="BM")

print(result)