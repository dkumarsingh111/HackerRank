import pandas as pd

leaders = pd.Series(['Donald Trump', 'Narendra Modi', 'Boris Johnson', 'Angela Merkel', 'Vladimir Putin', 'Xi Jinping'])
name = leaders.str.extract('([A-Za-z]+)')
print(name[:1])

#Output:
#         0
# 0  Donald