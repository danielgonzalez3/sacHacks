#!/usr/bin/env python3
''' 
 macOS Catalina 10.15.6
 Zoom Version 5.5.2 
'''
import speech_recognition as sr
import os, glob
import json
import datetime
import time
import subprocess
import pyautogui
import requests
import http.client
import pandas as pd
import spacy
from collections.abc import Iterable
from zoomus import components, ZoomClient, util
from datetime import date
from os import path
from igraph import *

nlp = spacy.load("en_core_web_sm")

client = ZoomClient('dD_Z1gcSQSSe588TyzTdJQ', 'sA77ty3FNTw4gOelV18PdEWdwbJynIxjJda6')
meetingID = '6487365240'
meetingPass = '9VryWd'

SUBJECTS = {"nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"}
OBJECTS = {"dobj", "dative", "attr", "oprd"}
BREAKER_POS = {"CCONJ", "VERB"}
NEGATIONS = {"no", "not", "n't", "never", "none"}


def main():
	print('\nStarting Project Jensen\n')
	
	df = pd.DataFrame()
	oldtime = time.time()
	setup(meetingID, meetingPass)
	try:
		df = scrapeUsers(df)
		print('Updating User List...')
		while(1):
			if time.time() - oldtime > 59:
				print('Updating User List...')
				oldtime = time.time()
				df = scrapeUsers(df)
	except:
		pass
		print('\nClosing Project Jensen\n')
		df.to_csv('user_list_'+date.today().strftime("%d-%m-%Y")+'.csv')
		print('\nSaving Output Data...')
		time.sleep(2)
		for root, dirs, files in os.walk("./"):
		    for file in files:
		        if file.endswith(".m4a"):
		             audio_path = os.path.join(root, file)
		             print(audio_path)
	print("\nGenerating Graph...\n")   
	g = Graph(directed=False)
	df = pd.read_csv('output_list.csv', error_bad_lines=False, warn_bad_lines=False, low_memory=False)
	df = df[["text"]].sample(frac=1).reset_index(drop=True)
	vsCount = 0
	for row in df.iterrows():
		text = row[1][0]
		nlp = spacy.load('en_core_web_lg')
		comment = nlp(text)
		svo = tuple(findSVOs(comment))
		for i in range(len(svo)):
			g.add_vertices(1)
			g.vs[vsCount]["id"] = vsCount
			g.vs[vsCount]["label"] = svo[i]
			vsCount += 1
	for v1 in g.vs:
			for v2 in g.vs:
				if(v1.index != v2.index):
					if(type(v1["label"]) == str):
						s1 = [v1["label"]]
						o1 = [v1["label"]]
					else:
						s1 = str.split(v1["label"][0])
						try:
							o1 = str.split(v1["label"][2])
						except:
							o1 = str.split(v1["label"][1])
					if (type(v2["label"]) == str):
						s2 = v2["label"]
						o2 = v2["label"]
					else:
						s2 = str.split(v2["label"][0])
						try:
							o2 = str.split(v2["label"][2])
						except:
							o2 = str.split(v2["label"][1])

                    # Compare words in subject and object
					for x in s1:
						for y in s2:
							if (x == y) and (x != "-pron-"):
								g.add_edge(v1.index, v2.index)
								break
					for x in o1:
						for y in o2:
							if (x == y) and (x != "-pron-"):
								g.add_edge(v1.index, v2.index)
								break

	weights = g.eigenvector_centrality()
	g.vs['weight'] = weights
	print(g)
	visual_style = {}
	visual_style["bbox"] = (1600, 1600)
	visual_style["vertex_size"] = 20
	visual_style["margin"] = 350
	visual_style["vertex_label_size"] = 15
	visual_style["layout"] = g.layout_circle()
	plot(g, 'output.png', **visual_style)


	
# Automate Zoom Deployment 
def setup(id, pswd): 
	# subprocess.call('C:\\myprogram.exe') [For Windows]
	subprocess.call(["/usr/bin/open", "/Applications/zoom.us.app"]) 
	time.sleep(8)
	x1, y1 = pyautogui.locateCenterOnScreen('join_btn_lrg.png')
	pyautogui.moveTo(x1-650, y1-340)
	pyautogui.click()
	pyautogui.write(id)
	pyautogui.press('enter') 
	time.sleep(4)
	pyautogui.press('enter') 



def scrapeUsers(df):
	user_list = json.loads(client.user.list().content)
	tmp_df = pd.DataFrame()
	for user in user_list['users']:
		# EX: user id: Q3rbf2H1SvmNNkDqJnGvXg ---> content = json.loads(client.meeting.list(user_id='Q3rbf2H1SvmNNkDqJnGvXg').content)
		# content = json.loads(client.user.get(id='Q3rbf2H1SvmNNkDqJnGvXg').content)
		content = json.loads(client.user.get(id=user['id']).content)
		tmp_df = tmp_df.append(content, ignore_index=True)
		tmp_df = tmp_df[['first_name', 'last_name', 'account_id','email','pic_url']] 
		tmp_df['timeLogged'] = '0'
		tmp_df["timeLogged"] = tmp_df["timeLogged"].astype(int)
		time.sleep(1)

	if(len(df.index) == 0):
		df = tmp_df
	else:
		df = pd.concat([df, tmp_df])
		df = df.drop_duplicates(keep="first",subset=['account_id'])

	df["timeLogged"] = df["timeLogged"] + 1

	return df

def retrieveMeeting():
	conn = http.client.HTTPSConnection("api.zoom.us")
	headers = { 'authorization': "Bearer eyJhbGciOiJIUzUxMiIsInYiOiIyLjAiLCJraWQiOiI3N2JkYWY3Ny05N2YzLTRiN2MtOGJiNS04Y2NhZWY3NWEyOTUifQ.eyJ2ZXIiOjcsImF1aWQiOiJiOGE4OTJhMzMxZmQzYWNkYzM3ZDU3NTgwNTYyY2IxYSIsImNvZGUiOiJrMnkzSGVMbjcyX1EzcmJmMkgxU3ZtTk5rRHFKbkd2WGciLCJpc3MiOiJ6bTpjaWQ6azl1clJxSVJiV3Y5QlRWaXNrOHciLCJnbm8iOjAsInR5cGUiOjAsInRpZCI6MCwiYXVkIjoiaHR0cHM6Ly9vYXV0aC56b29tLnVzIiwidWlkIjoiUTNyYmYySDFTdm1OTmtEcUpuR3ZYZyIsIm5iZiI6MTYxMzg2OTYzMiwiZXhwIjoxNjEzODczMjMyLCJpYXQiOjE2MTM4Njk2MzIsImFpZCI6InJQZ2xfSXJxU0tHT2M3U2wyY1lOa1EiLCJqdGkiOiI0YjgxMGZhNS1kN2EzLTQ2NWYtOWUyOS01ZGE4NmVmZTI2NzAifQ.pTycvFFYIM-0b9GjT6TSAW5yBa2pmIx9TI1BXDZtSjWo48FsUPIdXcdJh4p4MpbFNHB-kTdA1wWINkqOWNp38w" }
	conn.request("GET", "/v2/meetings/6487365240/recordings", headers=headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))


def json2xml(json_obj, line_padding=""):
    result_list = list()
    json_obj_type = type(json_obj)
    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))
        return "\n".join(result_list)
    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))
        return "\n".join(result_list)
    return "%s%s" % (line_padding, json_obj)

def contains_conj(depSet):
    return "and" in depSet or "or" in depSet or "nor" in depSet or \
           "but" in depSet or "yet" in depSet or "so" in depSet or "for" in depSet


# Get subs joined by conjunctions
def _get_subs_from_conjunctions(subs):
    more_subs = []
    for sub in subs:
        # rights is a generator
        rights = list(sub.rights)
        rightDeps = {tok.lower_ for tok in rights}
        if contains_conj(rightDeps):
            more_subs.extend([tok for tok in rights if tok.dep_ in SUBJECTS or tok.pos_ == "NOUN"])
            if len(more_subs) > 0:
                more_subs.extend(_get_subs_from_conjunctions(more_subs))
    return more_subs


# Get objects joined by conjunctions
def _get_objs_from_conjunctions(objs):
    more_objs = []
    for obj in objs:
        # rights is a generator
        rights = list(obj.rights)
        rightDeps = {tok.lower_ for tok in rights}
        if contains_conj(rightDeps):
            more_objs.extend([tok for tok in rights if tok.dep_ in OBJECTS or tok.pos_ == "NOUN"])
            if len(more_objs) > 0:
                more_objs.extend(_get_objs_from_conjunctions(more_objs))
    return more_objs


# Find sub dependencies
def _find_subs(tok):
    head = tok.head
    while head.pos_ != "VERB" and head.pos_ != "NOUN" and head.head != head:
        head = head.head
    if head.pos_ == "VERB":
        subs = [tok for tok in head.lefts if tok.dep_ == "SUB"]
        if len(subs) > 0:
            verb_negated = _is_negated(head)
            subs.extend(_get_subs_from_conjunctions(subs))
            return subs, verb_negated
        elif head.head != head:
            return _find_subs(head)
    elif head.pos_ == "NOUN":
        return [head], _is_negated(tok)
    return [], False


# Is the tok set's left or right negated?
def _is_negated(tok):
    parts = list(tok.lefts) + list(tok.rights)
    for dep in parts:
        if dep.lower_ in NEGATIONS:
            return True
    return False


# Get all the verbs on tokens with negation marker
def _find_svs(tokens):
    svs = []
    verbs = [tok for tok in tokens if tok.pos_ == "VERB"]
    for v in verbs:
        subs, verbNegated = _get_all_subs(v)
        if len(subs) > 0:
            for sub in subs:
                svs.append((sub.orth_, "!" + v.orth_ if verbNegated else v.orth_))
    return svs


# Get grammatical objects for a given set of dependencies (including passive sentences)
def _get_objs_from_prepositions(deps, is_pas):
    objs = []
    for dep in deps:
        if dep.pos_ == "ADP" and (dep.dep_ == "prep" or (is_pas and dep.dep_ == "agent")):
            objs.extend([tok for tok in dep.rights if tok.dep_ in OBJECTS or
                         (tok.pos_ == "PRON" and tok.lower_ == "me") or
                         (is_pas and tok.dep_ == 'pobj')])
    return objs


# Get objects from the dependencies using the attribute dependency
def _get_objs_from_attrs(deps, is_pas):
    for dep in deps:
        if dep.pos_ == "NOUN" and dep.dep_ == "attr":
            verbs = [tok for tok in dep.rights if tok.pos_ == "VERB"]
            if len(verbs) > 0:
                for v in verbs:
                    rights = list(v.rights)
                    objs = [tok for tok in rights if tok.dep_ in OBJECTS]
                    objs.extend(_get_objs_from_prepositions(rights, is_pas))
                    if len(objs) > 0:
                        return v, objs
    return None, None


# Xcomp; open complement - verb has no suject
def _get_obj_from_xcomp(deps, is_pas):
    for dep in deps:
        if dep.pos_ == "VERB" and dep.dep_ == "xcomp":
            v = dep
            rights = list(v.rights)
            objs = [tok for tok in rights if tok.dep_ in OBJECTS]
            objs.extend(_get_objs_from_prepositions(rights, is_pas))
            if len(objs) > 0:
                return v, objs
    return None, None


# Get all functional subjects adjacent to the verb passed in
def _get_all_subs(v):
    verb_negated = _is_negated(v)
    subs = [tok for tok in v.lefts if tok.dep_ in SUBJECTS and tok.pos_ != "DET"]
    if len(subs) > 0:
        subs.extend(_get_subs_from_conjunctions(subs))
    else:
        foundSubs, verb_negated = _find_subs(v)
        subs.extend(foundSubs)
    return subs, verb_negated


# Find the main verb - or any aux verb if we can't find it
def _find_verbs(tokens):
    verbs = [tok for tok in tokens if _is_non_aux_verb(tok)]
    if len(verbs) == 0:
        verbs = [tok for tok in tokens if _is_verb(tok)]
    return verbs


# Is the token a verb?  (excluding auxiliary verbs)
def _is_non_aux_verb(tok):
    return tok.pos_ == "VERB" and (tok.dep_ != "aux" and tok.dep_ != "auxpass")


# Is the token a verb?  (excluding auxiliary verbs)
def _is_verb(tok):
    return tok.pos_ == "VERB" or tok.pos_ == "AUX"


# return the verb to the right of this verb in a CCONJ relationship if applicable
# returns a tuple, first part True|False and second part the modified verb if True
def _right_of_verb_is_conj_verb(v):
    # rights is a generator
    rights = list(v.rights)

    # VERB CCONJ VERB (e.g. he beat and hurt me)
    if len(rights) > 1 and rights[0].pos_ == 'CCONJ':
        for tok in rights[1:]:
            if _is_non_aux_verb(tok):
                return True, tok

    return False, v


# get all objects for an active/passive sentence
def _get_all_objs(v, is_pas):
    # rights is a generator
    rights = list(v.rights)

    objs = [tok for tok in rights if tok.dep_ in OBJECTS or (is_pas and tok.dep_ == 'pobj')]
    objs.extend(_get_objs_from_prepositions(rights, is_pas))

    # potentialNewVerb, potentialNewObjs = _get_objs_from_attrs(rights)
    # if potentialNewVerb is not None and potentialNewObjs is not None and len(potentialNewObjs) > 0:
    #    objs.extend(potentialNewObjs)
    #    v = potentialNewVerb

    potential_new_verb, potential_new_objs = _get_obj_from_xcomp(rights, is_pas)
    if potential_new_verb is not None and potential_new_objs is not None and len(potential_new_objs) > 0:
        objs.extend(potential_new_objs)
        v = potential_new_verb
    if len(objs) > 0:
        objs.extend(_get_objs_from_conjunctions(objs))
    return v, objs


# return true if the sentence is passive - at he moment a sentence is assumed passive if it has an auxpass verb
def _is_passive(tokens):
    for tok in tokens:
        if tok.dep_ == "auxpass":
            return True
    return False


# resolve a 'that' where/if appropriate
def _get_that_resolution(toks):
    for tok in toks:
        if 'that' in [t.orth_ for t in tok.lefts]:
            return tok.head
    return toks


def _get_lemma(word: str):
    tokens = nlp(word)
    if len(tokens) == 1:
        return tokens[0].lemma_
    return word


def printDeps(toks):
    for tok in toks:
        print(tok.orth_, tok.dep_, tok.pos_, tok.head.orth_, [t.orth_ for t in tok.lefts],
              [t.orth_ for t in tok.rights])


def expand(item, tokens, visited):
    if item.lower_ == 'that':
        item = _get_that_resolution(tokens)

    parts = []

    if hasattr(item, 'lefts'):
        for part in item.lefts:
            if part.pos_ in BREAKER_POS:
                break
            if not part.lower_ in NEGATIONS:
                parts.append(part)

    parts.append(item)

    if hasattr(item, 'rights'):
        for part in item.rights:
            if part.pos_ in BREAKER_POS:
                break
            if not part.lower_ in NEGATIONS:
                parts.append(part)

    if hasattr(parts[-1], 'rights'):
        for item2 in parts[-1].rights:
            if item2.pos_ == "DET" or item2.pos_ == "NOUN":
                if item2.i not in visited:
                    visited.add(item2.i)
                    parts.extend(expand(item2, tokens, visited))
            break

    return parts


def to_str(tokens):
    if isinstance(tokens, Iterable):
        try:
            return ' '.join([item.lemma_.lower() for item in tokens])
        except:
            return ' '.join([item.text for item in tokens])
    else:
        return ''


def findSVOs(tokens):
    svos = []
    is_pas = _is_passive(tokens)
    verbs = _find_verbs(tokens)
    visited = set()  
    for v in verbs:
        subs, verbNegated = _get_all_subs(v)
        if len(subs) > 0:
            isConjVerb, conjV = _right_of_verb_is_conj_verb(v)
            if isConjVerb:
                v2, objs = _get_all_objs(conjV, is_pas)
                for sub in subs:
                    for obj in objs:
                        objNegated = _is_negated(obj)
                        if is_pas:  # reverse object / subject for passive
                            svos.append((to_str(expand(obj, tokens, visited)),
                                         "!" + v.lemma_ if verbNegated or objNegated else v.lemma_,
                                         to_str(expand(sub, tokens, visited))))
                            svos.append((to_str(expand(obj, tokens, visited)),
                                         "!" + v2.lemma_ if verbNegated or objNegated else v2.lemma_,
                                         to_str(expand(sub, tokens, visited))))
                        else:
                            svos.append((to_str(expand(sub, tokens, visited)),
                                         "!" + v.lower_ if verbNegated or objNegated else v.lower_,
                                         to_str(expand(obj, tokens, visited))))
                            svos.append((to_str(expand(sub, tokens, visited)),
                                         "!" + v2.lower_ if verbNegated or objNegated else v2.lower_,
                                         to_str(expand(obj, tokens, visited))))
            else:
                v, objs = _get_all_objs(v, is_pas)
                for sub in subs:
                    if len(objs) > 0:
                        for obj in objs:
                            objNegated = _is_negated(obj)
                            if is_pas:  
                                svos.append((to_str(expand(obj, tokens, visited)),
                                             "!" + v.lemma_ if verbNegated or objNegated else v.lemma_,
                                             to_str(expand(sub, tokens, visited))))
                            else:
                                svos.append((to_str(expand(sub, tokens, visited)),
                                             "!" + v.lower_ if verbNegated or objNegated else v.lower_,
                                             to_str(expand(obj, tokens, visited))))
                    else:
                        svos.append((to_str(expand(sub, tokens, visited)),
                                     "!" + v.lower_ if verbNegated else v.lower_,))

    return svos

if __name__ == "__main__":
    main()