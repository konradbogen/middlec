all = [];



def zozMbdr (pre, opt, config) :
    for y in opt:
        new = pre.copy ()
        new.append (y)
        if ((len (new) == 3 and 7 not in new) == False):
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

zozMbdr ([], [1, 3, 5, 7], {1: 2, 3: 4, 5: 4.5, 7: 6})

for i in range (0, len(all)):
    print (all[i])


    

