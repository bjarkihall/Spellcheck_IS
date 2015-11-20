#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys,collections, csv
import random

allWords={}

#Hash function for storing frequency based on sandwich
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
	'gn':62,
	'gs':63,
	'gf':64,
	'gl':65,
	'gc':66,
	'ga':67,
	'ng':68,
	'sg':69,
	'fg':70,
	'lg':71,
	'cg':72,
	'ag':73,
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
	'!t':181
	}[sandwich]

files = [
"althingi_tagged/079.csv", 
"althingi_tagged/080.csv", 
"althingi_tagged/081.csv", 
"althingi_tagged/082.csv",
"althingi_tagged/083.csv",
"althingi_tagged/084.csv",
"althingi_tagged/085.csv",
"althingi_tagged/093.csv"]

for x in range(0,len(files)):
	with open(files[x]) as csvfile:
		fieldnames = ['word', 'case', 'lemma']
		reader = csv.DictReader(csvfile, fieldnames=fieldnames)
		next(reader)
		prevWord='.'
		prevCase='.'
		allWords[prevWord]=[1,prevCase,{}]
		sandwich=prevCase
		for row in reader:
			currWord = row['word']
			#currWord = currWord.lower()
			currCase=row['case'][:1]
			if (currWord=='' or currWord=="=" or currWord=='\'' or currWord=="+" or currWord=="-" or currWord=="[" or currWord=="]" or currWord=="/"or currWord==":" or currWord=='(' or currWord==')' or currWord==","):
				continue
			#if this is the first time we have encountered this word
			if not allWords.get(currWord):
				allWords[currWord]=[1,prevCase,{}]
			else:
				allWords[currWord][0]=allWords[currWord][0]+1
			#If we are at the beginning of the file
			if (len(sandwich)>2):
				sandwich=sandwich 
			prevWord2back=prevWord
			prevCase2back=prevCase
			sandwich=prevCase2back+currCase
			sandwichIndex=sandwichToNumber(sandwich)
			print sandwichIndex
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

#All possible variations with edi distance=2
def known_edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words) : return set(w for w in words if w in NWORDS)

def correct(word, sandwich):
	candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
	#print "sandwich: ",sandwich
	#print "word: ", word
	return max(candidates, key=lambda x: getFrequency(x,sandwich))

def getFrequency (word, sandwich):
	#Psuedo-count of small frequency if the word has not been trained on
	if (not allWords.get(word)):
		return 0.0001
	else:
	 return allWords[word][2].get(sandwich)

def practice():
	wrong=0
	right=0
	with open('althingi_errors/079.csv') as csvfile:
		fieldnames = ['word', 'case', 'lemma', 'correctWord']
		reader = csv.DictReader(csvfile, fieldnames=fieldnames)
		next(reader)
		prev2Word='.'
		prev2Case='.'
		prev2Correct='.'
		prevWord=next(reader)['word']
		prevCase=next(reader)['case'][:1]
		prevCorrect=next(reader)['correctWord']
		for row in reader:
			currWord=row['word']
			currCase=row['case'][:1]
			currCorrect=row['correctWord']
			if (currWord=='' or currWord== "=" or currWord=='\'' or currWord=="+" or currWord=="-" or currWord=="[" or currWord=="]" or currWord=="/"or currWord==":" or currWord=='(' or currWord==')' or currWord==","):
				continue
			prevSandwich=prev2Case+currCase
			myAnswer=correct(prevWord,prevSandwich)
			if (myAnswer != prevCorrect):
				wrong +=1
				print "PrevWord:", prevWord, "MyAnswer: ", myAnswer, "CorrectWord: ", prevCorrect
			else:
				right +=1
			prev2Word=prevWord
			prev2Case=prevCase
			prev2Correct=prevCorrect
			prevWord=currWord
			prevCase=currCase
			prevCorrect=currCorrect
	print "WRONG: ", wrong
	print "RIGHT: ", right
	print "RATIO: ", wrong/right

#print correct("pég")
practice()
