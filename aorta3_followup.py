#!/usr/bin/python
from collections import Counter


def output_records(list_of_dicts, filename):
#build a list of keynames
    keylist = []
    for key in sorted(list_of_dicts[0].iterkeys()):
        keylist.append(key)
#write list to file   k
    a = open(filename , 'w')
    b = csv.DictWriter(a, fieldnames = keylist, delimiter=',')

#write the header row (deprecated - new way in 2.7 forward)
    b.writerow(dict((fn,fn) for fn in keylist))

#write rows to the output file
    for row in list_of_dicts:
        b.writerow(row)
    a.close()


#Open aorta file, read in acc #, and strip the newlines off the end 
a = open('aorta_one.csv', 'r')
accessions = a.readlines()
a.close()
accessions[:] = [ line[0:-1] for line in accessions]
new_mrn = [ line['mrn'] for line in original_list if line['acc'] in accessions]
new_mrn[:] = sorted(new_mrn)
new_mrn_unique = sorted(list(new_mrn for new_mrn,_ in itertools.groupby(new_mrn)))

aorta_one = [line for line in original_list if line['mrn'] in new_mrn_unique]

#format full_list columns, including drops
for line in aorta_one:
#truncate age string and turn this into a 2-digit int.  Note: assumes 2-digit ages 
    temp_age = line['age']
    if type(temp_age) == str:
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
    aorta_code = 0
    if line['acc'] in accessions:
       aorta_code = 1  
    line.update({'aorta':aorta_code})
     
        
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

output_records(aorta_one, 'all_priors_aorta_one.csv')

for line in aorta_one:
#create a date object field
    dt = parser.parse(line['date']) 
    line.update({'date_object':dt.date()}) 

#tally all of the times an mrn appears in the list
c = Counter(line['mrn'] for line in aorta_one)
new_mult_studies = [key for key in c.keys() if c[key] > 1]
#make a list containing only the studies for patients with more than one study
aorta_one_mult = [line for line in aorta_one if line['mrn'] in new_mult_studies]

measure_group = []
for mrn in new_mult_studies:
    exam_dates = [line['date_object'] for line in aorta_one_mult if line['mrn'] == mrn]
    min_date = min(exam_dates)
    max_date = max(exam_dates)
    date_diff = max_date - min_date
    if date_diff.days >= 180:
        measure_group.append(mrn)


#format output for file
for line in aorta_one_mult:
   line.pop('date_object', None)

aorta_measure_group = [line for line in aorta_one_mult if line['mrn'] in measure_group]
output_records(aorta_measure_group, 'measure_group_all_studies.csv')



