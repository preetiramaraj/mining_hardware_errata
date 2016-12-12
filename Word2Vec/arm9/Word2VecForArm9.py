import csv
from gensim.models.word2vec import Word2Vec
from nltk.corpus import stopwords
from collections import Counter
import re
import numpy as np
with open('ARM9.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    sentences = []
    i = 0
    for row in reader:
#['0Chip','1Details','2Core','3Errata ID','4Module','5Criticality','6Workaround','Revisions Impacted','8Failure','9Fix Status','Masks Affected','11Manufacturer']
        sentences.append(row[8])
        sentences.append(row[1])
        sentences.append(row[6])

sentences = [re.sub("[^a-zA-Z.]"," ", x) for x in sentences]
stops = set(stopwords.words("english"))
vectors = [x.lower().split() for x in sentences]
detailed_vectors = [[w for w in list_w if not w in stops] for list_w in vectors]
list_of_words = [word for word_list in detailed_vectors for word in word_list]
counts_words = Counter(list_of_words)
print str([x[0] for x in counts_words.most_common(100)])
print
print str(counts_words.most_common(100))

# Training word2vec model

model = Word2Vec(detailed_vectors,size=100,window=5,min_count=5)
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
model.save('Failure_workaround.model')
