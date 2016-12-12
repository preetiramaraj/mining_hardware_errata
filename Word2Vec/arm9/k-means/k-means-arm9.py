from gensim.models import Word2Vec
from sklearn.cluster import KMeans
import numpy as np
import time

start = time.time()

model = Word2Vec.load('Failure_workaround.model')
# Code reference: http://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-3-more-fun-with-word-vectors


# Set k (num_cluster) to be average of 5 words per cluster
word_vectors = model.syn0
#num_clusters = 15
num_clusters = 100

# Initializing k-means
kmeans_clustering = KMeans( n_clusters = num_clusters)
idx = kmeans_clustering.fit_predict(word_vectors)

end = time.time()
print "Time elapsed is", str(end-start),"seconds."

# Creating a word/index dictionary mapping word to cluster number
word_centroid_map = dict(zip( model.index2word, idx))
print len(idx)
for cluster in range(len(idx)):#xrange(0,20):
    print "\nCluster ",str(cluster)
    words = []
    for i in xrange(0, len(word_centroid_map.values())):
        if( word_centroid_map.values()[i] == cluster):
            words.append(word_centroid_map.keys()[i])
    print words