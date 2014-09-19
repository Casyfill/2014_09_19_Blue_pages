

class person:
	category = ''
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
	rawText = []
	
	def __init__(self, raw, cat='?'):
		self.rawText = raw
		self.category = cat

	def guessEmail(self):
		result = []
		for line in self.rawText:
			if '@' in line:
				line.replace(' .','').trim()
				ar = line.split()
		
				for mail in ar:
					if '@' in mail:
						result.append(mail)
		if len(result)!=0:
			self.email=', '.join(result)

	def guessTitle(self):
		self.title = self.rawText[0]

	def guessName(self):
		self.title = self.rawText[1]

	def plotRaw(self):
		print 'PERSON RAW'

		for line in self.rawText:
			print 'p: ', line
		print
		print
		print 


				

path = "/Users/f.kac/Dropbox (RN&IA'N)/My_Projects/Blue_pages/data/C1_cleaned.txt"

personList = []

with open(path,'rb') as readFile:	
	mode = False
	personText=[]

	for line in readFile:
		line=line.decode('utf-8').replace(' .','.').strip()
		# print line
		if len(line)!=0:
			if mode==False:
				personText=[]
				personText.append(line)
				mode=True
			else:
				# print '!!'
				personText.append(line)
		else:
			# print 'new person'
			if mode==True:
				personList.append( person(personText))
				mode = False
			else:
				pass


for p in personList:
	# print
	# print
	# print 'persona'
	# for line in p:
	# 	print line
	p.guessTitle()
	p.guessName()
	p.guessEmail()

	print 'email:', p.email()

	p.plotRaw()

		

