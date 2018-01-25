import pandas as pd
import collaborativeFiltering.loadData as data
from scipy import sparse

def buildMatrix():
    df = data.loadFromCsv(data.path)
    matrix = sparse.csr_matrix([df['UserId'], df['PostId'], df['Vote']])
    return matrix
print(buildMatrix().size)