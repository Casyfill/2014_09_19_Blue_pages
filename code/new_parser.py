#!/usr/bin/env python
#-*- coding: utf-8 -*-
import csv, sys

modulePath = "/Users/casy/Dropbox/My_Projects/2014_09_19_Blue_pages/git/2014_09_19_Blue_pages/code/misc/"	
sys.path.append(modulePath)
from misc import getFiles, textChunker
from person import person

txtPath = "/Users/casy/Dropbox/My_Projects/2014_09_19_Blue_pages/git/2014_09_19_Blue_pages/raw_txt/finals/overal.txt"
rPath = "/Users/casy/Dropbox/My_Projects/2014_09_19_Blue_pages/git/2014_09_19_Blue_pages/result/result.csv"

def getCPC(line):
	if '-' in line and len(line.split('-'))==3:
		city, pop, county = [x.strip() for x in line.split('-')]
		city, county = city.title(), county.title()
		
	else:
		print 'CPC warning: %s' % line
		city, pop, county = 'n/a','n/a','n/a'
	return city,pop,county


def poBox(chunk):
	for line in chunk:
		pLine = line.upper()
		if 'PO BOX' in pLine or 'POBOX'  in pLine:
			return pLine[pLine.index('BOX')+3:pLine.index('-')].strip(),pLine[pLine.index('-')+1:].strip()
			break

	return 'n/a','n/a'
			
def phone_fax(chunk):
	fax, phone = 'n/a','n/a'
	chunk = [x.upper() for x in chunk]
	
	for line in chunk:	
		if 'FAX' in line and 'TELEPHONE' in line:
			phone = line[line.index(':')+1:line.index('FAX')].strip()
			fax = line[line.rindex(':')+1:].strip()
			break
	
	if fax == 'n/a' and phone=='n/a':
		for line in chunk:
			if 'TELEPHONE' in line and ':' in line:
				phone = line[line.index(':')+1:].strip()

		for line in chunk:
			if 'FAX' in line and ':' in line: 
				fax = line[line.index(':')+1:].strip()
					
	return phone, fax

def hours(chunk):
	weekdays = ['sunday',
				'monday',
				'tuesday',
				'wednesday',
				'thursday',
				'friday',
				'saturday']

	wd = 'n/a'
	for line in chunk:
		lLine = line.lower()
	
		if any([x in lLine for x in weekdays]):
			wd = line
			
	return wd

def getAddress(chunk):
	if any(['box' in line.lower() and 'po' in line.lower() for line in chunk]):
		s = 2
	else:
		s = 1

	e = 100
	
	for i, line in enumerate(chunk):
		if 'phone' in line.lower():
			e = i
			break
	if s>=e:
		return 'n/a'
	else: return chunk[s].title()

def ZipFromAdress(Zip, address):
	address = address.replace('•','-').replace('·','-') 
	if Zip == 'n/a' and '-' in address:
		return address[address.index('-')+1:].strip(),address[:address.index('-')].strip()
	else: return Zip, address


def getPeople(chunk):
	rChunk = chunk[::-1]

	persons = []
	for line in rChunk:
		if '-' in line:
			

			position, person = line[:line.rindex('-')], line[line.rindex('-')+1:]
			names = [x.strip() for x in person.split()]
			persons.append({'position':position, 'last':names[-1], 'first':' '.join(names[:-1])})
		else:
			break

	return persons[::-1]




with open(txtPath,'rb') as readFile:
	chunks = textChunker(readFile)

rowArray = []

for chunk in chunks:

	chunk = [x.encode('utf-8') for x in chunk]
	chunk[0] = chunk[0].replace('•','-').replace('·','-')

	# city name, pop, county
	city, pop, county = getCPC(chunk[0])
	pb, Zip = poBox(chunk)
	phone, fax = phone_fax(chunk)
	wh = hours(chunk)
	address = getAddress(chunk)
	persons = getPeople(chunk)

	Zip, address = ZipFromAdress(Zip, address)

	for person in persons:
		row = {'First name':person['first'],'Last name':person['last'],'Title':person['position'],'Organization':'--','Address':address,'PO Box':pb,'City':city,'County': county, 'State':'OK','Zip':Zip,'Email':'n/a','Phone': phone, 'Fax':fax, 'office days':wh,'pop':pop}
		rowArray.append(row)


	# print '%s : %d' % (city, len(persons))
headersList = ['First name','Last name','Title','Organization','Address','PO Box','City','County','State','Zip','Email','Phone','Fax','office days', 'pop']

with open(rPath,'wb') as writeFile:
	wD = csv.DictWriter(writeFile, headersList,restval='', extrasaction='raise', dialect='excel')
	wD.writeheader()
	for row in rowArray:
		wD.writerow(row)
	print 'done!'