import csv
from gensim.models.word2vec import Word2Vec
from nltk.corpus import stopwords
from collections import Counter
import re
import numpy as np

# T-sne reference: https://raw.githubusercontent.com/devmount/GermanWordEmbeddings/master/visualize.py
sentences = []
with open('../CortexA9.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
# 'Criticality', '1Manufacturer', '2Chip', 'Linux_BSP_Status', 'Revisions Impacted', '5Workaround', '6Failure', '7Details', 'Fix Status', '9Core', 'Error Category'
        sentences.append(row[5])
        sentences.append(row[6])
        sentences.append(row[7])

with open('../CortexA8.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
    #[Revisions Impacted', 'Manufacturer', '2Chip', '3Details', '4Workaround', '5Fail       ure', 'Fix Status', 'Core']
        sentences.append(row[3])
        sentences.append(row[4])
        sentences.append(row[5])


sentences = [re.sub("[^a-zA-Z.]"," ", x) for x in sentences]
stops = set(stopwords.words("english"))
vectors = [x.lower().split() for x in sentences]
detailed_vectors = [[w for w in list_w if not w in stops] for list_w in vectors]
list_of_words = [word for word_list in detailed_vectors for word in word_list]
counts_words = Counter(list_of_words)

print str([x[0] for x in counts_words.most_common(500)])
print
print str(counts_words.most_common(500))

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
model.save('Cortex_Failure_workaround.model')