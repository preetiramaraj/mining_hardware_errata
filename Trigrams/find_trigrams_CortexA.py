import nltk 
import collections
import re
import csv
from nltk.corpus import stopwords
import nltk


failure_details_list = []
workaround_list = []
manufacturer = [] # keeping track of manufacturer for each column from above

with open('CortexA9.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
    # 'Criticality', '1Manufacturer', '2Chip', 'Linux_BSP_Status', 'Revisions Impacted', '5Workaround', '6Failure', '7Details', 'Fix Status', '9Core', 'Error Category'
        workaround_list.append(row[5])
        failure_details_list.append(' '.join((row[6],row[7])))
        manufacturer.append(row[1])

with open('CortexA8.csv') as f:
    reader  = csv.reader(f, delimiter='\t')
    reader.next()
    for row in reader:
    #[Revisions Impacted', 'Manufacturer', '2Chip', '3Details', '4Workaround', '5Fail       ure', 'Fix Status', 'Core']
        failure_details_list.append(' '.join((row[5],row[3])))
        workaround_list.append(row[4])
        manufacturer.append(row[1])


failure_details_list = [re.sub("[^a-zA-Z.]"," ",x) for x in failure_details_list]
workaround_list = [re.sub("[^a-zA-Z.]"," ",x) for x in workaround_list]

#Finding trigram

stops = set(stopwords.words('english'))
list_of_tokens_failure = [x.split() for x in failure_details_list]
tokens_failure = [[w for w in list_w if not w in stops] for list_w in list_of_tokens_failure]
list_of_tokens_workaround = [x.split() for x in workaround_list]
tokens_workaround = [[w for w in list_w if not w in stops] for list_w in list_of_tokens_workaround]
count_trigram_failure = collections.Counter()
count_trigram_workaround = collections.Counter()

# Processing each line to get list of trigram tuples
for i,trigram_line in enumerate(tokens_failure):
    trigram_failure_tuples = list(nltk.trigrams(trigram_line))
    trigram_workaround_tuples = list(nltk.trigrams(tokens_workaround[i]))
    for trigram in trigram_failure_tuples:
        count_trigram_failure[trigram] += 1
    for trigram_w in trigram_workaround_tuples:
        count_trigram_workaround[trigram_w] += 1

print "Failure - Cortex A" 
print [x[0] for x in count_trigram_failure.most_common()[0:100]]
print
print
print "Workaround - Cortex A"
print [x[0] for x in count_trigram_workaround.most_common()[10:140]]
