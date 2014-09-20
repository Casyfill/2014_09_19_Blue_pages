#!/usr/bin/env python
#-*- coding: utf-8 -*-

def getFiles(mypath):
	from os import listdir
	from os.path import isfile, join
	if mypath[-1]!='/': mypath+='/'
	return [ (mypath +f) for f in listdir(mypath) if (isfile(join(mypath,f)) and f[-3:]=='txt') ]

def textChunker(text):
	mode = False
	texts = []
	
	for line in text:
		line=line.decode('utf-8').replace(' .','.').strip()
		# print line
		if len(line)!=0:
			if mode==False:
				chunk=[]
				chunk.append(line)
				mode=True
			else:
				# print '!!'
				chunk.append(line)
		else:
			# print 'new person'
			if mode==True:
				texts.append(chunk)
				mode = False
			else:
				pass
	return texts
