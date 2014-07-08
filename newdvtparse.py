#!/usr/bin/python
import csv
import re
import pprint
import sys

a = open('DVT.csv', 'rB')

#write the csv to a list for processing 
dvtread = list(csv.DictReader(a))

a.close()

##create strings to consolidate coding
UU = ['UDUEVU', 'UDUEVR', 'UDUEVL']
UB = ['UDUEVB']
LU = ['UDLEVU', 'UDLEVR', 'UDLEVL']
LB = ['UDLEVB']

code2 = ''
    
#build matchcodes
occlu = re.compile(r'occlu|new thrombosis|focal clot', re.IGNORECASE)
noevidence = re.compile(r'no [\w\s]*evidence', re.IGNORECASE)
negative = re.compile(r'negative', re.IGNORECASE)
positive = re.compile(r'positive|extensive|persistent|(?<!no )acute', re.IGNORECASE)
noacutedvt = re.compile(r'no acute|no dvt', re.IGNORECASE)
possible = re.compile(r'possible|partial|probable|saphenous', re.IGNORECASE)

for line in dvtread:
#search for patterns in impression field
    match_occlu = re.search(occlu, line['impression'])
    match_noevidence = re.search(noevidence, line['impression'])
    match_negative = re.search(negative, line['impression'])
    match_positive = re.search(positive, line['impression'])
    match_noacutedvt = re.search(noacutedvt, line['impression'])
    match_possible = re.search(possible, line['impression'])
        
    line['test_occlu'] = ''
    line['test_noevidence'] = ''
    line['test_negative'] = ''
    line['test_positive'] = ''
    line['test_noacutedvt'] = ''        
    line['test_possible'] = ''
#assign values to new columns
    if match_occlu:
        line['test_occlu'] = 1
    if match_noevidence:
        line['test_noevidence'] = 0
    if match_negative:
        line['test_negative'] = 0
    if match_positive:
        line['test_positive'] = 1
    if match_noacutedvt:
        line['test_noacutedvt'] = 0
    if match_possible:
        line['test_possible'] = 2

#Consolidate coding
    if line['code'] in UU:
        code2 = 'UU'
    elif line['code'] in UB:
	code2 = 'UB'
    elif line['code'] in LU:
	code2 = 'LU'
    elif line['code'] in LB:
	code2 = 'LB'
    line['code2'] = code2

#build a list of keynames
keylist = []
for key in sorted(dvtread[0].iterkeys()):
    keylist.append(key)

#write list to file   
a = open('parsedDVT.csv' , 'w')
b = csv.DictWriter(a, fieldnames = keylist, delimiter=',')

#write the header row (deprecated - new way in 2.7 forward)
b.writerow(dict((fn,fn) for fn in keylist))

#write rows to the output file
for row in dvtread:
     b.writerow(row)
a.close()



    
#if __name__ == '__main__':
#  main()
