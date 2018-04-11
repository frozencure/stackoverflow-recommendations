import numpy as np
from lightfm import LightFM
from lightfm.evaluation import precision_at_k
from lightfm.evaluation import auc_score
from lightfm.evaluation import recall_at_k

from lightfm.datasets import fetch_movielens

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



movielens = fetch_movielens()

for key, value in movielens.items():
    print(key, type(value), value.shape)

train = movielens['train']
test = movielens['test']

model = LightFM(learning_rate=0.05, loss='bpr', no_components=1)
model.fit(train, epochs=10)
#predictions = model.predict(user_ids=2, item_ids=np.arange(1681))
# print(np.sort(predictions))
items = model.item_embeddings[0,:]
item_repr = model.get_item_representations()[1]
print(len(item_repr))
# print(movielens['item_labels'][0])
# tuples = similar_items(0, train.tocsr().getcol(0), model)
# print(tuples)
# for tuple in tuples:
#     print(movielens['item_labels'][tuple[0]])
#
train_precision = precision_at_k(model, train, k=10).mean()
test_precision = precision_at_k(model, test, k=10).mean()

train_auc = auc_score(model, train).mean()
test_auc = auc_score(model, test).mean()

train_recall = recall_at_k(model, train).mean()
test_recall = recall_at_k(model, test).mean()

print('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
print('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))
print('Recall: train %.2f, test %.2f.' % (train_recall, test_recall))
