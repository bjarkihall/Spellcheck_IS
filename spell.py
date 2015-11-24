#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys, collections, csv, random

allWords={}

#Store name of the inputFile from the commandLine
inputFileName= sys.argv[1]
outputFileName=sys.argv[2]


#Hash function that takes in a sandwich value and returns an index #
#Sandwich is a 2-letter string that represents the context for a word.
#First letter represents the type of word that precedes the current word
#Second letter represents the type of word that follows the current word
#e.g.: if a word's sandwich is 'nl', then we know it is preceded by a noun
#(nafnord) and is followed by an adjective (lysingarord)
def sandwichToNumber(sandwich):
	return{
	'nn':0,
	'ns':1,
	'nf':2,
	'nl':3,
	'nc':4,
	'na':5,
	'sn':6,
	'ss':7,
	'sf':8,
	'sl':9,
	'sc':10,
	'sa':11,
	'fn':12,
	'fs':13,
	'ff':14,
	'fl':15,
	'fc':16,
	'fa':17,
	'ln':18,
	'ls':19,
	'lf':20,
	'll':21,
	'lc':22,
	'la':23,
	'cn':24,
	'cs':25,
	'cf':26,
	'cl':27,
	'cc':28,
	'ca':29,
	'an':30,
	'as':31,
	'af':32,
	'al':33,
	'ac':34,
	'aa':35,
	'.n':36,
	'.s':37,
	'.f':38,
	'.l':39,
	'.c':40,
	'.a':41,
	'n.':42,
	's.':43,
	'f.':44,
	'l.':45,
	'c.':46,
	'a.':47,
	'tn':48,
	'ts':49,
	'tf':50,
	'tl':51,
	'tc':52,
	'ta':53,
	'nt':54,
	'st':55,
	'ft':56,
	'lt':57,
	'ct':58,
	'at':59,
	'.t':60,
	't.':61,
	'?:':62,
	'.:':63,
	';:':64,
	'!:':65,
	't:':66,
	';?':67,
	'gx':73,
	'.g':74,
	'g.':75,
	'?n':76,
	'?s':77,
	'?f':78,
	'?l':79,
	'?c':80,
	'?a':81,
	'n?':82,
	's?':83,
	'f?':84,
	'l?':85,
	'c?':86,
	'a?':87,
	'.?':88,
	'?.':89,
	'!n':90,
	'!s':91,
	'!f':92,
	'!l':93,
	'!c':94,
	'!a':95,
	'n!':96,
	's!':97,
	'f!':98,
	'l!':99,
	'c!':100,
	'a!':101,
	'.!':102,
	'!.':103,
	';n':104,
	';s':105,
	';f':106,
	';l':107,
	';c':108,
	';a':109,
	'n;':110,
	's;':111,
	'f;':112,
	'l;':113,
	'c;':114,
	'a;':115,
	';!':116,
	'!;':117,
	'tt':118,
	't;':119,
	';t':120,
	'en':121,
	'es':122,
	'ef':123,
	'el':124,
	'ec':125,
	'ea':126,
	'ne':127,
	'se':128,
	'fe':129,
	'le':130,
	'ce':131,
	'ae':132,
	';e':133,
	'!e':134,
	'te':135,
	'et':136,
	'gn':137,
	'gs':138,
	'gf':139,
	'gl':140,
	'gc':141,
	'ga':142,
	'ng':143,
	'sg':144,
	'fg':145,
	'lg':146,
	'cg':147,
	'ag':148,
	';g':149,
	'!g':150,
	'tg':151,
	'eg':152,
	'xn':153,
	'xs':154,
	'xf':155,
	'xl':156,
	'xc':157,
	'xa':158,
	'nx':159,
	'sx':160,
	'fx':161,
	'lx':162,
	'cx':163,
	'ax':164,
	';x':165,
	'!x':166,
	'tx':167,
	'ex':168,
	't?':170,
	'?t':171,
	'gt':172,
	'x.':173,
	'?g':174,
	'..':175,
	'ee':176,
	'.x':177,
	'xt':178,
	'e.':179,
	'g?':180,
	'!t':181,
	'xx':182,
	'x;':183,
	'e;':184,
	'.e':185,
	'?x':186,
	'.;':187,
	'x!':188,
	'x?':189,
	'?e':190,
	'xg':191,
	'e?':192,
	'g:':193,
	'g;':194,
	';.':195,
	'!!':196,
	't!':197,
	'xe':198,
	'?;':199,
	'??':200,
	'!?':201,
	'ge':202,
	';;':203,
	'g!':204,
	'?!':205,
	'e!':206,
	'a:':207,
	'c:':208,
	'e:':209,
	'f:':210,
	'l:':211,
	'x:':212,
	's:':213,
	'n:':214,
	'gg':215,
	'uu':216
	}[sandwich]

#Array of file names for our training data

files = [
"althingi_tagged/099.csv"#,
#"althingi_tagged/100.csv",
#"althingi_tagged/101.csv",
#"althingi_tagged/102.csv"
]

#These characters will be ignored during scanning
specialChars =['','»', '«', '\\', '{', '}', '±', '^', '_', '>','<', '´','`', "*","$",'\"',"=",'\'',"+","-","[","]","/",":",'(',')',","]

#Helper Function to determine if a string is all numeric digits
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

#Helper function to determine if a sandwich exists in our hash-key options
def sandwich_is_known(sandwich):
	try:
		x = sandwichToNumber(sandwich)
		return x
	except ValueError:
		#'uu' is a catch-all key for "Unknown-Unknown", for any unknown sandwiches
		return sandwichToNumber('uu')

#Iterate through all the training data Files to build our dictionary
for x in range(0,len(files)):
	#For each file of our training data
	with open(files[x]) as csvfile:
		fieldnames = ['word', 'tag', 'lemma']
		reader = csv.DictReader(csvfile, fieldnames=fieldnames)
		print "Building dictionary from", files[x], "..."
		next(reader) #skip the Column headers
		prevWord='.'
		prevCase='.'
		allWords[prevWord]=[1,prevCase,{}]
		sandwich=prevCase
		#For each word, tally up the frequency and context (sandwich) where we found it
		for row in reader:
			currWord = row['word']
			#Only use the first character from the "tag" column
			currCase=row['tag'][:1]
			#Skip if its a special character
			if (currWord in specialChars):
				continue
			#Skip if its a number
			if (is_number(currWord)):
				continue
			#if this is the first time we have encountered this word, initiate its entry in the hashTable
			if not allWords.get(currWord):
				allWords[currWord]=[1,prevCase,{}]
			#if we have seen it before, increment its frequency
			else:
				allWords[currWord][0]=allWords[currWord][0]+1
			#If we are at the beginning of the file
			if (len(sandwich)>2):
				sandwich=sandwich
			#We need to always have access to the previous 2 words plus current word
			#So that we will always have a 3-mer set of words 
			prevWord2back=prevWord
			prevCase2back=prevCase
			#We cant see the full sandwich of a word until we've read data from the 
			#word that follows it, so anytime we scan in a new word, we are then "looking back"
			#and processing the sandwich of the word that came before it
			sandwich=prevCase2back+currCase
			sandwichIndex=sandwich_is_known(sandwich)
			#If this is our first instance of the word in this particular context/sandwich,
			#initialize the hashValue for that pairing. otherwise, increment +1
			if not allWords[prevWord][2].get(sandwichIndex):
				allWords[prevWord][2][sandwichIndex]=1
			else: 
				allWords[prevWord][2][sandwichIndex]+=1
			prevWord=currWord
			prevCase=currCase

def words(text): return re.findall('[a-ö]+', text.lower())

def train(features):
	model = allWords
	return model

NWORDS = train(allWords)

alphabet = "aábcdeéfghiíjklmnoópqrstuúvwxyzþæö"

#Dictionary with all possible variations with edit distance=1
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

#All possible variations with edit distance=2
def known_edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

#remove any non-sensical words (e.g. dthr)
def known(words) : return set(w for w in words if w in NWORDS)

#returns the most probable (highest frequency within sandwich) word from the collection of all
#possible/real words that are <3 Levenstein distance from word.
def correct(word, sandwich):
	candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
	return max(candidates, key=lambda x: getFrequency(x,sandwich))

def getFrequency (word, sandwich):
	#Psuedo-count of small frequency if a new word is introduced that model has not been trained on
	if (not allWords.get(word)):
		return 0.0001
	else:
		confirmedSandwich=sandwich_is_known(sandwich)
		return allWords[word][2].get(confirmedSandwich)

#Test our model on some text with corrected errors
def proofRead(file):
	#These variables will track our accuracy
	ff = 0
	fp = 0
	pf = 0
	pp = 0
	a_w = []
	a_cw = []
	m_cw = []
	errorsFound=0
	titles=['Word','Tag','Lemma','CorrectWord']

	print ("Proofreading your file now...")
	with open(file) as csvfile:
		fieldnames = ['word', 'tag', 'lemma']
		reader = csv.DictReader(csvfile, fieldnames=fieldnames)
		#Mechanism to write to a .csv file
		myFile=open(outputFileName,'wb')
		wr=csv.writer(myFile,quoting=csv.QUOTE_ALL)
		wr.writerow(titles)
		next(reader)
		prev2Word='.'
		prev2Case='.'
		prev2Correct='.'
		prev2Tag='.'
		prev2Lemma='.'
		prevWord=next(reader)['word']
		prevCase=next(reader)['tag'][:1]
		prevTag=next(reader)['tag']
		prevLemma=next(reader)['lemma']

		nrTestRows = -1
		for row in reader:
			#for testing:
			if (nrTestRows == 5):
				break
			nrTestRows+=1

			correctedRow=[] #temporary storage of a word-correction
			currWord=row['word']
			currCase=row['tag'][:1]
			currTag=row['tag']
			currLemma=row['lemma']

			print "before: " + str(nrTestRows) + ", currWord: " + currWord
			
			#Skip special Characters
			if (currWord in specialChars):
				continue
			
			print "after specials: " + str(nrTestRows)
			
			if (is_number(currWord)):
				continue
			
			print "after numbers: " + str(nrTestRows)
			
			prevSandwich=prev2Case+currCase

			#Use our model to predict the correct spelling
			myAnswer=correct(prevWord,prevSandwich)
			if (myAnswer=='i'):
				myAnswer='í'
			if (myAnswer != prevWord):
				errorsFound += 1
			#Store data for this row
			correctedRow.append(prevWord)
			correctedRow.append(prevTag)
			correctedRow.append(prevLemma)
			correctedRow.append(myAnswer)
			wr.writerow(correctedRow) #Send this result to our outputFile
			#Update our variables for next iteration
			prev2Word=prevWord
			prev2Case=prevCase
			prev2Tag=prevTag
			prev2Lemma=prevLemma
			prevWord=currWord
			prevCase=currCase
			prevTag=currTag
			prevLemma=currLemma

			###

			#Accuracy:

		print errorsFound, " errors found"
		print "Results now available in ", outputFileName
	
proofRead(inputFileName)
