import csv
import operator
import numpy as np
from nltk.corpus import stopwords
import re
import pickle


stops = set(stopwords.words("english"))
list_of_invalid_keyword = ['Not','been','that', 'it', 'when', 'as', 'When', 'for', 'are', 'The', 'an', 'a', 'from','not', 'or', 'on', 'This', 'by', 'be', 'STR91xFA', 'and', 'in', 'In', 'of', 'at','is','Is','before', 'Before', 'where','there', 'There', 'during','For','for','which','up','should','but','into', 'can', 'must', 'to', '', 'the', 'under', 'below', 'will', 'It', 'Becasue', 'because', 'so', 'if', 'If', 'than', 'no', 'much','any','many','either','both', 'more', 'does', 'do', 'may','next','A','a','Figure','only','such','after','also','=', '.', ',', '5.','4.','3.', '2.', '1.', 'while', 'each', 'being', '1','2','3','4','5','6','7','8','9','0', 'still', '-', 'ARM', 'case', 'Use', 'No', 'this', 'its', 'To', 'never', 'due', 'down', 'with', 'above', 'was', 'until', 'An', 'As' 'without', 'one', 'two', 'have', 'has', 'then', 'their', 'all', 'less', 'other', 'After', 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','copyright','2010','2011','2012','2013','2014','2015','2009','2008','2007','www', 'january','feburary', 'march','april','may', 'june', 'july', 'august', 'september', 'october', 'november', 'december','workaround','using']

def concat_strings(entry):
	string = ''
	for k in entry:
		if k not in ['Core','Manufacturer']:
			string = string + ' ' + entry[k] 

	return string

def find_most_frequent_keyword(string):
	keywords = split_sentence(string)

	bin_count = dict()

	for element in keywords:
		element = element.strip()

		if element not in list_of_invalid_keyword and element not in stops:
			if element not in bin_count:
				bin_count[element] = 0

			bin_count[element] = bin_count[element] + 1

	sorted_bin_count = sorted(bin_count.items(), key=operator.itemgetter(1))

	list_of_frequent_keyword = list()
	for element in sorted_bin_count:
		count = element[1]
		if count > 10:
			list_of_frequent_keyword.append(element[0])

	return list_of_frequent_keyword


def identify_keyword_in_csv(csv_filename):
	entry_list = read_csv(csv_filename)

	# group by manufactures
	content_group_by_manufactures = dict()
	for entry in entry_list:
		manufacture = entry['Manufacturer']
		string = concat_strings(entry) 

		if manufacture not in content_group_by_manufactures:
			content_group_by_manufactures[manufacture] = ''

		content_group_by_manufactures[manufacture] = content_group_by_manufactures[manufacture] + '' + string

	# find most frequent keyword of each manufacturers
	frequent_keyword_group_by_manufacture = dict()
	for manufacture in content_group_by_manufactures:
		frequent_keyword_group_by_manufacture[manufacture] = find_most_frequent_keyword(content_group_by_manufactures[manufacture])

	# find common keyword among the manufacturers.
	accept_keyword_list = list()
	for man1 in frequent_keyword_group_by_manufacture:
		for man2 in frequent_keyword_group_by_manufacture:
			if man1 != man2:
				for keyword in frequent_keyword_group_by_manufacture[man1]:
					if keyword in frequent_keyword_group_by_manufacture[man2]:
						accept_keyword_list.append(keyword)
	#print "===========================", csv_filename
	# print set(accept_keyword_list)
	return set(accept_keyword_list)


def read_csv(csv_filename):
	with open(csv_filename) as f:
		entry_list = [{k: v for k, v in row.items()} 
			for row in csv.DictReader(f, delimiter='\t', skipinitialspace=True)]

	return entry_list

def split_sentence(string):
	#remove punctuations and numbers
	string = re.sub("[^a-zA-Z0-9]"," ",string)
	#split sentences into words
	keywords = string.lower().split()

	return keywords

def failure_workaround_co_occurrence_mat(common_keyword):
	# construct ids
	map_keyword_id = dict()
	map_id_keyword = dict()
	keyword_idx = 0
	for keyword in common_keyword:
		map_keyword_id[keyword] = keyword_idx
		map_id_keyword[keyword_idx] = keyword
		keyword_idx = keyword_idx + 1

	# concatenate the two csv files
	entry_list1 = read_csv('ARM9.csv')
	entry_list2 = read_csv('CortexA9.csv')
	entry_list = entry_list1 + entry_list2
	co_occurrence_mat = np.zeros((len(common_keyword), len(common_keyword)), dtype=np.int)

	# Identify the failure - workaround correspondence
	for errata_entry in entry_list:
		failure = errata_entry['Failure'] + ' ' + errata_entry['Details']
		workaround = errata_entry['Workaround']
		
		failure_keyword = split_sentence(failure)
		workdaround_keyword = split_sentence(workaround)

		# only identify each keyword once
		failure_keyword = list(set(failure_keyword))
		workaround_keyword = list(set(workdaround_keyword))

		# Note that the co-occurence matrix is not symmetric! 
		# the row index correspond to the failure keyword
		# the col index correspond to the workdaround keyword
		# for keyword1 in failure_keyword:
		# 	for keyword2 in workaround_keyword:
		# 		if keyword1 in common_keyword and keyword2 in common_keyword:

		for keyword1 in common_keyword:
		  	for keyword2 in common_keyword:
		  		if failure.find(keyword1) >=0 and workaround.find(keyword2) >= 0:
					# the first index points to failure
					# the second index points to workaround
					idx1 = map_keyword_id[keyword1]
					idx2 = map_keyword_id[keyword2]

					co_occurrence_mat[idx1, idx2] = co_occurrence_mat[idx1, idx2] + 1


	# identify the most frequent keywords as in the failure-workaround correspondence
	print "\n\n\n=============================================================="
	print "\t\t\tKeyword pairs"
	for i in range(0, len(common_keyword)):
		for j in range(0, len(common_keyword)):
			if co_occurrence_mat[i, j] > 20:
				print map_id_keyword[i], map_id_keyword[j], co_occurrence_mat[i, j]
	
	with open('failure_workaround_co_occurrence_mat.pickle', 'wb') as handle:
		pickle.dump([co_occurrence_mat, common_keyword], handle)


def find_bigram():
	# concatenate the two csv files
	entry_list1 = read_csv('ARM9.csv')
	entry_list2 = read_csv('CortexA9.csv')
	entry_list = entry_list1 + entry_list2
	
	# bigram pairs
	bigrams_map_count = dict()
	# Identify the bigram correspondence
	for errata_entry in entry_list:
		string = concat_strings(errata_entry)	
		keywords = split_sentence(string)

		# Note that the co-occurence matrix is symmetric! 
		for idx in range(0, len(keywords) - 1):
			keyword1 = keywords[idx]
			keyword2 = keywords[idx + 1]

			if keyword1 not in stops and keyword2 not in stops:
				if keyword1 not in list_of_invalid_keyword and keyword2 not in list_of_invalid_keyword:
					# use the 'keyword1 keyword2' as identifier
					key = keyword1 + ' ' + keyword2
					if key not in bigrams_map_count:
						bigrams_map_count[key] = 0
					else:
						bigrams_map_count[key] = bigrams_map_count[key] + 1

	# sort them, increasing order, the largest one is the last one 
	sorted_bigram = sorted(bigrams_map_count.items(), key=operator.itemgetter(1))

	output = list()
	print "\n\n\n=============================================================="
	print "\t\t\tBigrams"
	for i in range(0,100):
		print sorted_bigram[len(sorted_bigram)-i-1][0]
		output.append(sorted_bigram[len(sorted_bigram)-i-1][0])
	
	with open('sorted_bigram.pickle', 'wb') as handle:
		pickle.dump(sorted_bigram, handle)

	return output

############################################################################### Main routine


# first identiy common keywords in the files
keyword_set1 = identify_keyword_in_csv('ARM9.csv')
keyword_set2 = identify_keyword_in_csv('CortexA9.csv')
common_keyword = keyword_set1.union(keyword_set2)
common_keyword = list(common_keyword)
print "Number of keywords identified: ", len(common_keyword)
print common_keyword


# then build the co-occurence matrixes based on these common keywords
bigrams = find_bigram()
common_keyword = common_keyword + bigrams
failure_workaround_co_occurrence_mat(common_keyword)



