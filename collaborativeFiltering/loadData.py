import pandas as pd
import time
import numpy as np
from scipy import sparse

path = 'C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/Votes.csv'

def loadFilteredVotes(path):
    start = time.time()
    df = pd.read_csv(path)
    print(len(df.index))
    end = time.time()
    total = end - start
    df['Vote'] = np.ones(shape=(len(df.index)))
    df = df[df.UserId != -1]
    print(total)
   # print(df.head())
    return df

def createMatrix(df):
   # df = df.drop(df.index[10000:])
    df = df.to_sparse()
    print(df.head())
    newDf = df.pivot_table(index = ['UserId'], columns=['PostId'], values='Vote', fill_value = 0)
    print(len(newDf.index))
    newDf = newDf[(newDf != 0).any(1)]
    print(len(newDf.index))
    print(newDf.head(10))
    print(len(newDf.index))
    return newDf

def calculateCorreletions(df, postId):
    ratings = df[postId]
    similarItems = df.corrwith(ratings)
    similarItems = similarItems.dropna()
    #similarItems = similarItems.sort_values(ascending= False)
    newdf = pd.DataFrame(similarItems)
    newdf = newdf.sort_values(by = 0, ascending=False)
    print(newdf.head(10))
    return newdf


def loadFromCsv(csvPath):
    start = time.time()
    df = pd.read_csv(csvPath)
    df['UserId'] = df['UserId'].astype(int)
    end = time.time()
    total = end - start
    df = df.dropna(axis = 0, how= 'any')
    df = df.reset_index()
    df['Vote'] = np.ones(shape=(len(df.index)))
    print(len(df.index))
    print(df.head())
    print(total)
    return df

def writeToCsv(df, path):

    df.to_csv(path_or_buf=path, columns= ['PostId', 'UserId'], index=False)


def countFavourites(df, greaterThan):
    newDf = df.dropna(axis = 0, how = 'any')
    counts = newDf.PostId.value_counts()
    #print(counts.head(25))
    filteredCounts = counts[counts >= greaterThan]
    #print(filteredCounts.count)
    return filteredCounts

def removeLowVotes(df, greaterThan):
    willKeepItems = countFavourites(df, greaterThan)
    df = df[df['PostId'].isin(willKeepItems.index.tolist())]
    #print(df[df['PostId'] == 4754152])
    #print(df.head())
    return df

def countUserVotes(df, smallerThan):
    newDf = df.dropna(axis=0, how='any')
    counts = newDf.UserId.value_counts()
    #print(counts.head(25))
    filteredCounts = counts[counts < smallerThan]
    #print(filteredCounts.count)
    return filteredCounts

def removeTooManyFavourites(df, smallerThan):
    willKeepItems = countUserVotes(df, smallerThan)
    df = df[df['UserId'].isin(willKeepItems.index.tolist())]
    #print(df.head())
    return df


df = loadFilteredVotes('C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/FilteredVotes.csv')
filteredDf = removeLowVotes(df, 80)
filteredDf = removeTooManyFavourites(filteredDf, 30)
print(filteredDf.shape)
matrix = createMatrix(filteredDf)
#calculateCorreletions(matrix, 4754152)