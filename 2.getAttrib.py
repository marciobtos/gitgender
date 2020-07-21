#!/usr/bin/env python
# coding: utf-8


import csv
import re
import urllib.request
import re
import csv
from geopy.geocoders import Nominatim
import time
from github import Github
import pandas as pd
import numpy
import requests
import json
#from selenium import webdriver
import os

geolocator = Nominatim(user_agent="gendergit")
#geolocator = Nominatim(user_agent="gendergit")
user_github = os.environ['usergit']
password_github = os.environ['pwdgit']
g = Github(user_github, password_github)

#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--headless')
#chrome_options.add_argument("--disable-setuid-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
#driver = webdriver.Chrome('/tmp/chromedriver', chrome_options=chrome_options)

time.sleep(1)

#def get_num_contributors(full_name_repo):
#    driver.get('https://github.com/' + full_name_repo)
#    time.sleep(1)
#    p_element = driver.find_elements_by_class_name('num')
#    num_elements =  p_element[4].text
#    return num_elements

def get_country(location_):
    if (', CA' in location_):
        country = 'USA'
    else:
        geolocator = Nominatim(user_agent="gitgender")
        try:
            location = geolocator.geocode(location_,language='en')
            country = location.address.split(sep=', ')[-1]
        except:
            country = ''
        
    return country

def remove_characters(text):
    text = text.replace(')','')
    text = text.replace('(','')
    return text

df_commiters = pd.read_csv('commiters_with_TF3.csv',header=None)
#df_commiters.columns = ['language', 'id', 'full_name','name','size','watchers','forks','created_at','git_url','lines','user','user_num_commits','rate_commits']
#df_commiters.columns = ['language', 'id', 'full_name','name','size','watchers','forks','created_at','git_url','lines','user','login']


for index, row in df_commiters.iterrows():
    full_name_repo = row[2]
    id_repo = row[1]
    full_name = row[2]
    print('username :' + str(row[11]))

    try: 
        user_name = remove_characters(row[11])
        user_list = g.get_user(user_name)
        login = user_list.login   
    except:
        login = 'null'
    try:     
        location = user_list.location   
    except:
        location = 'null'

    try:
        email = user_list.email
    except:
        email = 'null'
    if (location):
        #try:
        country = get_country(location)
        #except:
         #   country = 'null'
        
    else:
        print('location is none')
        country = ''
    time.sleep(5)
   
    
    df_commiters.loc[index, '12'] = location
    df_commiters.loc[index, '13'] = country
    df_commiters.loc[index, '14'] = email


df_commiters.to_csv('commiters_with_repo_data.csv',index_label=None,index=False,header=False)

#driver.close()



