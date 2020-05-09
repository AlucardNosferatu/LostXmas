# -*- coding: utf-8 -*-
import os
from ie import TripleIE
from pyltp import Segmentor, Postagger, Parser, NamedEntityRecognizer
from tqdm import tqdm
import utils as U
import time

input=os.path.abspath('.')+"\\Preparation\\NER\\TripleIE-master\\data\\mysample.txt"
model=os.path.abspath('.')+"\\Preparation\\NER\\TripleIE-master\\ltp_data_v3.4.0"
output=os.path.abspath('.')+"\\Preparation\\NER\\TripleIE-master\\out\\mysample.txt"

def build_sub_dicts(words,postags,arcs):
	sub_dicts = []
	for idx in range(len(words)):
		sub_dict = dict()
		for arc_idx in range(len(arcs)):
			if arcs[arc_idx].head==idx+1:
				if arcs[arc_idx].relation in sub_dict:
					sub_dict[arcs[arc_idx].relation].append(arc_idx)
				else:
					sub_dict[arcs[arc_idx].relation]=[]
					sub_dict[arcs[arc_idx].relation].append(arc_idx)
		sub_dicts.append(sub_dict)
	return sub_dicts

def fill_ent(words,postags,sub_dicts,word_idx):
	sub_dict = sub_dicts[word_idx]
	prefix = ''
	if 'ATT' in sub_dict:
		for i in range(len(sub_dict['ATT'])):
			prefix += fill_ent(words,postags,sub_dicts,sub_dict['ATT'][i])
	postfix = ''
	if postags[word_idx] == 'v':
		if 'VOB' in sub_dict:
			postfix += fill_ent(words,postags,sub_dicts,sub_dict['VOB'][0])
		if 'SBV' in sub_dict:
			prefix = fill_ent(words,postags,sub_dicts,sub_dict['SBV'][0])+prefix
	return prefix + words[word_idx] + postfix

def SBV_VOB(idx, out_handle, postags, sub_dict, sub_dicts, words):
	e1 = fill_ent(words,postags,sub_dicts,sub_dict['SBV'][0])
	r=words[idx]
	e2 = fill_ent(words,postags,sub_dicts,sub_dict['VOB'][0])
	out_handle.write("主谓宾\t(%s, %s, %s)\n" % (e1, r, e2))
	#print("主谓宾\t(%s, %s, %s)\n" % (e1, r, e2))
	out_handle.flush()

def ATT_VOB(arcs, idx, out_handle, postags, sub_dict, sub_dicts, words):
	e1 = fill_ent(words,postags,sub_dicts,arcs[idx].head-1)
	r=words[idx]
	e2 = fill_ent(words,postags,sub_dicts,sub_dict['VOB'][0])
	temp=r+e2
	if temp not in e1:
		out_handle.write("动宾定语后置\t(%s, %s, %s)\n" % (e1, r, e2))
		#print("动宾定语后置\t(%s, %s, %s)\n" % (e1, r, e2))
		out_handle.flush()
	else:
		pass

def InitExtractor(parser, pos, rec, seg, sentence):
	words=seg.segment(sentence)
	postags=pos.postag(words)
	ner=rec.recognize(words,postags)
	arcs=parser.parse(words,postags)
	sub_dicts=build_sub_dicts(words,postags,arcs)
	return arcs, ner, postags, sub_dicts, words

def HeadWordDetector(postags, idx, out_handle, sub_dicts, words, arcs):
	if postags[idx] == 'v':
		sub_dict = sub_dicts[idx]
		if(('SBV' in sub_dict)
			and ('VOB' in sub_dict)):
			SBV_VOB(idx, out_handle, postags, sub_dict, sub_dicts, words)
		if((arcs[idx].relation == 'ATT')
			and ('VOB' in sub_dict)):
			ATT_VOB(arcs, idx, out_handle, postags, sub_dict, sub_dicts, words)
	else:
		pass

def NER(ner, idx, out_handle, sentence):
		if((ner[idx][0]=='S') or (ner[idx][0]=='B')):
			try:
				ni=idx
				if ner[ni][0] == 'B':
					while((len(ner)>0) and (len(ner[ni])>0) and (ner[ni] != 'E]')):
						ni+=1
					e1=''.join(words[idx:ni+1])
				else:
					e1=words[ni]
				if((arcs[ni].relation == 'ATT') and (postags[arcs[ni].head-1]=='n') and (ner[arcs[ni].head-1]=='0')):
					r = fill_ent(words,postags,sub_dicts,arcs[ni].head-1)
					if e1 in r:
						r=r[(r.idx(e1)+len(e1)):]
					if((arcs[arcs[ni].head-1].relation=='ATT') and (ner[arcs[arcs[ni].head-1].head-1]!='0')):
						e2 = fill_ent(words,postags,sub_dicts,arcs[arcs[ni].head-1].head-1)
						mi = arcs[arcs[ni].head-1].head-1
						li=mi
						if ner[mi][0] == 'B':
							while ner[mi][0]!='E':
								mi+=1
							e = ''.join(words[li+1:mi+1])
							e2 += e
						if r in e2:
							e2 = e2[(e2.idx(r)+len(r)):]
						if r+e2 in sentence:
							out_handle.write("人名/地名/机构\t(%s, %s, %s)\n" % (e1, r, e2))
							#print("人名/地名/机构\t(%s, %s, %s)\n" % (e1, r, e2))
							out_handle.flush()
			except:
				pass
		else:
			pass

def extract(sentence,out_handle,seg,pos,rec,parser):
	arcs, ner, postags, sub_dicts, words = InitExtractor(parser, pos, rec, seg, sentence)
	for idx in range(len(postags)):
		HeadWordDetector(postags, idx, out_handle, sub_dicts, words, arcs)
		NER(ner, idx, out_handle, sentence)

segmentor=Segmentor()
segmentor.load(os.path.join(model, "cws.model"))
postagger=Postagger()
postagger.load(os.path.join(model, "pos.model"))
parser=Parser()
parser.load(os.path.join(model, "parser.model"))
recognizer = NamedEntityRecognizer()
recognizer.load(os.path.join(model, "ner.model"))

with open(input, "r", encoding="utf-8") as rf:
    text = ""
    for line in rf:
        line = line.strip()
        text += line
    text = U.rm_html(text)
    sentences = U.split_by_sign(text)
    out_handle = open(output, 'a')
    for sentence in tqdm(sentences,ncols=75):
        extract(sentence,out_handle,segmentor,postagger,recognizer,parser)
    out_handle.close()
