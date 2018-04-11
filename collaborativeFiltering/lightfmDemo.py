from lightfm import LightFM
from lightfm import cross_validation
from lightfm.evaluation import precision_at_k,auc_score, recall_at_k
from collaborativeFiltering.main import getPath
from collaborativeFiltering.SparseDataframe import SparseDataframe
import logging
import time






if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    path = getPath()
    sparseDf = SparseDataframe(greaterThan=10, csvPath=path)
    print(sparseDf.dataframe.head())
    logging.info('Matrix created, size: %s' % (sparseDf.csrMatrix.shape,))
    (train, test) = cross_validation.random_train_test_split(interactions=sparseDf.csrMatrix, test_percentage=0.2)
    logging.info('Cross validation split done')

    model = LightFM(learning_rate=0.05, loss='bpr')
    model.fit(train, epochs=10)
    logging.info('Model fit done')

    train_precision = precision_at_k(model, train, k=5).mean()
    logging.info('Train precision computed')
    test_precision = precision_at_k(model, test, k=5).mean()
    logging.info('Test precision computed')

    train_auc = auc_score(model, train).mean()
    logging.info('Train auc computed')
    test_auc = auc_score(model, test).mean()
    logging.info('Test auc computed')


    train_recall = recall_at_k(model, train).mean()
    logging.info('Train recall computed')
    test_recall = recall_at_k(model, test).mean()
    logging.info('Test recall computed')

    logging.info('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
    logging.info('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))
    logging.info('Recall: train %.2f, test %.2f.' % (train_recall, test_recall))


