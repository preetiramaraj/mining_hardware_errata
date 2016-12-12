import csv
from gensim.models import doc2vec
from nltk.corpus import stopwords
from collections import Counter
import re
import numpy as np

# Code reference: https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/test/test_doc2vec.py

with open('../ARM9.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    # omitting headers
    reader.next()
    sentences = []
    #['0Chip','1Details','2Core','3Errata ID','4Module','5Criticality','6Workaround','Revisions Impacted','8Failure','9Fix Status','Masks Affected','11Manufacturer']
    raw_sentences = [' '.join((row[8], row[1],row[6])).lower().split() for row in reader]
    

raw_sentences = [re.sub("[^a-zA-Z.]"," ", x) for x in raw_sentences]
stops = set(stopwords.words("english"))
vectors = [x.lower().split() for x in raw_sentences]
detailed_vectors = [[w for w in list_w if not w in stops] for list_w in vectors]
sentences =[doc2vec.TaggedDocument(val), [row[11].lower()]) for i,val  in enumerate(detailed_vectors)]

# Training doc2vec model
model = doc2vec.Doc2Vec(sentences,size=300,window=8,min_count=5,dm=0)
alpha, min_alpha, passes = (0.025, 0.001, 20)
alpha_delta = (alpha - min_alpha) / passes

for epoch in range(passes):
    model.alpha, model.min_alpha = alpha, alpha
    model.train(sentences)

    #print('completed pass %i at alpha %f' % (epoch + 1, alpha))
    alpha -= alpha_delta

    np.random.shuffle(sentences)

# This is the final model hence init_sims makes it more efficient
model.init_sims(replace=True)
model.save('Doc2Vec_Failure_Workaround.model')