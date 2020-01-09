import re
import requests
import dill
from bs4 import BeautifulSoup
from datetime import datetime as dt
import time
import spacy
import numpy as np

######################################33

# all_pages = dill.load(open('link_soups.pkd', 'rb'))
#
# wbsite = all_pages[1]
# soup = BeautifulSoup(wbsite.text, 'lxml')
# #print(soup.prettify())

############################

wbsite  = 'https://web.archive.org/web/20151114014941/http://www.newyorksocialdiary.com/party-pictures/2015/celebrating-the-neighborhood'

def soupify(wbpage):
    page = requests.get(wbpage)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup

soup = soupify(wbsite)

##########################################



#This function is called getlinks. But it gets captions.
def getlinks():
    link_divs = soup.select('div.photocaption') # For graph 2 question

    ti = int(len(link_divs)) # total items
    print('total items:', ti, '\n')
    cmp = list(range(0, ti)) #compiled list
    #cml = list(range(0,ti)) # completed links
    #print(link_divs)
    reg_str = '<div.*>(.*)<\/div>'
    print("Following is automatically generated list from captions:\n")
    for i in range(0, ti):
        cmp[i] = re.findall(reg_str, str(link_divs[i]))
        #regular expressions library takes only strings, so converted list object to string.
        #cml[i] = 'https://web.archive.org{}'.format(cmp[i][0])
        print(cmp[i])

    return ti, cmp

ti, cmp = getlinks()
print('\nProcessing Round 1\n')

nms = {} #names list

for i in range(ti):
    if not cmp[i]: #added this as otherwise indexing would choke on an empty list item
        print('cmp[',i,'] is an empty array')
    elif len(cmp[i][0]) > 250:
        print('Greater than 250 characters. skipping it')
    else:
        reg_str = '^\s'
        cmp[i][0] = re.sub(reg_str, '', cmp[i][0])

        reg_str = '\s$'
        cmp[i][0] = re.sub(reg_str, '', cmp[i][0])

        if ' at ' in cmp[i][0]:
            reg_str = '\sat\s.*'
            cmp[i][0] = re.sub(reg_str, '', cmp[i][0])

        if '(' in cmp[i][0]:
            print('Removed a parenthesis from ', i)
            reg_str = '\(.*\)'
            cmp[i][0] = re.sub(reg_str, '', cmp[i][0])

        if 'and friend' in cmp[i][0]:
            print("Removing 'and friend(s)' from this item:", i)
            reg_str = '\sand\sfriends*'
            cmp[i][0] = re.sub(reg_str, '', cmp[i][0])


print('\nThis is the list after spaces and other things are removed:\n')
for i in range(ti):
    print(i, cmp[i])

print('\nSplitting names into separate items:\n')

for i in range(0,ti): # putting each name into its own list
    print(i)
    nms[i] = {}
    if not cmp[i]: #added this as otherwise indexing would choke on an empty list item
        print('cmp[',i,'] is an empty array')
    elif len(cmp[i][0]) > 250:
        print('Greater than 250 characters. skipping it')
    elif not(',' in cmp[i][0]):
        reg_str = '^([^\s]+)\s+and\s+([^\s]+)\s+([^\s]+)$' # separating 'first and first last' name format
        if not(' and ' in cmp[i][0]): # means just a single name in this caption
            nms[i][0] = (cmp[i][0])
        elif re.search(reg_str, cmp[i][0]):
            rout = re.findall(reg_str, cmp[i][0])
            nms[i] = {}
            nms[i][0] = rout[0][0] + ' ' + rout[0][2]
            nms[i][1] = rout[0][1] + ' ' + rout[0][2]
            print('Split this first and first last name for', i)
        else:
            ln1, ln2 = cmp[i][0].split(' and ') #list of names 1 and 2
            nms[i] = {}
            nms[i][0] = ln1
            nms[i][1] = ln2
            print('Split these two names caption for', i)
    else:
        ln = cmp[i][0].split(', ') # list of names assuming separated by comma
        for j in range(0,len(ln)):
            if 'and ' in ln[j]:
                ln[j] = re.sub('and\s', '', ln[j])
            nms[i][j] = ln[j]
            print(nms[i][j])
        print('Splitting these comma separated names for', i)

print(nms)

print('\nCleaning up the list. Dangerous, be careful:\n')
print('nms list before cleaning round 2:\n', nms)

# nmi is nms item
def clean_things(nmi):

    #nmi2 = []

    if 'and ' in nmi:
        print("Removing 'and' from from of this item:", nmi)
        reg_str = '^and\s'
        nmi = re.sub(reg_str, '', nmi)

    if 'with ' in nmi:
        print("Removing 'with' from from of this item:", i, nmi)
        reg_str = ' with '
        nmi = nmi.split(reg_str)

    if 'Dr. ' in nmi:
        print("Removing 'Dr. ' from this item", nmi)
        reg_str = '^Dr\.\s'
        nmi = re.sub(reg_str, '', nmi)

    if 'Mr. ' in nmi:
        print("Removing 'Mr. ' from this item:", nmi)
        reg_str = '^Mr\.\s'
        nmi = re.sub(reg_str, '', nmi)

    if 'Mrs. ' in nmi:
        print("Removing 'Mrs. ' from this item:", nmi)
        reg_str = '^Mrs\.\s'
        nmi = re.sub(reg_str, '', nmi)

    if 'Esq.' in nmi:
        print("Removing 'Esq. ' from this item:", nmi)
        reg_str = '\s*Esq\.$'
        nmi = re.sub(reg_str, '', nmi)

    if ' on ' in nmi:
        print("Removing anything after ' on ' from this item:", nmi)
        reg_str = '\son\s.*$'
        nmi = re.sub(reg_str, '', nmi)

    if 'Mr.' in nmi or 'Mrs.' in nmi: #order matters, after the other Mrs. one
        print("Deleting this entry:", i,',',nmi)
        #del nmi
        nmi = {}

    return nmi


nml = len(nms)
for i in range(nml):
    nmk = len(nms[i])
    for j in range(nmk):
        nmt = clean_things(nms[i][j]) # nm_temp
        print(nmt)
        if len(nmt) == 2:
            nmk = len(nms[i])
            nms[i][nmk] = nmt[1]
            nms[i][j] = nmt[0]
        elif len(nmt) == 1:
            nms[i][j] = nmt[0]
        elif len(nmt) == 0:
            del nms[i][j]


print('\nAfter the looping change:')

for i,j in nms.items():
    print(i, j)

#cleaning
for l,i in nms.items():
    k = 0
    new_dict = {}
    for j in i:
        new_dict[k] = i[j]
        k += 1
    nms[l] = new_dict
#
print('\n\n\nWith cleaning stuff:')
for i,j in nms.items():
    print(i, j)

nml = len(nms)
for i in range(nml):
    nmk = len(nms[i])
    for j in range(nmk):
        nmt = clean_things(nms[i][j]) # nm_temp
        print(nmt)
        if len(nmt) == 2:
            nmk = len(nms[i])
            nms[i][nmk] = nmt[1]
            nms[i][j] = nmt[0]
        elif len(nmt) == 1:
            nms[i][j] = nmt[0]
        elif len(nmt) == 0:
            del nms[i][j]

#cleaning
for l,i in nms.items():
    k = 0
    new_dict = {}
    for j in i:
        new_dict[k] = i[j]
        k += 1
    nms[l] = new_dict


print('\nAfter re-indexing change:', nms)


nlp = spacy.load('en_core_web_sm')

def sp_nlp(nmi):
    doc = nlp(nmi)
    in_tok_n = [] #token is noun
    tok_n = np.array(in_tok_n)
    j = 0
    deli = 0
    for token in doc:
        if token.pos_ == 'PROPN':
            tok_n = np.append(tok_n, 1)
        else:
            #tok_n[j] = 0
            tok_n = np.append(tok_n, 0)
        j = j+1

    if np.mean(tok_n) < 0.5:
        print('\n', token.text, '\n', token.pos_, '\n', nmi)
        deli = 1 #delete_item
    return deli

del_ar = []

for m,i in nms.items():
    for j,k in i.items():
        deli = sp_nlp(k)
        if deli == 1:
            del_ar.append([m,j])


print(del_ar)
for i in del_ar:
    del nms[i[0]][i[1]]
    #print(i[0])

print('\nnms list after NLP:\n')
for i,j in nms.items():
    print(j)
#print('\nnms list after NLP:', nms, '\n')
print('nms list length after NLP:', len(nms), '\n')


#cleaning
for l,i in nms.items():
    k = 0
    new_dict = {}
    for j in i:
        new_dict[k] = i[j]
        k += 1
    nms[l] = new_dict



#dill.dump(nms, open('nms1_list.pkd', 'wb'))
# #dill.dump(nm_out2, open('p1_name_list.pkd', 'wb'))