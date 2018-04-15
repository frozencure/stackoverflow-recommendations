from lightfm import LightFM
from lightfm import cross_validation
from lightfm.evaluation import precision_at_k, auc_score, recall_at_k
from main import getPath
from SparseDataframe import SparseDataframe
import logging
import numpy as np
import time


def similar_items(item_id, item_features, model, N=10):
    (item_biased, item_representations) = model.get_item_representations(features=item_features)
    # Cosine similarity
    scores = item_representations.dot(item_representations[item_id])
    item_norms = np.linalg.norm(item_representations, axis=1)
    item_norms[item_norms == 0] = 1e-10
    scores /= item_norms
    best = np.argpartition(scores, -N)[-N:]
    return sorted(zip(best, scores[best] / item_norms[item_id]),
                  key=lambda x: -x[1])

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')
    path = getPath()
    sparseDf = SparseDataframe(greaterThan=10, csvPath=path, hasItemsAsRows=False)
    print(sparseDf.dataframe.head())
    logging.info('Matrix created, size: %s' % (sparseDf.csrMatrix.shape,))
    (train, test) = cross_validation.random_train_test_split(interactions=sparseDf.csrMatrix, test_percentage=0.2 )
    logging.info('Cross validation split done')

    model = LightFM(learning_rate=0.03, loss='bpr', no_components=50)
    model.fit_partial(train)
    logging.info("Model first partial fit done")
    test_precision = precision_at_k(model, test, k=5).mean()
    prev_prec = test_precision
    epoch = 1
    while test_precision >= prev_prec:
        logging.info('Epoch: %s, Test prec: %.2f' % (epoch,test_precision))
        prev_prec = test_precision
        test_precision = precision_at_k(model, test, k=5).mean()
    # logging.info('Model fit done')
    # similarItems = similar_items(item_id=sparseDf.getItemIndexById(4105331), item_features=None, model=model)
    # for tuple in similarItems:
    #     print('Item id: %s, Accuracy: %s' % (sparseDf.getItemIdFromIndex(tuple[0]), tuple[1]))





    train_precision = precision_at_k(model, train, k=5).mean()
    logging.info('Train precision computed')
    test_precision = precision_at_k(model, test, k=5).mean()
    logging.info('Test precision computed')
    logging.info('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
    #
    train_auc = auc_score(model, train).mean()
    logging.info('Train auc computed')
    test_auc = auc_score(model, test).mean()
    logging.info('Test auc computed')
    logging.info('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))


    train_recall = recall_at_k(model, train, k=5).mean()
    logging.info('Train recall computed')
    test_recall = recall_at_k(model, test, k=5).mean()
    logging.info('Test recall computed')
    logging.info('Recall: train %.2f, test %.2f.' % (train_recall, test_recall))


