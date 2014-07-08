#!/usr/bin/python
import csv
import itertools
from datetime import date
from dateutil import parser

def convertcsvdate(sourcelist, datefield, newdatefield):
    """  Given a list of dicts and date key, convert the 
         string date to a date object and store it in a
         new date key
        
         Return the sourcelist 
    """
    for line in sourcelist:
        dt = parser.parse(line[datefield]) 
        line.update({newdatefield:dt.date()}) 
    return sourcelist

def csvtodictlist(sourcefile, destlist=None):
    """  Turn a sourcefile into a list of dicts.
         Assume that the input file is a comma separated csv.
         Optionally pass in a destination list to append file to

         Returns a list of dicts
    """
    #
    if destlist == None:
        destlist = []   
    try:
        a = open(sourcefile, 'r')
    except IOError:
        print 'Source file not found'
    else:
        #write the csv to a list for processing 
        destlist.extend(list(csv.DictReader(a, delimiter=',')))
        a.close()
    
    return destlist

def mergecsvfiles(list_of_files, newfilename = ''):
    """  Merge a list of csv files to single output file
         If new filename is not included, no files are created
         Returns an output list of dicts created by the file.
    """   
    outputlist = []
    for line in list_of_files:
        try:
            a = open(line, 'r')
        except IOError:
            print 'Source file not found'
        else:
            #write the csv to a list for processing 
            outputlist.extend(list(csv.DictReader(a, delimiter=',')))
            a.close()
    
    if newfilename != '':
        #build a list of keynames
        keylist = []
        for key in sorted(outputlist[0].iterkeys()):
            keylist.append(key)
        #write list to file   
        a = open(newfilename , 'w')
        b = csv.DictWriter(a, fieldnames = keylist, delimiter=',')

        #write the header row (deprecated - new way in 2.7 forward)
        b.writerow(dict((fn,fn) for fn in keylist))

        #write rows to the output file
        for row in outputlist:
            b.writerow(row)
        a.close()
    
    return outputlist
