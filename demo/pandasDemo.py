import pandas as pd
import time

start = time.time()
df = pd.read_csv('C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/resources/Votes.csv')
end = time.time()
total = end - start
print(total)
print(df.count)
newDf = df.dropna(axis = 0, how = 'any')
counts = newDf.PostId.value_counts()

print(counts.head(25))
filteredCounts = counts[counts >= 100]
print(filteredCounts.count)