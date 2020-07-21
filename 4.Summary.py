#!/usr/bin/env python
# coding: utf-8

import csv
import pandas as pd
import numpy
import matplotlib.pyplot as plt

df_commiters = pd.read_csv('/gitgender/files/results/core_developers.csv')
num_truckfacktors = len(df_commiters)
print ('Number of TF identified: {}'.format(num_truckfacktors))


df_commiters_fullname = pd.DataFrame(index=None, columns=None)
i = 0
for index,row in df_commiters.iterrows():
    nome = row['user']
    size_name = len(nome.split())
    if (size_name > 1):    
        try:
            df_commiters_fullname = df_commiters_fullname.append(df_commiters.iloc[i],ignore_index=True)
        except:
            print('error adding fullname row: ' + row)
   
    i = i + 1

df_commiters_fullname.drop_duplicates(subset=['login','full_name','user'],inplace=True)

num_truckfacktors_full_name = len(df_commiters_fullname)
print ('Number of TF with full name: {}'.format(num_truckfacktors_full_name))

df_commiters_male = df_commiters_fullname.loc[(df_commiters_fullname['gender1'] != 'female') & (df_commiters_fullname['gender2'] != 'female') ]
num_commiters_male = len(df_commiters_male)
print ('Number of TF male: {}'.format(num_commiters_male))

df_commiters_female = df_commiters_fullname.loc[(df_commiters_fullname['gender1'] == 'female') | (df_commiters_fullname['gender2'] == 'female') ]
num_commiters_female = len(df_commiters_female)
print ('Number of TF female: {}'.format(num_commiters_female))