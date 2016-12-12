import nltk 
import collections
import re
import csv
from nltk.corpus import stopwords
import nltk
#0Chip','1Details','2Core','3Errata ID','4Module','5Criticality','6Workaround','Revisions Impacted','8Failure','9Fix Status','Masks Affected','11Manufacturer']

failure_details_arm9_list = []
workaround_arm9_list = []
manufacturer = [] # keeping track of manufacturer for each column from above

with open('ARM9.csv') as f:
    reader = csv.reader(f, delimiter='\t')
    reader.next()
    
    for row in reader:
        failure_details_arm9_list.append(' '.join((row[8],row[1])))
        workaround_arm9_list.append(row[6])
        manufacturer.append(row[11])


failure_details_arm9_list = [re.sub("[^a-zA-Z.]"," ",x) for x in failure_details_arm9_list]
workaround_arm9_list = [re.sub("[^a-zA-Z.]"," ",x) for x in workaround_arm9_list]

#Finding trigram

stops = set(stopwords.words('english'))
list_of_tokens_failure = [x.split() for x in failure_details_arm9_list]
tokens_failure = [[w for w in list_w if not w in stops] for list_w in list_of_tokens_failure]
list_of_tokens_workaround = [x.split() for x in workaround_arm9_list]
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

print "Failure - ARM 9" 
print [x[0] for x in count_trigram_failure.most_common()[0:70]]
print
print
print "WOrkaround - ARM 9"
print [x[0] for x in count_trigram_workaround.most_common()[90:140]]
