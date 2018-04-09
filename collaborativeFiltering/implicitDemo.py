from collaborativeFiltering.SparseDataframe import SparseDataframe
import implicit
import time

def demo():
    path = 'C:/Users/Iancu/PycharmProjects/Stackoverflow_Recommendations/stackoverflow-recommendations/resources/filteredVotes.gz'
    start = time.time()
    sparseDf = SparseDataframe(greaterThan=10, csvPath=path)
    model = implicit.als.AlternatingLeastSquares(factors=100, regularization=0.03)
    afterInit = time.time()
    print('After init %s' % (afterInit - start))
    model.fit(sparseDf.csrMatrix)
    fit = time.time()
    print('After fit %s' % (fit - start))
    print(sparseDf.getItemIndexById(5585779))
    predictedIndeces = model.similar_items(itemid=sparseDf.getItemIndexById(4105331))
    for tuple in predictedIndeces:
        print('Id: %s, Similarity: %s' %(sparseDf.getItemIdFromIndex(tuple[0]), tuple[1]))
    afterPredict = time.time()
    print('After predict %s' % (afterPredict - start))

if __name__ == '__main__':
    demo()