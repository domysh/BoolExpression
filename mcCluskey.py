'''
        Code by DomySh!
    Boolean Expression solver
    Minimising verity table 
    and a general expression
  GNU 3.0 General Public License
'''
from utils import toBits, NULL_CHAR

def getNumOne(term):
    count = 0
    for ele in term:
        if ele == '1': 
            count+=1
    return count

def getDistance(term1,term2):
    if len(term1) != len(term2): raise Exception(f"Impossible to compare this 2 terms {term1} and {term2}")
    dist = 0
    for i in range(len(term1)):
        if term1[i] != term2[i]:
            dist+=1
    #print(dist)
    return dist

def getNBitElements(terms,bitN):
    res = []
    for ele in terms:
        if getNumOne(ele) == bitN:
            res.append(ele)
    return res

def getBitSelection(minTerms,n_vars):
    bitSelection = list(range(n_vars+1))
    for i in range(n_vars+1):
        bitSelection[i] = getNBitElements(minTerms,i)
    return bitSelection

def isMatEmpty(mat):
    for ele in mat:
        if len(ele) != 0:
            return False
    return True

def replaceDiff(a,b,put):
    if len(b) != len(a): raise Exception(f"Impossible to compare this 2 terms {a} and {b}")
    res = []
    for i in range(len(a)):
        if a[i] != b[i]:
            res.append(put)
        else:
            res.append(a[i])
    return tuple(res)
        

def compareComb(a,b,vet,finded):
    if getDistance(a,b) == 1:
        vet.append(replaceDiff(a,b,NULL_CHAR))
        return True
    return False


def compareSelection(selection, finded):
    newSelection = list(range(len(selection)-1))
    selected = []
    for i in newSelection:
        newSelection[i] = []
        for indA in range(len(selection[i])):
            for indB in range(len(selection[i+1])):
                #print(f"selection[{i}][{indA}]:{selection[i][indA]}")
                #print(f"selection[{i+1}][{indB}]:{selection[i+1][indB]}")
                if compareComb(selection[i][indA],selection[i+1][indB],newSelection[i],finded):
                    selected.append(selection[i][indA])
                    selected.append(selection[i+1][indB])
    #print(selected)
    for ele1 in selection:
        for ele2 in ele1:
            if ele2 not in selected:
                finded.append(ele2)
    return newSelection

def getAdiacense(selection,finded=[]):
    #print(f"Selection:{selection}")
    #print(f"Finded:{finded}")
    #res = None
    if isMatEmpty(selection):
        return finded
    else:
        sel = compareSelection(selection,finded)
        return getAdiacense(sel,finded)

def getTerms(minTerms,n_var):
    return getAdiacense(getBitSelection(minTerms,n_var))