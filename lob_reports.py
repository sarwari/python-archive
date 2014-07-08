#!/usr/bin/python
import re
import os
from copy import deepcopy
from datetime import date
import sunil_csv

output_files = False
today = date.today()
#Get all of the source files, assume that they are in subdir reporting
sourcefilelist = sorted(os.listdir('reporting'))
sourcedir = os.path.abspath('reporting')
sourcefiles = [(os.path.join(sourcedir,line), line[:-4].lower()) for line in\
                sourcefilelist if line[-3:] == 'txt']
localvars = [line[1] for line in sourcefiles]
#Dynamically create lists of dicts with names the same as their filename
for line in sourcefiles:
    resultlist = sunil_csv.csvtodictlist(line[0])
    exec("%s=deepcopy(resultlist)" % line[1]) 



sunil_csv.convertcsvdate(aa_rateschedule_project,'ProjectRoleEndDate', 'EndDate')


