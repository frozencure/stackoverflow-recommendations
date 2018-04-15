import time
import numpy as np
import pandas as pd
from SparseDataframe import *
import os
import pathlib

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

def getPath():
    repo_path = str(pathlib.Path(os.getcwd()).parent)
    return repo_path + '/resources/filteredVotes.gz'



#df = loadFilteredVotes('C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/FilteredVotes.csv')
#
# path = getPath()
# sparseDf = SparseDataframe(greaterThan=10, csvPath=path, hasItemsAsRows=False)
# print(sparseDf.dataframe.head())
# dict = sparseDf.getTopItemsCosineSim(postId=150505)
# print(dict)