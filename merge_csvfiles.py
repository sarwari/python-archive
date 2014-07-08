#!/usr/bin/python
import csv
import itertools
import os

def csvtodictlist(sourcefile, destlist=None):
    """  Turn a sourcefile into a list of dicts.
         Assume that the input file is a comma separated csv.
         Optionally pass in a destination list to append file to

         Returns a list of dicts
    """
    #
    if destlist = None:
        destlist = []
    for line in sourcefile:
        a = open(line, 'r')
        #write the csv to a list for processing 
        destlist.extend(list(csv.DictReader(a, delimiter=',')))
        a.close()

def printcsvfiles(list_of_files, newfilename = ''):
    outputlist = []
    for line in list_of_files:
        a = open(line, 'r')
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
