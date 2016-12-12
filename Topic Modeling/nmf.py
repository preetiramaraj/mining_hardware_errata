#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 09:51:46 2016

@author: jeeheh
"""

import pickle
import numpy as np
import sklearn.feature_extraction.text as text
from sklearn import decomposition
from sklearn import linear_model
import csv

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

##################################################################################################

def ccmat(num_topics,side1,side2):
    ccmat=np.zeros((num_topics,num_topics))
    ccmat_rand=np.zeros((num_topics,num_topics))
    side3=side2[np.random.choice(len(side1),len(side1))]
    for i in range(len(side1)):
        for j in range(num_topics):
            if side1[i,j]>.2:
                for k in range(num_topics):
                    if side2[i,k]>.2:
                        ccmat[j,k]=ccmat[j,k]+1
                    if side3[i,k]>.2:
                        ccmat_rand[j,k]=ccmat_rand[j,k]+1
    ccmat=ccmat-ccmat_rand
    indx=np.argsort(ccmat.ravel()) #indx of largest values are at the end
    return np.unravel_index(indx[-3:],(num_topics,num_topics))
    
##################################################################################################
#Import Data
with open('Output.pickle','rb') as f:
    ARM9,CortexA8,CortexA9=pickle.load(f)

output=ARM9+CortexA8+CortexA9

#Count of Data
for core in np.unique([x['Core'] for x in output]):
    output2=[x for x in output if x['Core']==core]
    print(core+" "+str(len(output2)))
    for manu in np.unique([x['Manufacturer'] for x in output2]):
        output3=[x for x in output2 if x['Manufacturer']==manu]
        print(manu+" "+str(len(output3)))

#Remove Certain Words
for i in range(len(output)):
    for j in ['Workaround','Failure','Details']:
        output[i][j]=output[i][j].replace(' TI ',' ')
        output[i][j]=output[i][j].replace(' OMAP',' ')

#Create a list - combine failure and details. workarounds separate.
combined=[x['Workaround'] for x in output] 
combined=combined+[x['Failure']+' '+x['Details'] for x in output] 
labelref=ARM9+CortexA9+CortexA8+ARM9+CortexA9+CortexA8  

#Vectorize    
vectorizer = text.CountVectorizer(stop_words='english', min_df=20)
dtm = vectorizer.fit_transform(combined).toarray()
vocab = np.array(vectorizer.get_feature_names())
dtm.shape
len(vocab)

#Topic Modeling Grid Search
num_top_words = 20
#num_topic_grid=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
num_topic_grid=[9]
topic_words=[]
results=np.empty((len(num_topic_grid),9))
results[:]=np.nan
proportions=np.empty(9)
proportions[:]=np.nan

for indx, num_topics in enumerate(num_topic_grid): 
    print(num_topics)
    clf = decomposition.NMF(n_components=num_topics, random_state=1)
    doctopic = clf.fit_transform(dtm) 
    
    #Words associated with topics
    topic_words_temp = []    
    for topic in clf.components_:
        word_idx = np.argsort(topic)[::-1][0:num_top_words]
        topic_words_temp.append([vocab[i] for i in word_idx])
    topic_words.append(topic_words_temp)
    

    with open('topic'+str(num_topics)+'.csv', "w") as f:
        writer = csv.writer(f)
        writer.writerows(topic_words_temp)    

        
    #Normalize to Sum to 1
    doctopic = doctopic / np.sum(doctopic, axis=1, keepdims=True)
    doctopic=np.nan_to_num(doctopic)

    testnum=0    
    
    #Run Regression: Predict Workaround or Failure/Details
    label=np.hstack((np.zeros(len(ARM9+CortexA9+CortexA8)),np.ones(len(ARM9+CortexA9+CortexA8)))) 
    #label indicates Failures/Details (vs Workarounds)
    clsf=linear_model.LogisticRegression()
    clsf.fit(doctopic,label)
    pred=clsf.predict(doctopic)
    print('Pred Failure (vs Workaround): '+str((np.mean(pred==label))))
    coef=np.hstack((clsf.coef_[0,:],clsf.intercept_))
    top=np.argsort(-abs(coef))
    print(top[:3])
    print(coef[top[:3]])
    results[indx,testnum]=np.mean(pred==label)
    proportions[testnum]=np.mean(label)
    print(np.maximum(proportions[testnum],1-proportions[testnum])-np.mean(pred==label))
    
    #Run Regressions: Predict Core
    for core in np.unique([x['Core'] for x in labelref]):
        label=[x['Core']==core for x in labelref]*1
        clsf=linear_model.LogisticRegression()
        clsf.fit(doctopic,label)
        pred=clsf.predict(doctopic)
        print('Pred '+core+': '+str((np.mean(pred==label))))
        coef=np.hstack((clsf.coef_[0,:],clsf.intercept_))
        top=np.argsort(-abs(coef))
        print(top[:3])
        print(coef[top[:3]])
        testnum=testnum+1
        results[indx,testnum]=np.mean(pred==label)
        proportions[testnum]=np.mean(label)
        print(np.maximum(proportions[testnum],1-proportions[testnum])-np.mean(pred==label))
    
    #Run Regressions: Predict Manufacturer
    for manu in np.unique([x['Manufacturer'] for x in labelref]):
        label=1*[x['Manufacturer']==manu for x in labelref]
        clsf=linear_model.LogisticRegression()
        clsf.fit(doctopic,label)
        pred=clsf.predict(doctopic)
        print('Pred '+str(manu)+': '+str((np.mean(pred==label))))
        coef=np.hstack((clsf.coef_[0,:],clsf.intercept_))
        top=np.argsort(-abs(coef))
        print(top[:3])
        print(coef[top[:3]])
        testnum=testnum+1
        results[indx,testnum]=np.mean(pred==label)
        proportions[testnum]=np.mean(label)
        print(np.maximum(proportions[testnum],1-proportions[testnum])-np.mean(pred==label))
    '''
    for manu in np.unique(CortexA9_df['Manufacturer']):
        label=1*(CortexA9_df['Manufacturer']==manu)
        clsf=linear_model.LogisticRegression()
        clsf.fit(doctopic[-len(CortexA9):,:],label)
        pred=clsf.predict(doctopic[-len(CortexA9):,:])
        print('Pred C-A9'+str(manu)+': '+str((np.mean(pred==label))))
        coef=np.hstack((clsf.coef_[0,:],clsf.intercept_))
        top=np.argsort(-abs(coef))
        print(top[:3])
        print(coef[top[:3]])
        testnum=testnum+1
        results[indx,testnum]=np.mean(pred==label)
        proportions[testnum]=np.mean(label)
        print(np.maximum(proportions[testnum],1-proportions[testnum])-np.mean(pred==label))
    '''
    
#Best Method
proportions=np.maximum(proportions,1-proportions)
test=results-proportions
test=np.sum(results-proportions, axis=1)
print('Best Number of Topics: '+str(num_topic_grid[np.argmax(test)]))


#Co-Occurence Matrix: All
cctop3=[]
cctop3.append(['All',ccmat(num_topics,doctopic[len(doctopic)/2:,:],doctopic[:len(doctopic)/2,:])])
for core in np.unique([x['Core'] for x in labelref]):
    indx=[index for index,value in enumerate(labelref) if value['Core']==core]
    doctopicTEMP=doctopic[indx,:]
    cctop3.append([core,ccmat(num_topics,doctopicTEMP[len(doctopicTEMP)/2:,:],doctopicTEMP[:len(doctopicTEMP)/2,:])])


#References
#   https://de.dariah.eu/tatom/topic_model_python.html