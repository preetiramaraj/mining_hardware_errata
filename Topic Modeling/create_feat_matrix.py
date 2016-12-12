#Run with Python 2

import csv
import pandas as pd
import numpy as np
import pickle
#import find_common_keyword as fck

def openCSV(csv_filename):
    with open(csv_filename) as f:
        entry_list = [{k: v for k, v in row.items()} 
                       for row in csv.DictReader(f, delimiter='\t', skipinitialspace=True)]
    return entry_list

'''
#Import List of Dictionaries and Keywords
ARM9_keywords=fck.identify_keyword_in_csv('ARM9.csv')
CortexA9_keywords=fck.identify_keyword_in_csv('CortexA9.csv')
ARM9=openCSV('ARM9.csv')
CortexA9=openCSV('CortexA9.csv')


#Create Dataframe for ARM9
ARM9_df=pd.DataFrame(ARM9)
ARM9_df=ARM9_df.ix[:,['Core','Manufacturer','Chip',\
                      'Workaround','Details','Failure','Fix Status']]
for word in ARM9_keywords:
    for cat in ['Workaround','Details','Failure','Fix Status']:
        feat=[x.find(word)!=-1 for x in ARM9_df[cat]]
        feat=1*np.asarray(feat)
        ARM9_df[cat+'-'+word]=feat      
ARM9_df=ARM9_df.drop(['Workaround','Details','Failure','Fix Status'],1)      


#Create Dataframe for CortexA9
CortexA9_df=pd.DataFrame(CortexA9)
CortexA9_df=CortexA9_df.ix[:,['Core','Manufacturer','Chip',\
                      'Workaround','Details','Failure','Fix Status']]
for word in CortexA9_keywords:
    for cat in ['Workaround','Details','Failure','Fix Status']:
        feat=[x.find(word)!=-1 for x in CortexA9_df[cat]]
        feat=1*np.asarray(feat)
        CortexA9_df[cat+'-'+word]=feat      
CortexA9_df=CortexA9_df.drop(['Workaround','Details','Failure','Fix Status'],1) 

with open('Dataframes.pickle','w') as f:
    pickle.dump([CortexA9,CortexA9_df,CortexA9_keywords,\
                 ARM9,ARM9_df,ARM9_keywords],f)

'''
ARM9=openCSV('ARM9.csv')
CortexA9=openCSV('CortexA9.csv')
CortexA8=openCSV('CortexA8.csv')
with open('Output.pickle','w') as f:
    pickle.dump([ARM9,CortexA8,CortexA9],f)