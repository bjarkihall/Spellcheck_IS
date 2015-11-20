#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re, sys,collections, csv
import random

allWords={}

with open('althingi_tagged/079.csv') as csvfile:
	fieldnames = ['word', 'case', 'lemma']
	reader = csv.DictReader(csvfile, fieldnames=fieldnames)
	prevWord='.'
	prevCase='.'
	for row in reader:
		currWord = row['word']
		currWord = currWord.lower()
		currCase=row['case'][:1]
		#allWords[prevWord][1]+=currCase
		print currWord
		print currCase
		#if not allWords[currWord]:
			#allWords[currWord]=[1,prevCase]
	
		

def words(text): return re.findall('[a-ö]+', text.lower())

def train(features):
	model = collections.defaultdict(lambda:1)
	for f in features:
		model[f] += 1
	return model

NWORDS = train(words(file('althingi_text/079.txt').read()))

alphabet = "aábcdeéfghiíjklmnoópqrstuúvwxyzþæö"

#Dictionary with all possible variations with edit distance=1
def edits1(word):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
	return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words) : return set(w for w in words if w in NWORDS)

def correct(word):
	candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
	return max(candidates, key=NWORDS.get)

print correct("pég")
