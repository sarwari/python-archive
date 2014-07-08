#!/usr/bin/python
import csv
import re
import pprint
import itertools
import sys
from datetime import date
from dateutil import parser
import os
from copy import deepcopy

output_files = False
### Instructions
#-Drop if proc contains "BIOPSY"
proc_exclude = re.compile(r'BIOPSY', re.IGNORECASE)
#-Drop if diag contains criteria below
#-Note:  there are records that say evaluate or rule out aortic dissection
diag_exclude_aneurysm = re.compile(r'aorta|aortic|dissection|disection|desection|aneurysm|anuersym'
                          , re.IGNORECASE)
diag_exclude = re.compile(r'chest\stube|AAA|TAA|triple A|T.A.A|\bTEVAR\b|\bEVAR\b|type b'
                          , re.IGNORECASE)

##Exclusion
#-Parse Impression out of report and put in separate column
impression_string = re.compile('IMPRESSION.*',re.DOTALL|re.IGNORECASE)
#Exam: remove if "Impression: This is a non-reportable study."
exam_exclude = re.compile(r'non-reportable', re.IGNORECASE)
#If impression contains:
#"aorta" "aortic" "ectatic" "ectasia" created a column #"aorta" and place a 1 in the column, otherwise 0

imp_exclude = re.compile(r'aorta|(?<!abdominal) aortic (?!valve|dissection|stenosis)|\bectatic|\bectasia',re.IGNORECASE)
imp_exclude2 = re.compile(r'aortic dissection|aortic disection', re.IGNORECASE)
#Get user input for debugging purposes
test_mrn = raw_input("Type an MRN for debugging or press enter for all records\n")

#Get all of the source files, assume that they are in subdir source
sourcefiles = sorted(os.listdir('source'))
os.chdir('source')
aortaread = []
for line in sourcefiles:
    a = open(line, 'r')
    #write the csv to a list for processing 
    aortaread.extend(list(csv.DictReader(a, delimiter=',')))
    a.close()

#put us back to the original directory and make a copy of the list
os.chdir('..')
#debugging
if test_mrn != '':
    aortaread = [line for line in aortaread if line['mrn'] == test_mrn]
#intentionally using shallow copy to keep original rows but get key updates to certain rows
original_list = aortaread[:]
full_list = deepcopy(original_list)

##Used for additional sourcefiles.  commented out (could use exception handling in the future)
#sourcefiles = sorted(os.listdir('source_add'))
#os.chdir('source_add')
#
#for line in sourcefiles:
#    a = open(line, 'r')
#    #write the csv to a list for processing 
#    full_list.extend(list(csv.DictReader(a, delimiter=',')))
#    a.close()
#
#os.chdir('..')


#read in manual list of aorta = 0
manual_aorta_zero = []

try:
    a = open('aorta_0.csv', 'r')
except IOError:
    print "Note: no manual aorta file exists"
else:
    b = csv.reader(a)
    for item in b:
        manual_aorta_zero.extend(item)
    a.close()
    manual_aorta_zero.sort()

#read in manual list of descending = 1
descending_one = []
try :
    a = open('descending_1.csv', 'r')
except IOError:
    print "Note: no descending aorta file exists"
else:
    b = csv.reader(a)
    for item in b:
        descending_one.extend(item)
    a.close()
    descending_one.sort()


#format full_list columns, including drops
for line in full_list:
#truncate age string and turn this into a 2-digit int.  Note: assumes 2-digit ages 
    temp_age = line['age']
    line['age'] = int(temp_age[:2])
#remove the time from the date string
    temp_date = line['date']
    date_array = temp_date.split(' ')
    line['date'] = date_array[0]
#create a new impression key
    impression_match = re.search(impression_string, line['report'])
    impression_result = ''
    if impression_match:
       impression_result = str(impression_match.group())
    line.update({'impression':impression_result})

# put a 1 in the column if the aorta string matches 
    aorta_match = re.search(imp_exclude, impression_result)
    aorta_code = 0
    if aorta_match:
       aorta_code = 1  
    line.update({'aorta':aorta_code})
## 3/22 removed - after the initial evaluation, if aortic dissection appears anywhere, put this at 0    
#    aorta_dissection_match = re.search(imp_exclude2, impression_result)
#    if aorta_dissection_match:
#        line.update({'aorta': 0})     

#if the aorta field is 1, run this test to see if we manually excluded it and code
#whether or not this occurred in the descending aorta (done manually as well)    
    if line['aorta'] == 1:
        if line['acc'] in manual_aorta_zero:
            line.update({'aorta': 0})
	if line['acc'] in descending_one:
            line.update({'descending': 1})  
        else:
            line.update({'descending': 0})                    
        
#remove unused keys
    line.pop('attending', None)
    line.pop('completeddate', None)
    line.pop('facility', None)
    line.pop('mod', None)
    line.pop('ordered', None)
    line.pop('part', None)
    line.pop('patientclass', None)
    line.pop('ref', None)
    line.pop('res', None)
    line.pop('scheduled', None)
    line.pop('starteddate', None)
    line.pop('stat', None)
    line.pop('sub', None)
    line.pop('type', None)
    line.pop('\xef\xbb\xbftype', None)


#exclude records from aortaread in place
#first, test inclusions and exclusions
aortaread = deepcopy(full_list)
aortaread[:] = [line for line in aortaread if (line['age'] >= 55 and line['age'] <= 80)]
exclude_proc_array = [line for line in aortaread if bool(re.search(proc_exclude, line['proc']))]
exclude_diag_array = [line for line in aortaread if bool(re.search(diag_exclude, line['diag']))]
exclude_exam_array = [line for line in aortaread if bool(re.search(exam_exclude, line['report']))]
exclude_aneurysm_array = [line for line in aortaread if (bool(re.search(diag_exclude_aneurysm, line['diag'])) and line['location'] != 'L1B L1B' )]

# now, do the exclusions (not efficient, but easier to follow with counts)
#hardcoded list of manual account numbers to exclude
manual_excl_acc = ['7670057', '8174641', '8693901']
aortaread[:] = [line for line in aortaread if not bool(re.search(proc_exclude, line['proc']))]
aortaread[:] = [line for line in aortaread if not bool(re.search(diag_exclude, line['diag']))]
aortaread[:] = [line for line in aortaread if not bool(re.search(exam_exclude, line['report']))]
aortaread[:] = [line for line in aortaread if line['acc'] not in manual_excl_acc]
aortaread[:] = [line for line in aortaread if not (bool(re.search(diag_exclude_aneurysm, line['diag'])) and line['location'] != 'L1B L1B') ]
non_excluded_studies = len(aortaread)
aorta_array = [line for line in aortaread if line['aorta'] == 1 ]
aorta_acc = sorted( [line['acc'] for line in aorta_array] )
aorta_mrn = sorted( [line['mrn'] for line in aorta_array] )
final_out = [line for line in full_list if line['mrn'] in aorta_mrn ]



# find all of the patients with multiple studies in the final_out list
studies_counts = {}
for line in final_out:
    medrecnbr = line.get('mrn')
    counter = studies_counts.get(medrecnbr, 0)
    counter = counter + 1
    studies_counts[medrecnbr] = counter

mult_studies_list = []
for line in studies_counts.keys():
    if studies_counts[line] > 1:
        mult_studies_list.append(line)

final_out_mult = sorted([line for line in final_out if line['mrn'] in mult_studies_list])
##Status
#original_list => contains the full file as initially read in
#aortaread => contains all studies that were not excluded due to criteria
#aorta_array => contains all studies that contain aorta keywords in the impressions
#aorta_mrn => contains a sorted list of MRN from the aorta_array
#final_out => contains a record for all studies in the original list related to an mrn with any
#             study of aorta of '1'  
#mult_studies => contains all of the mrns from final_out with counts of how many studies they have 

# Find the total number of unique mrn in the non-excluded studies
# denominator = unique patients in non-excluded list
# numerator = unique patients in in non-excluded list with aorta = 1

#first, get a list of mrns and sort them (important to sort first before trying to dedup)
#deduplicate through groupby and sort again (potentially redundant to sort again)
aortaread_mrn = sorted([line['mrn'] for line in aortaread])
aread_mrn_unique = sorted(list(aortaread_mrn for aortaread_mrn,_ in itertools.groupby(aortaread_mrn)))
unique_patient_count = float(len(aread_mrn_unique))

aarray_mrn = sorted([line['mrn'] for line in aorta_array])
aarray_mrn_unique = sorted(list(aarray_mrn for aarray_mrn,_ in itertools.groupby(aarray_mrn)))
unique_aorta_count = float(len(aarray_mrn_unique))


#Final files for output
#1.  A percentage of patients from the non-excluded studies that had a '1' in the aorta column
#2.  Sheet containing all of the non-excluded studies
#3.  Sheet containing all of the studies (excluded and non-excluded) for the mrn numbers 
#    that had '1' in the aorta column
#----------------------------------------------

#File 1:For now, print percentages to the screen
print 'Total number of non-excluded studies: ' +str(non_excluded_studies)
print 'Total number of non-excluded patients: ' + str(unique_patient_count)
print 'Total number of non-excluded patients with aorta criteria: ' + str(unique_aorta_count)
print 'Percentage of patients meeting criteria: ', (unique_aorta_count/unique_patient_count) * 100

if output_files:
#File 2: non-excluded studies
#build a list of keynames
    keylist = []
    for key in sorted(aortaread[0].iterkeys()):
        keylist.append(key)
    keylist.append('descending')

#write list to file   
    a = open('non_excluded_file.csv' , 'w')
    b = csv.DictWriter(a, fieldnames = keylist, delimiter=',')

#write the header row (deprecated - new way in 2.7 forward)
    b.writerow(dict((fn,fn) for fn in keylist))

#write rows to the output file
    for row in aortaread:
        b.writerow(row)
    a.close()

#File 3: All studies for MRN numbers
#build a list of keynames
    keylist = []
    for key in sorted(final_out_mult[0].iterkeys()):
        keylist.append(key)
    keylist.append('descending')
#write list to file   
    a = open('all_studies_from_aorta_patients.csv' , 'w')
    b = csv.DictWriter(a, fieldnames = keylist, delimiter=',')

#write the header row (deprecated - new way in 2.7 forward)
    b.writerow(dict((fn,fn) for fn in keylist))

#write rows to the output file
    for row in final_out_mult:
        b.writerow(row)
    a.close()

