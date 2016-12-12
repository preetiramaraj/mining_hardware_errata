import csv
import operator
from collections import Counter
import os
import random



def open_csv_file(csv_filename):
	with open(csv_filename) as f:
		entry_list = [{k: v for k, v in row.items()} 
			for row in csv.DictReader(f, delimiter='\t', skipinitialspace=True)]
	return entry_list


def gen_RNN_training_data(entry_list, reference_lines):
	random.shuffle(entry_list)
	train_entry_list = entry_list[:len(entry_list)-10]
	test_entry_list = entry_list[len(entry_list)-10:]

	try:
		os.mkdir('problem_vs_workdaround')
	except:
		print "path already exists"

	with open("./problem_vs_workdaround/input.txt",'w+') as f:	# problem description v.s. workaround
		for entry in train_entry_list:
			Workaround = entry['Workaround']
			Problem_Description = entry['Details']
			f.write("Problem Description: " + Problem_Description.replace('Description of limitation', ''))	
			f.write(" Workaround: " + Workaround + '\n')
			f.write("\n")	
	with open("./problem_vs_workdaround/testset.txt",'w+') as f:	# problem description v.s. workaround
		for entry in test_entry_list:
			Workaround = entry['Workaround']
			Problem_Description = entry['Details']
			f.write("Problem Description: " + Problem_Description.replace('Description of limitation', ''))	
			f.write(" Workaround: " + Workaround + '\n')
			f.write("\n")


#####################################################################
	try:
		os.mkdir('problem_description_with_refernence')
	except:
		print "path already exists"

	# train set and test set

	with open("./problem_description_with_refernence/input.txt",'w+') as f:	# only problem description
		for entry in train_entry_list:
			Problem_Description = entry['Details']
			Problem_Description = Problem_Description.replace('Details:', '')
			Problem_Description = Problem_Description.replace('Details/Impact:', '')
			Problem_Description = Problem_Description.replace('Impact:', '')
			Problem_Description = Problem_Description.replace('Description:', '')
			Problem_Description = Problem_Description.replace('Description of limitation', '')
			Problem_Description = Problem_Description.strip()
			f.write(Problem_Description + '\n')
		for line in reference_lines:
			f.write(line)
	with open("./problem_description_with_refernence/testset.txt",'w+') as f:	# only problem description
		for entry in test_entry_list:
			Problem_Description = entry['Details']
			Problem_Description = Problem_Description.replace('Details:', '')
			Problem_Description = Problem_Description.replace('Details/Impact:', '')
			Problem_Description = Problem_Description.replace('Impact:', '')
			Problem_Description = Problem_Description.replace('Description:', '')
			Problem_Description = Problem_Description.replace('Description of limitation', '')
			Problem_Description = Problem_Description.strip()
			f.write(Problem_Description + '\n')	

def add_reference_files():
	list_of_refernce_files = ['OMAP-L137 C6000 DSP_ARM Process - Texas Instruments, Incorporated.txt','OMAP-L132 C6000 DSP_ARM Process - Texas Instruments, Incorporated.txt', 'OMAP4470.txt', 'i.MX 6Dual_6Quad Applications P - Freescale Semiconductor Inc_.txt', 'i.MX27 and i.MX27L Data Sheet - Freescale Semiconductor, Inc_.txt']

	lines = list()
	for _file in list_of_refernce_files:
		with open(_file) as f:
			for line in f:
				if len(line) > 15:
					counter = Counter(line)
					if counter['.'] < 5:
						lines.append(line)

	print len(lines)
	return lines

reference_lines = add_reference_files()

list1 = open_csv_file('ARM9.csv')
list2 = open_csv_file('CortexA9.csv')

combined_list = list1 + list2
gen_RNN_training_data(combined_list, reference_lines)
