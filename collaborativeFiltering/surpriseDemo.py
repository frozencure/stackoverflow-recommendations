from collaborativeFiltering.SparseDataframe import SparseDataframe

from surprise import Reader, Dataset
from surprise.prediction_algorithms import knns
from surprise.model_selection import cross_validate
from . import main


def demo():
    path = main.getPath()
    sparseDf = SparseDataframe(greaterThan=100, csvPath=path)
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(sparseDf.dataframe[['UserId', 'PostId', 'Votes']], reader)
    trainset = data.build_full_trainset()
    sim_options = {'name':'cosine', 'user_based': False}
    algo = knns.KNNBaseline(sim_options=sim_options)
    algo.fit(trainset)
    
if __name__ == '__main__':
    demo()