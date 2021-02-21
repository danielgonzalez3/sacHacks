''' 
 macOS Catalina 10.15.6
 Zoom Version 5.5.2 
'''
import json
import datetime
import time
from zoomus import components, ZoomClient, util
from datetime import date
import subprocess
import pyautogui
import requests
import http.client
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_lg')

client = ZoomClient('dD_Z1gcSQSSe588TyzTdJQ', 'sA77ty3FNTw4gOelV18PdEWdwbJynIxjJda6')
meetingID = '6487365240'

SUBJECTS = {"nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"}
OBJECTS = {"dobj", "dative", "attr", "oprd"}
BREAKER_POS = {"CCONJ", "VERB"}
NEGATIONS = {"no", "not", "n't", "never", "none"}


def main():
	df = pd.DataFrame()
	oldtime = time.time()
	print('brrr')
	while(1):
		if time.time() - oldtime > 59:
			print('doing the thing')
			df = scrapeUsers(df)
			oldtime = time.time()
			df.to_csv('user_list_'+date.today().strftime("%d-%m-%Y")+'.csv')
	

# Automate Zoom Deployment [Later On]
def setup(id, pswd):
	subprocess.call("usr/bin/open", "/Applications/zoom.us.app")
	time.sleep(8)
	join = pyautogui.locateCenterOnScreen('join_btn.png')
	pyautogui.moveTo(join)
	pyautogui.click()


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

def _is_negated(tok):
    parts = list(tok.lefts) + list(tok.rights)
    for dep in parts:
        if dep.lower_ in NEGATIONS:
            return True
    return False


def _find_svs(tokens):
    svs = []
    verbs = [tok for tok in tokens if tok.pos_ == "VERB"]
    for v in verbs:
        subs, verbNegated = _get_all_subs(v)
        if len(subs) > 0:
            for sub in subs:
                svs.append((sub.orth_, "!" + v.orth_ if verbNegated else v.orth_))
    return svs


def _get_objs_from_prepositions(deps, is_pas):
    objs = []
    for dep in deps:
        if dep.pos_ == "ADP" and (dep.dep_ == "prep" or (is_pas and dep.dep_ == "agent")):
            objs.extend([tok for tok in dep.rights if tok.dep_  in OBJECTS or
                         (tok.pos_ == "PRON" and tok.lower_ == "me") or
                         (is_pas and tok.dep_ == 'pobj')])
    return objs


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


def _get_all_subs(v):
    verb_negated = _is_negated(v)
    subs = [tok for tok in v.lefts if tok.dep_ in SUBJECTS and tok.pos_ != "DET"]
    if len(subs) > 0:
        subs.extend(_get_subs_from_conjunctions(subs))
    else:
        foundSubs, verb_negated = _find_subs(v)
        subs.extend(foundSubs)
    return subs, verb_negated


def _find_verbs(tokens):
    verbs = [tok for tok in tokens if _is_non_aux_verb(tok)]
    if len(verbs) == 0:
        verbs = [tok for tok in tokens if _is_verb(tok)]
    return verbs


def _is_non_aux_verb(tok):
    return tok.pos_ == "VERB" and (tok.dep_ != "aux" and tok.dep_ != "auxpass")


def _is_verb(tok):
    return tok.pos_ == "VERB" or tok.pos_ == "AUX"


def _right_of_verb_is_conj_verb(v):
    # rights is a generator
    rights = list(v.rights)

    # VERB CCONJ VERB (e.g. he beat and hurt me)
    if len(rights) > 1 and rights[0].pos_ == 'CCONJ':
        for tok in rights[1:]:
            if _is_non_aux_verb(tok):
                return True, tok

    return False, v


def _get_all_objs(v, is_pas):
    # rights is a generator
    rights = list(v.rights)

    objs = [tok for tok in rights if tok.dep_ in OBJECTS or (is_pas and tok.dep_ == 'pobj')]
    objs.extend(_get_objs_from_prepositions(rights, is_pas))

    #potentialNewVerb, potentialNewObjs = _get_objs_from_attrs(rights)
    #if potentialNewVerb is not None and potentialNewObjs is not None and len(potentialNewObjs) > 0:
    #    objs.extend(potentialNewObjs)
    #    v = potentialNewVerb

    potential_new_verb, potential_new_objs = _get_obj_from_xcomp(rights, is_pas)
    if potential_new_verb is not None and potential_new_objs is not None and len(potential_new_objs) > 0:
        objs.extend(potential_new_objs)
        v = potential_new_verb
    if len(objs) > 0:
        objs.extend(_get_objs_from_conjunctions(objs))
    return v, objs


def _is_passive(tokens):
    for tok in tokens:
        if tok.dep_ == "auxpass":
            return True
    return False


def _get_that_resolution(toks):
    for tok in toks:
        if 'that' in [t.orth_ for t in tok.lefts]:
            return tok.head
    return toks


def _get_lemma(nlp, word: str):
    tokens = nlp(word)
    if len(tokens) == 1:
        return tokens[0].lemma_
    return word


def printDeps(toks):
    for tok in toks:
        print(tok.orth_, tok.dep_, tok.pos_, tok.head.orth_, [t.orth_ for t in tok.lefts], [t.orth_ for t in tok.rights])

def removePunctuationCharacters(tokens:'list spacy tokens'):
    not_punctuation_token = [token for token in tokens if not token.is_punct]
    return not_punctuation_token

def expand(item, tokens, visited, removepunctuation=False):
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
                    parts.extend(expand(item2, tokens, visited,removepunctuation))
            break

    if removepunctuation:
        return removePunctuationCharacters(parts)
    return parts


def to_str(tokens):
    if isinstance(tokens, Iterable):
        return ' '.join([item.text for item in tokens])
    else:
        return ''

def uncontract(text:str):
    return ContractText().uncontract(text)

def findSVOs(nlp: "spacy doc", text:str,  removepunctuation=False, uncontracttext=False):
    if uncontracttext:
        text = uncontract(text)
    tokens = nlp(text)
    return _get_svos(tokens, removepunctuation)

def _get_svos(tokens, removepunctuation=False):
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
                        if is_pas:  
                            svos.append((to_str(expand(obj, tokens, visited, removepunctuation)),
                                         "!" + v.lemma_ if verbNegated or objNegated else v.lemma_, to_str(expand(sub, tokens, visited, removepunctuation))))
                            svos.append((to_str(expand(obj, tokens, visited, removepunctuation)),
                                         "!" + v2.lemma_ if verbNegated or objNegated else v2.lemma_, to_str(expand(sub, tokens, visited, removepunctuation))))
                        else:
                            svos.append((to_str(expand(sub, tokens, visited, removepunctuation)),
                                         "!" + v.lower_ if verbNegated or objNegated else v.lower_, to_str(expand(obj, tokens, visited, removepunctuation))))
                            svos.append((to_str(expand(sub, tokens, visited, removepunctuation)),
                                         "!" + v2.lower_ if verbNegated or objNegated else v2.lower_, to_str(expand(obj, tokens, visited, removepunctuation))))
            else:
                v, objs = _get_all_objs(v, is_pas)
                for sub in subs:
                    if len(objs) > 0:
                        for obj in objs:
                            objNegated = _is_negated(obj)
                            if is_pas:  
                                svos.append((to_str(expand(obj, tokens, visited, removepunctuation)),
                                             "!" + v.lemma_ if verbNegated or objNegated else v.lemma_, to_str(expand(sub, tokens, visited, removepunctuation))))
                            else:
                                svos.append((to_str(expand(sub, tokens, visited, removepunctuation)),
                                             "!" + v.lower_ if verbNegated or objNegated else v.lower_, to_str(expand(obj, tokens, visited, removepunctuation))))
                        svos.append((to_str(expand(sub, tokens, visited, removepunctuation)),
                                     "!" + v.lower_ if verbNegated else v.lower_, ''))

    return svos

if __name__ == "__main__":
    main()