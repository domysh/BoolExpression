'''
        Code by DomySh!
    Boolean Expression solver
    Minimising verity table 
    and a general expression
  GNU 3.0 General Public License

Example of the structure that have to have an expression
[
    [ ["k"] , ["l"] ] , [ ["k"] , ["m"] ],
    [ ["l"] , ["n"] ] , [ ["m"] , ["p"] ],
    [ ["n"] , ["q"] ] , [ ["p"] , ["q"] ]
]
'''
from utils import toBits,NULL_CHAR

def noCp(ob):
    return tuple(set(ob))

def everyIn(op1,op2):
    for ele in op1:
        if ele not in op2:
            return False
    return True

def singInBig(ex):
    for i in range(len(ex)):
        for j in range(len(ex)):
            if i != j and everyIn(ex[i],ex[j]):
                ex = list(ex)
                #print("delete ->",ex[j])
                del ex[j]
                return singInBig(tuple(ex))
    #print("Result Semplify",ex)
    return ex

def mul2Expr(ex1,ex2):
    res = []
    #print("Multiply Op1",ex1,"Op2",ex2)
    for ele1 in ex1:
        for ele2 in ex2:
            res.append(noCp(tuple(ele1)+tuple(ele2)))
    #print("Multiply Res ->",res)
    return singInBig(res)

def isList(a):
    return type(a[0]) == tuple or type(a[0]) == list

def getMul(exp):
    if len(exp) == 1:return exp.pop()
    while len(exp)>1:
        exp.append(mul2Expr(exp.pop(),exp.pop()))
    #while :
    #    exp = exp[0]
    #print(exp)
    return noCp(exp.pop())

def getMinEx(exp):
    res = []
    dims = []
    for ele in exp:
        dims.append(len(ele))
    minLen = min(dims)
    for i in range(len(exp)):
        if dims[i] == minLen:
            res.append(exp[i])
    return res

def petrickMethod(op):
    return getMinEx(getMul(op))

#Interfacing with other files

def toCharBits(term,n_var):
    res = list(toBits(term,n_var))
    for i in range(len(res)):
        if res[i]: res[i] = '1'
        else: res[i] = '0'
    return tuple(res)

def toBitsMinTerm(minTerms,n_var):
    return [toCharBits(term,n_var) for term in minTerms]

def getAnalyseMat(minTerms,results):
    mat = [] 
    for x in range(len(results)):
        mat.append([])
        for y in range(len(minTerms)):
            mat[x].append(equalsIngoreNull(minTerms[y],results[x]))
    return mat
    
def equalsIngoreNull(a,b):
    if len(b) != len(a): raise Exception(f"Impossible to compare this 2 terms len(a):{len(a)} and len(a):{len(b)}")
    for i in range(len(a)):
        if a[i]!=NULL_CHAR and b[i]!=NULL_CHAR:
            if a[i] != b[i]:
                return False
    return True

def getPatrickExpression(minTerms,results):
    anly = getAnalyseMat(minTerms,results)
    #printM(anly)
    res = []
    for i in range(len(anly[0])):
        s = []
        for j in range(len(anly)):
            if anly[j][i]:
                s.append([results[j]])
        res.append(s)
    #print(res)
    return res
'''
def printM(m):
    for ele in m:
        print(ele)
'''

