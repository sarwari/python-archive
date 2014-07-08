#!/usr/bin/python
import csv
import re
import pprint
import itertools
import sys
import datetime

#used the below regex to clean the file beforehand and write it out to testa.csv
#matched = re.sub(r"\xef\xbb\xbf","", myfile)
finalheader = ['EMP_NUM', 'COURSE', 'SF_EXP_DATE', 'SAP_EXP_DATE', 'BUNDLE', 'JOB', 'RIG']

a = open('sap_formatted.csv', 'r')
b = open('sf_formatted.csv', 'r')

#write the csv to a list for processing 
##sapread: input file for SAP
##platread: input file for Plateau
sapread = list(csv.reader(a))
platread = list(csv.reader(b))

a.close()
b.close()

#delete the header records
del sapread[0]
del platread[0]

#no longer necessary - fix null dates in SAP file
for line in sapread:
    if line[2] == '':
        line[2] = '1/1/1900'

print 'Step 1: finding differences in personnel numbers', str(datetime.datetime.now())
#find personnel ids that do not match in the list
##plat_ids: all ids in Plateau
##sap_ids: all ids in SAP
plat_ids = [line[0] for line in platread]
sap_ids = [line[0] for line in sapread]
##plat_only: ids in Plateau but not in SAP
##sap_only: ids in SAP not in Plateau
plat_only = list(set(plat_ids) - set(sap_ids))
sap_only = list(set(sap_ids) - set(plat_ids))
print 'Step 1 Completed', str(datetime.datetime.now())
#append 'Plateau' or 'SAP' to the record before generating the file  
##exclude_id: all ids not shared between the SAP and Plateau
exclude_id = []
for line in plat_only:
    line += ',SF_ONLY\n'
    exclude_id.append(line)	
for line in sap_only:
    line += ',SAP_ONLY\n'
    exclude_id.append(line)


#write out a file of ID mismatches
c = open('ids_exclude.csv', 'w')
c.writelines([line for line in exclude_id])
c.close()

#create two lists that we can use for comparison (unique ids)
print 'Testprint: create two lists that we can use for comparison (unique ids)', \
str(datetime.datetime.now()) 
plateau_comp = sorted([ line for line in platread if line[0] not in plat_only ])
sap_comp = sorted([ line for line in sapread if line[0] not in sap_only ])

#create a list of person course combinations in the lists
print 'Testprint: create a list of person course combinations in the lists', str(datetime.datetime.now())
platcourse = sorted([(line[0], line[1]) for line in plateau_comp])
sapcourse = sorted([(line[0], line[1]) for line in sap_comp])

#find person/course combos that do not match in the list
print 'Testprint: find person/course combos that do not match in the list', str(datetime.datetime.now()) 
plat_only = list(set(platcourse) - set(sapcourse))
sap_only = list(set(sapcourse) - set(platcourse))

#create a list of records with person course combinations not in the lists
print 'Testprint: create a list of records with person course combinations not in the lists', str(datetime.datetime.now())
plateau_course = sorted([ line for line in plateau_comp if (line[0], line[1])\
in plat_only ])
sap_course = sorted([ line for line in sap_comp if (line[0], line[1])\
in sap_only ])

print 'Testprint: write files with person course combinations not in the lists', str(datetime.datetime.now())
d = open('course_only_in_plat.csv', 'w')
e = open('course_only_in_sap.csv', 'w')

platcoursewrite = csv.writer(d)
platcoursewrite.writerows([line for line in plateau_course])

sapcoursewrite = csv.writer(e)
sapcoursewrite.writerows([line for line in sap_course])

d.close()
e.close()

#build two lists of courses that should be the same length
print 'Testprint: build two lists of courses that should be the same length', str(datetime.datetime.now())
plateau_course = sorted([ line for line in plateau_comp if (line[0], line[1])\
not in plat_only ])
sap_course = sorted([ line for line in sap_comp if (line[0], line[1])\
not in sap_only ])

#deduplicate list of plateau courses
print 'Testprint: deduplicate list of plateau courses', str(datetime.datetime.now())
plat_course = list(plateau_course for plateau_course,_ in\
 itertools.groupby(plateau_course))

#test
print 'Testprint: re-sort final lists', str(datetime.datetime.now())
testlist = [ list((item[0], item[1], item[2])) for item in plat_course]
finalplat = sorted(list(testlist for testlist,_ in\
 itertools.groupby(testlist)))
finalsap = sorted([ list((item[0], item[1], item[2])) for item in sap_course])

if len(finalplat) != len(finalsap):
    print 'Error - mismatch in final file length', str(datetime.datetime.now())
    for index, line in enumerate(finalplat):
        if line[0] != finalsap[index][0] or line[1] != finalsap[index][1]:
            print index, line
            sys.exit(1)            




finaldiff = []
print 'Testprint: Output data differences to file', str(datetime.datetime.now())
for index, line in enumerate(finalplat):
    if line != finalsap[index]:
        finaldiff.append([line[0], line[1], line[2], sap_course[index][2], sap_course[index][3],\
 sap_course[index][4], sap_course[index][5]])

finaldiff.insert(0, finalheader)
f = open('final_diffs.csv', 'w')    
finalwrite = csv.writer(f)
finalwrite.writerows([line for line in finaldiff])
f.close()
print 'Testprint: Completed', str(datetime.datetime.now())





