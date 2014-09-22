#!/usr/bin/env python
#-*- coding: utf-8 -*-
import re

class person:
	category = 'n/a'
	position = 'n/a'
	title = 'n/a'
	first  = 'n/a'
	last  = 'n/a'
	organization  = 'n/a'
	address  = 'n/a'
	poBox  = 'n/a'
	city  = 'n/a'
	state  = 'n/a'
	Zip  = 'n/a'
	email  = 'n/a'
	web = 'n/a'
	fax = 'n/a'
	phone = 'n/a'
	rawText = []
	
	def __init__(self, raw):
		self.rawText = raw
		

	def guessEmail(self):
		result = []
		for line in self.rawText:
			if '@' in line:
				line.replace(' .','').replace(' .','').strip()
				ar = line.split()
		
				for mail in ar:
					if '@' in mail:
						result.append(mail)
		if len(result)!=0:
			self.email=', '.join(result)

	def guessWeb(self):
		result = []
		words = []
		for line in self.rawText:
			line.replace(' .','').strip()
			words+=line.split(' ')
		
		for word in words:
			d = ['.ru', '.com', '.org', '.io', '.com', '.edu', '.net', '.gov','.us','.ok']
			if any([True for x in d if x in word]) and '@' not in word:	
				result.append(word)
					
		if len(result)!=0:
			self.web=', '.join(result)

	def guessPosition(self):
		self.position = self.rawText[0]

	def guessName(self):
		names = self.rawText[1].split(' ')
		self.last = names[-1]
		self.first = ' '.join(names[:-1])

	def guessTitle(self):
		if len(self.rawText)>2:
			self.title = self.rawText[2]

	def guessPhones(self):
		
		words = [word for line in self.rawText for word in line.replace(' .','').replace('fax','FAX').strip().split()]

		phonePattern = re.compile(r'^(\d{3})-(\d{3})-(\d{4})')
		
		if 'FAX' in words:
			i = words.index('FAX')-1
			if phonePattern.match(words[i]):
				self.fax= words[i]
				words.pop(i)


		result = [x for x in words if phonePattern.match(x)]

		if len(result)!=0:
			self.phone=', '.join(result)

	def guessPOBox(self):
		words = [word for line in self.rawText for word in line.replace(' .','').strip().split()]
		
		# boxList = ['PO', 'Box', 'box', 'Drawer']
		# if any(True for x in boxList if x in words ):
		
		if 'PO' in words:
			# print 'PO detected'
			POpattern = re.compile(r'\d+')
			i = words.index('PO') +2
			
			if POpattern.match(words[i]):
				self.poBox= words[i]
			else: print self.first, ' ', self.last, ': PO_box conflict!'
	

	def guessAdress(self):
		words = [word for line in self.rawText for word in line.replace(' .','').strip().split()]
		
		States = {
		  "AL": "Alabama",
		  "AK": "Alaska",
		  "AZ": "Arizona",
		  "AR": "Arkansas",
		  "CA": "California",
		  "CO": "Colorado",
		  "CT": "Connecticut",
		  "DE": "Delaware",
		  "FL": "Florida",
		  "GA": "Georgia",
		  "HI": "Hawaii",
		  "ID": "Idaho",
		  "IL": "Illinois",
		  "IN": "Indiana",
		  "IA": "Iowa",
		  "KS": "Kansas",
		  "KY": "Kentucky",
		  "LA": "Louisiana",
		  "ME": "Maine",
		  "MD": "Maryland",
		  "MA": "Massachusetts",
		  "MI": "Michigan",
		  "MN": "Minnesota",
		  "MS": "Mississippi",
		  "MO": "Missouri",
		  "MT": "Montana",
		  "NE": "Nebraska",
		  "NV": "Nevada",
		  "NH": "New Hampshire",
		  "NJ": "New Jersey",
		  "NM": "New Mexico",
		  "NY": "New York",
		  "NC": "North Carolina",
		  "ND": "North Dakota",
		  "OH": "Ohio",
		  "OK": "Oklahoma",
		  "OR": "Oregon",
		  "PA": "Pennsylvania",
		  "RI": "Rhode Island",
		  "SC": "South Carolina",
		  "SD": "South Dakota",
		  "TN": "Tennessee",
		  "TX": "Texas",
		  "UT": "Utah",
		  "VT": "Vermont",
		  "VA": "Virginia",
		  "WA": "Washington",
		  "WV": "West Virginia",
		  "WI": "Wisconsin",
		  "WY": "Wyoming",
		  "AS": "American Samoa",
		  "DC": "District of Columbia",
		  "FM": "Federated States of Micronesia",
		  "GU": "Guam",
		  "MH": "Marshall Islands",
		  "MP": "Northern Mariana Islands",
		  "PW": "Palau",
		  "PR": "Puerto Rico",
		  "VI": "Virgin Islands",
		  "AE": "Armed Forces Africa",
		  "AA": "Armed Forces Americas",
		  "AE": "Armed Forces Canada",
		  "AE": "Armed Forces Europe",
		  "AE": "Armed Forces Middle East",
		  "AP": "Armed Forces Pacific"
		}


		#states and indexes 
		if any(True for x in States.keys() if x in words ):
			
			indexPattern = re.compile(r'\d{5}')
			
			for sc in States.keys():
				if sc in words:
					self.state = States[sc]

					i = words.index(sc) +1

					if indexPattern.match(words[i]):
						self.Zip= words[i]

					# ADRESS
					if 'PO' in words:
						j = words.index('PO') +3
						addr = words[j:i-1]
					else:
						bldPattern = re.compile(r'\d+')
						addr = []
						cntr = i-2
						while True:
							if not bldPattern.match(words[cntr]):
								addr.insert(0, words[cntr])
								cntr-=1
							else:
								addr.insert(0, words[cntr])
								break
					if len(addr)>0:self.address = ' '.join(addr)



		
			
			
			
			
			
				

		

	def analyse(self):
		# make all guessings in one command
		self.guessPosition()
		self.guessName()
		self.guessEmail()
		self.guessTitle()
		self.guessWeb()
		self.guessPhones()
		self.guessPOBox()
		self.guessAdress()

	def asDict(self):
		return {'category':self.category ,
				'position':self.position ,
				'title':self.title ,
				'first':self.first ,
				'last':self.last ,
				'organization':self.organization,
				'address':self.address,
				'poBox':self.poBox,
				'city':self.city ,
				'state':self.state ,
				'Zip':self.Zip ,
				'email':self.email ,
				'web':self.web ,
				'fax': self.fax,
				'phone': self.phone,
				'rawText':'|'.join(self.rawText)}

	def plotRaw(self):
		print 'PERSON RAW'

		for line in self.rawText:
			print 'p: ', line
		print
		print
		print

	def plotParsed(self):
		print
		print 'organization: ', self.organization
		print 'name: ', self.first, ' ', self.last
		print 'title: ', self.title
		print 'position: ', self.position
		print 'poBox: ', self.poBox
		print 'fax: ', self.fax
		print 'phones: ', self.phone
		print 'email: ', self.email
		print 'web: ', self.web
		print 'state: ', self.state
		print 'index: ', self.Zip
		print 'address: ', self.address





	
if __name__ ==' __main__':

	r = ['American Fidelity Assurance Co',
	'Bob Fleet',
	'PO Box 25523',
	'Oklahoma City OK ',
	'73125 ',
	'405-523-5309',
	'405-523-5425',
	'bob.fleet@af-group .com www.af-group.com']


	perk  = person(r)
	perk.analyse()

	perk.plotParsed()


