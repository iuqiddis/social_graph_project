import matplotlib
import seaborn as sns
import re
sns.set()

import requests
import dill
from bs4 import BeautifulSoup
from datetime import datetime as dt
import time

wbsite  = 'https://web.archive.org/web/20150913224145/http://www.newyorksocialdiary.com/party-pictures'

def soupify(wbpage):
    page = requests.get(wbpage)
    soup = BeautifulSoup(page.text, 'lxml')
    return soup

soup = soupify(wbsite)
#print(soup.prettify())

def getlinks():
    link_divs = soup.select('div.views-row span.field-content a') # The a only selects the links span
    reg_str = '<a href="(.*)">'
    ti = int(len(link_divs)) # total items
    cmp = list(range(0, ti)) #compiled list
    cml = list(range(0,ti)) # completed links

    for i in range(0, ti):
        cmp[i] = re.findall(reg_str, str(link_divs[i]))
        #regular expressions library takes only strings, so converted list object to string.
        cml[i] = 'https://web.archive.org{}'.format(cmp[i][0])
        #print(cml[i])


    return cmp, cml

cmp, cml = getlinks()
print('The length of this URL list is:', len(cmp), '\n')
print('First 5  incomplete urls are:\n', cmp[-5:], '\n')
print('First 5  urls are:\n', cml[-5:], '\n')

def getdates():
    link_divs = soup.select('div.views-row span.field-content')  #Unlike links cannot exclusively select dates
    print('Total URL + dates selected:', len(link_divs))
    ti = int(len(link_divs)/2)
    link_divs2 = [i for i in range(ti)]
    for i in link_divs2:
        link_divs2[i] = link_divs[i*2+1]

    print('Length of just dates list is:', len(link_divs2))

    reg_str = '<span class="field-content">\w*,(.*)<\/span>'
    cmp= list(range(0,ti))
    cmt= list(range(0,ti))

    for i in range(0,len(link_divs2)): #needed the range function as link_divs2 is not a list
        cmp[i] = re.findall(reg_str, str(link_divs2[i]))
        cmt[i] = dt.strptime(str(cmp[i]), "[' %B %d, %Y']")


    return cmp,cmt

cmp2, cmt = getdates()
print('The length of this "date" list is:', len(cmp2), '\n')
print('First 5 dates are:\n', cmp2[-5:], '\n')
print('First 5 dates are:\n', cmt[-5:], '\n')

#This thing has 26 pages
pg = [i for i in range(0,26)]
for i in pg:
    wb2 = 'https://web.archive.org/web/20150913224145/http://www.newyorksocialdiary.com/party-pictures?page={}'.format(pg[i])
    print(wb2)
    print('page#:', i+1)
    soup = soupify(wb2)

    cmpp, cmlp = getlinks()
    cml = cml + cmlp

    cmpp2, cmtp = getdates()
    cmp2 = cmp2 + cmpp2
    cmt = cmt + cmtp

    time.sleep(1)



with open('links.txt', 'w') as f:
    for item in cml:
        f.write("%s\n" % item)

with open('dates_un.txt', 'w') as f:
    for item in cmp2:
        f.write("%s\n" % item)

with open('dates_form.txt', 'w') as f:
    for item in cmt:
        f.write("%s\n" % item)

dill.dump(cml, open('links.pkd', 'wb'))
dill.dump(cmp2, open('dates_un.pkd', 'wb'))
dill.dump(cmt, open('dates_form.pkd', 'wb'))
