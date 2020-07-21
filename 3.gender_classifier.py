#!/usr/bin/env python
# coding: utf-8

import csv
import pandas as pd
from genderComputer.genderComputer import *
import requests
import json
import os
from iso3166 import countries

keyapi = os.environ['keyapi']

df_commiters = pd.read_csv('commiters_with_repo_data.csv',header=None)

#df_commiters.columns = ['language', 'id', 'full_name','repository','size','watchers','forks','created_at','git_url','lines','user','user_num_commits','rate_commits','login', 'location', 'country', 'email']
df_commiters.columns = ['language', 'id', 'full_name','repository','size','watchers','forks','created_at','git_url','lines','user','login', 'location', 'country', 'email']

gc = GenderComputer(os.path.abspath('./genderComputer/nameLists'))

#def get_gender_namsor(name):
#    name = name.split()
#    url = 'https://v2.namsor.com/NamSorAPIv2/api2/json/gender/' + name[0] + '/' + name[-1]
#    headers = {'content-type': 'application/json', 'X-API-KEY': keyapi}
#    r = requests.get(url, headers=headers)
#    try:
#	
#    	dados_namsor = json.loads(r.content)
#    except:
#        gender = 'unisex'
#        return gender
#    try:
#        gender = dados_namsor['likelyGender'].encode("utf-8")
#    except:
#        gender = 'unisex'
#    print(url)
#    return gender
def get_gender_namsor(name,country_iso):
    name = name.split()
    #/api2/json/genderGeo/{firstName}/{lastName}/{countryIso2}
    if (country_iso):
        url = 'https://v2.namsor.com/NamSorAPIv2/api2/json/genderGeo/' + name[0] + '/' + name[-1] + '/' + country_iso
    else:
        url = 'https://v2.namsor.com/NamSorAPIv2/api2/json/gender/' + name[0] + '/' + name[-1]
    headers = {'content-type': 'application/json', 'X-API-KEY': keyapi}
    r = requests.get(url, headers=headers)
    try:
	
    	dados_namsor = json.loads(r.content)
    except:
        gender = 'unisex'
        return gender
    try:
        gender = dados_namsor['likelyGender'].encode("utf-8")
    except:
        gender = 'unisex'
    print(url)
    return gender
	
def getCountryISO(country):
    try:
        c = countries.get(country)
        c = c.alpha2
    except:
        c = ''
    return c


for index, row in df_commiters.iterrows():
    error_ = 0
    try:
        nome = unicode(row[10])
    except:
        
        nome = row[10]
        #break
        error_ = 1
    country_ = row[13]
    if not (str(country_).isupper()):
        country_ = unicode(country_).capitalize()
    else:
        country_ = unicode(country_)
    
    gender2 = get_gender_namsor(nome,getCountryISO(country_))
    if (error_ == 0):
        gender = gc.resolveGender(nome, country_)
    else:
        gender = 'unisex'
    print('{} - {} - {} - {}'.format(nome,country_,gender,gender2))
    df_commiters.loc[index, 'gender'] = gender
    df_commiters.loc[index, 'gender2'] = gender2


#df_commiters.columns = ['language', 'id', 'full_name','repository','size','watchers','forks','created_at','git_url','lines','user','user_num_commits','rate_commits','login', 'location', 'country', 'email','gender1', 'gender2']
df_commiters.columns = ['language', 'id', 'full_name','repository','size','watchers','forks','created_at','git_url','lines','user','login', 'location', 'country', 'email','gender1', 'gender2']
if not os.path.exists('/gitgender/files/results'):
    os.makedirs('/gitgender/files/results')

df_commiters.drop_duplicates(subset=['login','full_name','user'],inplace=True)
df_commiters.to_csv('/gitgender/files/results/core_developers.csv',index_label=None,index=False,header=True)




