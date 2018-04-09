import pandas as pd
import itertools

def recursive_len(item):
    try:
        iter(item)
        return sum(recursive_len(subitem) for subitem in item)
    except TypeError:
        return 1

x = pd.Series([[1, (2,5,6)], [2, (3,4)], [3, 4], [(5,6), (7,8,9)]])
df = pd.DataFrame({'A': x})
print(df.head())
df['Length'] = df['A'].apply(recursive_len)

print(df)
