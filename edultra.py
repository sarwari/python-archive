#!/usr/bin/python
import csv
import itertools
import re
import pprint
from datetime import date
from dateutil import parser
from operator import itemgetter
from copy import deepcopy
import pandas as pd

#1. fields to remove
#type, stat, location, sub, facility, patientclass, profcpt, hospcpt, ordered, scheduled, starteddate, completeddate
#
#2. Coding (add columns)
# Rule: if code == 'UEDLMT' then EDUS == True, else EDUS == False
#
#3. Group by MRN, sort by date ascending
#4. If dates are <= 2 days apart, consider as same Episode of care or ED visit.
#5. Determine in the episode of care whether or not the person had an EDUS, RADUS, or BOTH
#6. Group and tabulate the episodes of care data by month.

#Define matching patterns for diagnosis
dvt_pattern = re.compile(r'dvt|extremity|\brue\b|\brle\b|\blle\b|\brle\b|calf|\bleg\b|\barm\b|\bclot|picc|thrombosis|\blij\b|\brij\b', re.IGNORECASE)
abd_pattern = re.compile(r'abd|ruq|bili|transaminitis|lipase|lft|liver|spleen|pancreatitis|gall\s*bladder|gallstone|gb|jaund|chole|hepat|esld|abdominal|ascites|epigast|cirrhosis|hcc|hcv', re.IGNORECASE)
test_pattern = re.compile(r'testic|scrot|varicocele|epididym|genital', re.IGNORECASE)
renal_pattern = re.compile(r'renal|flank|void|bladder|hydro|urin|hematuria|cva|kidney|nephric|nephro|pvr|\baki\b|\barf\b|ckd|nephro|obstruction|\buti\b|creatinine|stone|pubic|pyelo|elevated cr|rising cr', re.IGNORECASE)
preg_pattern = re.compile(r'preg|ectopic|hcg|trimester|placenta|\biup\b|yolk|1st|2nd', re.IGNORECASE)
pelvic_pattern = re.compile(r'ovar|torsion|vaginal|pelvic|adnex|\biud\b|gyn|orrhagia', re.IGNORECASE)

fast_pattern = re.compile(r'trauma|fast', re.IGNORECASE)
aorta_pattern = re.compile(r'aaa|aorta|aortic|aneurysm|dissection|pulsatile', re.IGNORECASE)
cardiac_pattern = re.compile(r'tamponade|cardiac|pericardial|heart|bradycardia|tachycardia|chest pain|cp|disection', re.IGNORECASE)
abscess_pattern = re.compile(r'abscess', re.IGNORECASE)
appy_pattern = re.compile(r'appendicitis|appendix|rlq|appy', re.IGNORECASE)
limited_pattern = re.compile(r'LIMITED', re.IGNORECASE)

rank_diagnosis = { 'test': 10, 
                   'preg': 20,
                   'pelvic': 30,
                   'appy' : 35,
                   'ruq' : 40,
                   'abd' : 50,
                   'renal' :60,
                   'dvt' :70,
                   'abscess' :80,
                   'aorta' :90,
                   'cardiac' :100,
                   'fast' :110,
                   'none' :120,
                   'limited' :130 }

def map_diagnosis(text):
    if re.search(test_pattern, text):
        return 'test'
    if re.search(preg_pattern, text):
        return 'preg'
    if re.search(pelvic_pattern, text):
        return 'pelvic'             
    if re.search(abd_pattern, text):
        return 'abd'
    if re.search(renal_pattern, text):
        return 'renal'
    if re.search(dvt_pattern, text):
        return 'dvt'
    if re.search(appy_pattern, text):
        return 'appy'
    if re.search(aorta_pattern, text):
        return 'aorta'
    if re.search(abscess_pattern, text):
        return 'abscess'
    if re.search(cardiac_pattern, text):
        return 'cardiac'
    if re.search(fast_pattern, text):
        return 'fast'
    if re.search(limited_pattern, text):
        return 'limited'
    return 'none'


output_files = False
#Get all of the source files, assume that they are in subdir source
ed_source = []
a = open('may2014_us.csv', 'r')
#write the csv to a list for processing 
ed_source = list(csv.DictReader(a, delimiter=','))
a.close()

#format full_list columns, including drops
for line in ed_source:
##truncate age string and turn this into a 2-digit int.  Note: assumes 2-digit ages 
#    temp_age = line['age']
#    line['age'] = int(temp_age[:2])
#remove the time from the date string and format
    temp_date = line['date']
    date_array = temp_date.split(' ')
    line['date'] = date_array[0]
    dt = parser.parse(line['date']) 
    line['date'] = dt.date()
#if code == 'UEDLMT' then EDUS == True, else EDUS == False    
    if line['code'] == 'UEDLMT':
        line.update({'EDUS': True})  
    else:
        line.update({'EDUS': False})

#remove unused keys
    line.pop('location', None)
    line.pop('completeddate', None)
    line.pop('facility', None)
    line.pop('hospcpt', None)
    line.pop('ordered', None)
    line.pop('patientclass', None)
    line.pop('profcpt', None)
    line.pop('scheduled', None)
    line.pop('starteddate', None)
    line.pop('stat', None)
    line.pop('sub', None)
    line.pop('type', None)
    line.pop('\xef\xbb\xbftype', None)

#Group by MRN and sort by date ascending
ed_source = sorted(ed_source, key=lambda k: (k['mrn'], k['date']))

#If dates are <= 2 days apart, consider as same Episode of care or ED visit.
#Determine in the episode of care whether or not the person had an EDUS, RADUS, or BOTH
init_date = date(1900, 1, 1)
prev_row = {'epi_num': 0, 'mrn' : 0, 'EDUS': 0, 'RADUS': 0, 'date' : init_date, 'counter' : 1 }
eoc_list = []
for line in ed_source:
    if line['mrn'] == prev_row['mrn'] and ((line['date'] - prev_row['date']).days <= 2):
        prev_row['study_count'] = prev_row['study_count'] + 1
        if line['EDUS'] == True:
            prev_row['EDUS'] = prev_row['EDUS'] + 1
            prev_row['diagnosis'].append((map_diagnosis(line['diag']), 'EDUS'))
        else:    
            prev_row['RADUS'] = prev_row['RADUS'] + 1
            prev_row['diagnosis'].append((map_diagnosis(line['diag']), 'RADUS'))
    else:          
        if prev_row['epi_num'] > 0:
            if (prev_row['EDUS'] > 0 and prev_row['RADUS'] > 0):
                prev_row['BOTH'] = True   
            eoc_list.append(deepcopy(prev_row))
        #reset variables and populate with first study of EOC
        prev_row['diagnosis'] = []
        prev_row['epi_num'] = prev_row['epi_num'] + 1
        prev_row['mrn'] = line['mrn']
        prev_row['date'] = line['date']
        prev_row['study_count'] = 1
        prev_row['BOTH'] = False    
        if line['EDUS'] == True:
            prev_row['EDUS'] = 1
            prev_row['RADUS'] = 0
            prev_row['diagnosis'].append((map_diagnosis(line['diag']), 'EDUS'))
        else:   
            prev_row['EDUS'] = 0
            prev_row['RADUS'] = 1
            prev_row['diagnosis'].append((map_diagnosis(line['diag']), 'RADUS'))


#To do: think about what to do with the last row.  Can we just blind append?        

def ranker(list_of_diags):
#return the diagnosis with the best (lowest) rank
    best_diagnosis = ''
    if len(list_of_diags) > 0:
        for diag in list_of_diags:
            if best_diagnosis == '':
                best_diagnosis = diag
            elif rank_diagnosis[diag] < rank_diagnosis[best_diagnosis]:
                best_diagnosis = diag
    return best_diagnosis

for line in eoc_list:
    #Group the dates into month-year bins
    line['date_bucket'] = str(line['date'].year) + '-' + str(line['date'].month).zfill(2)
    #Categorize the episode of care as ED only, Rad only, or Both
    if line['BOTH'] is True:
        line['category'] = 'BOTH'
    elif line['EDUS'] > 0:
        line['category'] = 'EDONLY'
    else:
        line['category'] = 'RADONLY' 
    #Determine a single diagnosis for the eoc.  Use ranker function
    #first, split the diagnosis list into lists
    ed_list = []
    rad_list = []
    for item in line['diagnosis']:
        if item[1] == 'RADUS':
            rad_list.append(item[0])
        else:
            ed_list.append(item[0])
    if line['category'] == 'EDONLY':
        line['eoc_diagnosis'] = ranker(ed_list)
    elif line['category'] == 'RADONLY':
        line['eoc_diagnosis'] = ranker(rad_list)   
    else:
    #if both, use the RADUS diagnosis if there is only one
        if len(rad_list) == 1:
            line['eoc_diagnosis'] = ranker(rad_list)
    #else, use the RADUS diagnosis that is also in the ED diagnosis
    #if there is no common diagnosis, just use the best rad diagnosis
        else:
            common_diag = set(ed_list) & set(rad_list)
            if not common_diag:
                line['eoc_diagnosis'] = ranker(rad_list)
            else:
                line['eoc_diagnosis'] = ranker(list(common_diag))
            
               
eoc_dual_studies = [line for line in eoc_list if line['BOTH']]
eoc_mult_studies =  [line for line in eoc_list if line['study_count'] > 1]


for line in eoc_mult_studies:
    diff_diag = None
    for item in line['diagnosis']:
        if diff_diag is None:
            diff_diag = 'Error'  
        elif temp_diag[0] == item[0]:
            diff_diag = False
        else:
            diff_diag = True
        temp_diag = item                  
    line['diff_diag'] = diff_diag
             
eoc_diff_studies = [ line for line in eoc_mult_studies if line['diff_diag']]

def print_diags(mrn=None):
    if mrn is None:
        temp_mrn = raw_input("Enter an MRN: ")
    else:
       temp_mrn = mrn
    for line in ed_source:
        if line['mrn'] == temp_mrn:
            print 'Date: ' + line['date'].strftime('%m/%d/%Y')
            print 'EDUS: ' + str(line['EDUS'])
            print 'Diagnosis: ' + line['diag']
            print ' '
            

    

##Replaced the basic dataframe call to use episode number as the index
##eoc_df = pd.DataFrame(eoc_list)

#eoc_df = pd.DataFrame.from_records(eoc_list, index='epi_num')
#print eoc_df.groupby(['date_bucket', 'BOTH']).count()
#print eoc_df.groupby('date_bucket').sum()
#print eoc_df.groupby(['date_bucket', 'BOTH']).sum()
    


