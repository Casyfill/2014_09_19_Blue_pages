#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, csv		

modulePath = "/Users/casy/Dropbox/My_Projects/2014_09_19_Blue_pages/git/2014_09_19_Blue_pages/code/misc/"	
sys.path.append(modulePath)
from misc import getFiles, textChunker
from person import person

source ="/Users/casy/Dropbox/My_Projects/2014_09_19_Blue_pages/git/2014_09_19_Blue_pages/raw_txt/"
result ="/Users/casy/Dropbox/My_Projects/2014_09_19_Blue_pages/git/2014_09_19_Blue_pages/raw_csv/raw.csv" 

headersList = [
	'category',
	'position',
	'title',
	'first' ,
	'last' ,
	'organization' ,
	'address' ,
	'poBox' ,
	'city' ,
	'state' ,
	'Zip' ,
	'email' ,
	'web',
	'rawText']

with open(result,'wb') as writeFile:
	wD = csv.DictWriter(writeFile, headersList,restval='', extrasaction='raise', dialect='excel')
	wD.writeheader()

	personList =[]

	for f in getFiles(source):
		chapter = f.split('/')[-1].replace('.txt','').replace('_',' ')
		print chapter.upper()
		print
	
		with open(f, 'rb') as text:
			chunks = textChunker(text)
			for chunk in chunks:
				p = person(chunk)
				p.category = chapter
				p.analyse()
				personList.append(p)
				p.plotRaw()
	
	for person in personList:
		wD.writerow(person.asDict())

print 'done!'





