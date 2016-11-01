import os,subprocess, random
from nltk import word_tokenize, WordNetLemmatizer
from collections import Counter

def read_files(path):
	return  subprocess.check_output('find ' + path + ' -type f', shell=True).splitlines()
	
def read_file_contents(file_list):
	content_list = []
	for file in file_list:
		f = open(file,'r')
		content_list.append(f.read().replace('\n',' ').replace('\r',' '))
		f.close()
	return content_list


def preprocess(sentence):
	return [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(sentence)]

def get_features(text, setting,stoplist):
	if setting == 'bow':
		return {word: count for word, count in \
			Counter(preprocess(text)).items() \
			if not word in stoplist }
	else:
		return { word: True for word in preprocess(text) \
			if not word in stoplist }

	



	
