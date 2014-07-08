import re
import os
import csv
import pandas as pd
import numpy as np
from datetime import date
from dateutil import parser
import dateutil


#Read in CSV file as dataframe
os.chdir(r"C:\Users\nancyb\Documents\Documents\Research\ED US\Current")
#ed_us=pd.read_csv('ed_all.csv', parse_dates=True)
ed_us=pd.read_csv('ed_all.csv', parse_dates=[1], infer_datetime_format=True)

ed_us['EDUS']=ed_us['code'].apply(lambda x: 1 if x=="UEDLMT" else 0)
ed_us.EDUS.value_counts()
ed_only=ed_us[ed_us['EDUS']==1]
rad_only=ed_us[ed_us['EDUS']==0]



#Define matching patterns for diagnosis
dvt_pattern = re.compile(r'dvt|extremity|rue|rle|lle|rle|calf|leg|arm|clot|picc|thrombosis|lij|rij', re.IGNORECASE)
abd_pattern = re.compile(r'abd|ruq|bili|transaminitis|lipase|lft|liver|spleen|pancreatitis|gallbladder|gallstone|gb|jaund|chole|hepat|esld|abdominal|ascites|epigast|cirrhosis|hcc|hcv', re.IGNORECASE)
test_pattern = re.compile(r'testic|scrot|varicocele|epididym|genital', re.IGNORECASE)
renal_pattern = re.compile(r'renal|flank|void|bladder|hydro|urin|hematuria|cva|kidney|nephric|nephro|pvr|aki|arf|ckd|nephro|obstruction|uti|creatinine|stone|pubic|pyelo|elevated cr|rising cr', re.IGNORECASE)
preg_pattern = re.compile(r'preg|ectopic|hcg|trimester|placenta|iup|yolk|1st|2nd', re.IGNORECASE)
pelvic_pattern = re.compile(r'ovar|torsion|vaginal|pelvic|adnex|iud|gyn|orrhagia', re.IGNORECASE)

fast_pattern = re.compile(r'trauma|fast', re.IGNORECASE)
aorta_pattern = re.compile(r'aaa|aorta|aortic|aneurysm|dissection|pulsatile', re.IGNORECASE)
cardiac_pattern = re.compile(r'tamponade|cardiac|pericardial|heart|bradycardia|tachycardia|chest pain|cp|disection', re.IGNORECASE)
abscess_pattern = re.compile(r'abscess', re.IGNORECASE)
appy_pattern = re.compile(r'appendicitis|appendix|rlq|appy', re.IGNORECASE)
limited_pattern = re.compile(r'LIMITED', re.IGNORECASE)
		
def diagnosis(text):
    if re.search(test_pattern, text):
        return 'test'
    if re.search(preg_pattern, text):
        return 'preg'
    if re.search(pelvic_pattern, text):
        return 'pelvic'             
    if re.search(renal_pattern, text):
        return 'renal'
    if re.search(abd_pattern, text)
        return 'abd'
    if re.search(dvt_pattern, text)
        return 'dvt'
    if re.search(appy_pattern, text)
        return 'appy'
    if re.search(aorta_pattern, text):
        return 'aorta'
    if re.search(abcess_pattern, text)
        return 'abcess'
    if re.search(cardiac_pattern, text)
        return 'cardiac'
    if re.search(fast_pattern, text)
        return 'fast'
    if re.search(limited_pattern, text)
        return 'limited'
    return 'none'
    
rad_only['diagnosis']=rad_only['diag'].apply(diagnosis)
rad_only.diagnosis.value_counts()

ed_only['diagnosis']=ed_only['diag'].apply(diagnosis)
ed_only.diagnosis.value_counts()


ed_missing=ed_only[ed_only['diagnosis']=='none']
ed_missing.diag.ix[0:100]
rad_missing=rad_only[rad_only['diagnosis']=='none']

def missing (text):
    if text=="none"
   
    
#rad_only['diagnosis']=rad_only['diag'].apply(dvt_diagnosis)
#rad_only['diagnosis']=rad_only['diag'].apply(abd_diagnosis)	
#rad_only['diagnosis']=rad_only[rad_only['diag'].str.contains('dvt')]
