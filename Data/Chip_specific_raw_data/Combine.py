# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 21:18:40 2016

@author: jeeheh
"""

import pickle
import csv

def importPickle2(loc,filelist):
    output=[]
    for file in filelist:
        with open(loc+file,'rb') as f:
            u=pickle._Unpickler(f)
            u.encoding='latin1'            
            #outputT=pickle.load(f)
            outputT=u.load()
        output=output+outputT
    return output

def importPickle3(loc,filelist):
    output=[]
    for file1 in filelist:
        #with open(loc+file,'rb') as f:
        with open(file1,'rb') as f:
            outputT=pickle.load(f)
        output=output+outputT
    return output    

def saveCSV(dictlist,filename):
    keys = dictlist[0].keys()
    with open(filename+'.csv', 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys,delimiter='\t')
        dict_writer.writeheader()
        dict_writer.writerows(dictlist)

def rmlinebreak(listdict):
    for i in range(len(listdict)):
        for j in list(listdict[i].keys()):
            listdict[i][j]=listdict[i][j].replace('\n',' ')
            listdict[i][j]=listdict[i][j].replace('\t',' ')
    return listdict

#loc= 'D:\Microarchitecture\Final_project\New_Data\'
loc=''
ARM9_f2=['ST.pickle','NXP_LPC32.pickle', 
    'Arm9_NXP_MC9328_Mask_Errata.pickle',
    'Arm9_NXP_MCIMX_Errata.pickle',
    'MX_28.pickle',
    'Arm9_Arm7_Atmel_Errata.pickle',
    'NXP_LPC2xxx.pickle']

ARM9_f3=['ARM9_TI.pickle']

CortexA9_f2=['NXP.pickle']
CortexA8_f2=['CA8_NXP.pickle','CA8_TI.pickle']
CortexA9_f3=['CortexA-9_TI.pickle']

ARM9=importPickle2(loc,ARM9_f2)+importPickle3(loc,ARM9_f3)[0]
CortexA9=importPickle2(loc,CortexA9_f2)+importPickle3(loc,CortexA9_f3)[0]
CortexA8=importPickle2(loc,CortexA8_f2)
CortexA8=CortexA8[0]+CortexA8[1]

ARM9=rmlinebreak(ARM9)
CortexA9=rmlinebreak(CortexA9)
CortexA8=rmlinebreak(CortexA8)
     
saveCSV(ARM9,'ARM9')
saveCSV(CortexA9,'CortexA9')
saveCSV(CortexA8, 'CortexA8')

