#!/usr/bin/env python
# coding: utf-8



# import json
import time	
import requests
import os

def get_popular_projects(language):
	prefix = 'https://api.github.com/search/repositories?q='
	suffix = '&sort=stargazers_count&order=desc&page='
	for lang in language:
		time.sleep(5)
		stars = '1'
		
		projects = int(os.environ['num_projects'])
		
		outFile = '/gitgender/files/projects/{}.csv'.format(lang)
		
		lang  = '+language:' + lang 
		
		stars = 'stars:%3E'  + stars
		perpage = '&per_page=100'
		uri   = prefix + stars + lang + perpage + suffix
		
		
		print ('searching the github API')
		print ('query string:', uri)
		
		response = requests.get(uri + '1')
		data = response.json()
		
		items = data['items']
		
		pagination = 0
		
		f = open(outFile, 'wb')
		
		for item in items:
			time.sleep(1)		
			pagination += 1 
		
		pages =  (projects // pagination)
		
		for i in range(1, pages):
			time.sleep(1)
			print (uri + str(i + 1))
			response = requests.get(uri + str(i + 1))
			data = response.json()
			if 'items' in data.keys():
				items = items + data['items']
			else: 
				print (data)
				break 
		
		count = 0   
		for item in items: 
			if(count < projects and item != None):
				line   = item.get("language", "-") + ","
				line  += str(item.get("id", "-")) + ","
				line  += item.get("full_name", "-") + ","
				line  += item.get("name", "-") + ","
				line  += str(item.get("size", "-")) + "," 
				line  += str(item.get("watchers", "-")) + "," 
				line  += str(item.get("forks", "-")) + "," 
				line  += str(item.get("created_at", "-")) + "," 
				line  += item.get("git_url", "-")  
				count += 1
				line += '\n'			
				f.write(line.encode('utf8'))
			elif(count >= projects):  
				break
		
		f.close()






