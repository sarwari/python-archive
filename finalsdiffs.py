import csv
import itertools
import sys


a = open('danfinal.csv', 'rB')
b = open('final_diffs.csv', 'rB')
danfinal = list(csv.reader(a))
sunilfinal = list(csv.reader(b))
a.close()
b.close()

del danfinal[0]
del sunilfinal[0]

danfinal = sorted(danfinal)
sunilfinal = sorted(sunilfinal)

danfinal = list(danfinal for danfinal,_ in\
 itertools.groupby(danfinal))

for index, line in enumerate(danfinal):
    if line[0] != sunilfinal[index][0] or line[1] != sunilfinal[index][1]:
        print index, line
        print sunilfinal[index]
        break

