all = [];



def zozMbdr (pre, opt, config) :
    for y in opt:
        new = pre.copy ()
        new.append (y)
        if (((len (new) == 3 and 7 not in new) == False) and (1 in new)):
            extend (new.copy (), config)
            zozMbdr (new.copy (), [x for x in opt if x != y], config)

def extend (base, config):
    all.append (base.copy ())
    for i in range (1, len(base) + 1):
        ext = base.copy ()
        for j in range (0, i):
            x = len (ext) - j * 2 - 1
            ext.insert (x, config [ext[x]])
    all.append (ext)

def selectSort (list):
    for i in range (0, len (list) - 1):
        min = i
        for j in range (i + 1, len (list) - 1):
            if len (list[j]) < len(list[min]):
                min = j
        swap (list, i, min)

def swap (list, a, b):
    c = list [a]
    list [a] = list [b]
    list [b] = c
    return list

a = [0.5, 2]
b = [2, 2.5, 4]
c = [4.5, 5.5]
d = [6]

for xA in range (0, len (a)):
    for xB in range (0, len (b)):
        for xC in range (0, len(c)):
            for xD in range (0, len (d)):
                _a = a [xA]
                _b = b [xB]
                _c = c [xC]
                _d = d [xD]
                config = {1: _a, 3: _b, 5: _c, 7: _d}
                all.append ("############")
                zozMbdr ([], [1, 3, 5, 7], config)


for i in range (0, len(all)):
    print (all[i])



    

