# -*- coding: utf-8 -*-

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

def orgs(text):
	st = StanfordNERTagger('trained_modal/stanford_ner/classifiers/english.all.3class.distsim.crf.ser.gz',
						   'trained_modal/stanford_ner/stanford-ner.jar',
						   encoding='utf-8')

	tokenized_text = word_tokenize(text)
	classified_text = st.tag(tokenized_text)

	names_list = []
	for tag_tuple in classified_text:
		if tag_tuple[1] == 'ORGANIZATION':
			names_list.append(tag_tuple[0])

	return names_list
