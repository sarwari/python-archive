lista = [{'a':1, 'b':1, 'c':1, 'd':1 }, {'a':2, 'b':2, 'c':2, 'd':0} , {'a':3, 'b':3, 'c':3, 'd':3}]
listb = lista[:]
lista[:] = [line for line in lista if line['d'] > 0 ]
listc = [{'a':100, 'b':1, 'c':1, 'd':1 }, {'a':200, 'b':2, 'c':2, 'd':0} , {'a':300, 'b':3, 'c':3, 'd':3}]
