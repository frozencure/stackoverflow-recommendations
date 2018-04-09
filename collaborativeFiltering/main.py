import time
import numpy as np
import pandas as pd
from collaborativeFiltering.SparseDataframe import *

def loadFilteredVotes(path):
    start = time.time()
    df = pd.read_csv(path)
    print(len(df.index))
    end = time.time()
    total = end - start
    df['Vote'] = np.ones(shape=(len(df.index)))
    df = df[df.UserId != -1]
    print(total)
    return df



#df = loadFilteredVotes('C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/FilteredVotes.csv')
path = 'C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/filteredVotes.gz'
sparseDf = SparseDataframe(greaterThan=10, csvPath=path)
print(sparseDf.dataframe.head())
dict = sparseDf.getTopItemsCosineSim(postId=150505)
print(dict)