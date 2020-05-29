'''
        Code by DomySh!
    Boolean Expression solver
    Minimising verity table 
    and a general expression
'''
from TerminalMenu import MenuCreate

ANDSYM = '*' #or space (To add with a function)
ORSYM = '+'
OPER = [ANDSYM,ORSYM]
NOTSYM = '!'
OPEN_BRA = ['(', '[', '{']
CLOSE_BRA = [')', ']', '}']
BRACKETS = OPEN_BRA+CLOSE_BRA
NULL_CHAR = '-' # have to be different from 0 and 1

#Pause Function
def pause():input("Press Enter...")

#Error Function
def throwError(s):
    import sys
    print(f"\nERRORE INDIVIDUATO!\n{s}")
    pause()
    sys.exit()

def toBits(num,lenght):
    bitTester = 2**(lenght-1)
    val = []
    for _ in range(lenght):
        val.append(bool(int(int(num) & int(bitTester)) !=0))
        bitTester /= 2
    return tuple(val)
    
#Gen a combination of bits to assign at all variables
def getCombination(idComb,n_sym):
    return toBits(idComb,n_sym)


'''
This function separate special sym to alpha
in a array without counting spaces
but separate also brackets as special char
'''
def exprToArray(expr):
    lastAlNum = False
    mustChange = False
    putBraket = ''
    vetExp = []
    item = ''
    for ele in expr:
        thisAlNum = ele.isalnum()
        #print(f"NOW:{thisAlNum} | LAST:{lastAlNum} | CHANGE:{mustChange}")
        #print(f"ITEM:{item} | BRACK:{putBraket}")
        #Decido cosa fare per l'elemento precedente in base alla situazione
        if thisAlNum != lastAlNum or mustChange:
            mustChange = False
            if item != '':
                vetExp.append(item)
                item = ''
                #if ele != ' ': item = ele
            if putBraket != '':
                vetExp.append(putBraket)
                putBraket = ''
                #mustChange = True
        
        #In base al carattere in arrivo do indicazioni diverse
        if ele == ' ':
            mustChange = True
        elif ele in BRACKETS:
            mustChange = True
            putBraket = ele
        else:
            item+=ele

        lastAlNum = thisAlNum

    if putBraket != '':
        vetExp.append(putBraket)
    if item != '':
        vetExp.append(item)


    return vetExp

#add beetween spaces AND implicated operation
def showHiddenAnd(expr):
    complete_expression = []
    lastele = ''
    for ele in expr:
        if ele.isalnum() or ele in BRACKETS or ele == NOTSYM:
            if lastele.isalnum() or lastele in BRACKETS:
                if lastele not in OPEN_BRA and ele not in CLOSE_BRA: 
                    complete_expression.append(ANDSYM)
        lastele = ele
        complete_expression.append(ele)
    return complete_expression

#return the array with all operation reparated
def makeArray(expression):
    ex = exprToArray(expression)
    #print(ex)
    return showHiddenAnd(ex)

def symTable(expr):
    sym = []
    for i in expr:
        if i.isalnum() and i not in sym:
            sym.append(i)
    sym.sort()
    sym = tuple(sym)
    return sym

'''
Creation of a Dictionary of operation to do:
Structure:

{
    "1":{
        "1": {"1":a, "op":"!"},
        "2": "b",
        "o": "*",
    },

    "2": "c",
    "o": +,
}
'''
#return true if the element return a value
def isVar(ele):#a b + (c b { a b + c) !d) * !a
    #print(ele)
    if type(ele) != dict:
        return ele.isalnum()
    return True 

#get the end of a pointed bracket
def getBracketEnd(expr,ind):
    level = 0
    for i in range(ind,len(expr)):
        if expr[i] in OPEN_BRA:
            level+=1
        elif expr[i] in CLOSE_BRA:
            level-=1
        if level==0:
            return i
    throwError("Parentesi non inserite correttamente")

#Resolver of Not Operation
def resolveNotOp(expr):
    for i in range(len(expr)):
        if expr[i] == NOTSYM:
            if isVar(expr[i+1]):
                pass
            elif expr in OPEN_BRA:
                expr = bracket_solve(expr,i)
            expr[i] = {'o':NOTSYM,'1':expr.pop(i+1)}
            return resolveNotOp(expr)
    #print(f"resolveNotOp {expr}")
    return expr

#search and solve brackets
def resolvBracket(expr):
    for i in range(len(expr)):
        if expr[i] in OPEN_BRA:
            expr = bracket_solve(expr,i)
            return resolvBracket(expr)
    #print(f"resolvBracket {expr}")
    return expr

#solve brackets
def bracket_solve(expr,init):
    if expr[init] in OPEN_BRA:
        end = getBracketEnd(expr,init)
        dexp = cvtArrayToDict(expr[init+1:end])#end-1
        for _ in range(end-init):
            del expr[init+1]
        expr[init] = dexp
        return expr
    throwError("Errore con le parentesi!")

#resolve an operation
def resolveOp(expr,op):
    for i in range(len(expr)):
        if expr[i] == op:
            if isVar(expr[i-1]) and isVar(expr[i+1]):
                rdict = cvtArrayToDict(expr[i-1:i+2])
                #print(rdict)
                del expr[i]
                del expr[i]
                expr[i-1] = rdict
                return resolveOp(expr,op)
            else:
                throwError(f"Operazione {op} ha operandi non validi! {i}")
    #print(f"resolveAndOp {expr}")
    return expr

#Translate array in dictionary and set the order of operation and the priorities
def cvtArrayToDict(expr):
    #print(expr)
    if len(expr) == 2:
        if expr[0] == NOTSYM and isVar(expr[1]):
            return {'o':NOTSYM, '1':expr[1]}
        else:
            throwError(f'Operazione "{expr[0]}" non valida su operando "{expr[1]}"!')
    elif len(expr) == 3:
        if isVar(expr[0]) and (expr[1] in OPER) and isVar(expr[2]): 
            return {'1':expr[0], 'o':expr[1], '2':expr[2]}
        else:
            throwError(f'Operazione "{expr[0]}" "{expr[1]}" "{expr[2]}" non valida!')
    else:
        expr = resolvBracket(expr)
        expr = resolveNotOp(expr)
        expr = resolveOp(expr,ANDSYM)
        expr = resolveOp(expr,ORSYM)
        if(len(expr) == 0):
            throwError("Errore nella risoluzione!")
        return expr[0]

#Separate special character OP+NOT
def separateOrAndToNot(ex):
    ORCOMB = ORSYM+NOTSYM
    ANDCOMB = ANDSYM+NOTSYM
    for i in range(len(ex)):
        if ex[i] == ORCOMB:
            first = ex[:i]
            second = ex[i+1:]
            ex = first + [ORSYM,NOTSYM] + second
            return separateOrAndToNot(ex)
        elif ex[i] == ANDCOMB:
            first = ex[:i]
            second = ex[i+1:]
            ex = first + [ANDSYM,NOTSYM] + second
            return separateOrAndToNot(ex)
    return ex

def getExpressionStructure(ex):
    ex = makeArray(ex) # Esemplify the string in blocks
    variables = symTable(ex)
    ex = separateOrAndToNot(ex)
    #print(ex)
    ex = cvtArrayToDict(ex)
    return [ex,variables]

def getValue(op,bVar,bVal):
    if type(op) is dict:
        return solveExpression(op,bVar,bVal)
    elif type(op) is str:
        #print(bVar)
        #print(op)
        return bVal[bVar.index(op)]
    else:
        throwError("unknow operand!")

def solveExpression(expr,variables,values):
    if expr in variables:
        return values[variables.index(expr)]
    if expr['o'] == ANDSYM:
        op1 = getValue(expr['1'],variables,values)
        op2 = getValue(expr['2'],variables,values)
        return op1 and op2
    elif expr['o'] == ORSYM:
        op1 = getValue(expr['1'],variables,values)
        op2 = getValue(expr['2'],variables,values)
        return op1 or op2
    elif expr['o'] == NOTSYM:
        op1 = getValue(expr['1'],variables,values)
        return not op1
    else:
        throwError("Operazione non identificata!")

def bitBool(v):
    if v:return '1'
    else: return '0'

def printRow(variables,value,res):
    for i in range(len(variables)):
        print(f'|  {variables[i]}: {bitBool(value[i])}  ',end='')
    print(f'|  ## Risultato: {bitBool(res)}')

def printVerityTable(sym,result,expression = None,intestation = True):
    if intestation:
        print("""
        ---------------------------------------
        ---          Verity Table.          ---
        ---------------------------------------
        """)
    if type(expression) is str:
        print(f"Espressione: {expression}")

    for i in range(len(result)):
        val = getCombination(i,len(sym))
        printRow(sym,val,result[i])

def getVerityTable(ex,sym):
    res = []
    for i in range(2**len(sym)):
        val = getCombination(i,len(sym))
        res.append(solveExpression(ex,sym,val))
    return res

def getMinTerm(results):
    res = []
    for i in range(len(results)):
        if results[i]:
            res.append(i)
    return res

def toCharBits(term,n_var):
    res = list(toBits(term,n_var))
    for i in range(len(res)):
        if res[i]: res[i] = '1'
        else: res[i] = '0'
    return tuple(res)

def toBitsMinTerm(minTerms,n_var):
    return [toCharBits(term,n_var) for term in minTerms]

#Minimization

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


'''
def getNoRepeat(vet):
    res = []
    for ele in vet:
        if ele not in res:
            res.append(ele)
    return res
'''

def getAdiacense(selection,finded=[]):
    #print(f"Selection:{selection}")
    #print(f"Finded:{finded}")
    #res = None
    if isMatEmpty(selection):
        return finded
    else:
        sel = compareSelection(selection,finded)
        return getAdiacense(sel,finded)

def getMulOfSum(minimized,sym):
    ex = ""
    for comb in minimized:
        for iBit in range(len(comb)):
            #print(comb)
            if comb[iBit] == '1':
                ex+=(sym[iBit]+' ')
            elif comb[iBit] == '0':
                ex+= (NOTSYM+sym[iBit]+' ')
        ex+= (ORSYM+' ')
    ex = ex[:len(ex)-len(ORSYM+' ')]
    return ex

def resultSelector(minTerms,results):
    anTab = getAnalyseMat(minTerms,results)
    res = []
    checked = []
    for x in range(len(anTab)):
        if minTerms[x] not in checked:
            repeted = len(minTerms)
            minPos = None
            for y in range(len(anTab[x])):
                if anTab[x][y]:
                    this_repeat = getRepeted(anTab,minTerms,y,checked)
                    if repeted > this_repeat:
                        repeted = this_repeat
                        minPos = y
            repeted = len(minTerms)
            for term in minTerms:
                if equalsIngoreNull(results[minPos],term):
                    checked.append(term)
            res.append(results[minPos])
    return res


def getRepeted(tab,minTerms,y,chk):
    count = 0
    for x in range(len(tab)):
        if tab[x][y]:
            if minTerms[x] in chk:
                count+=1
    return count



def getAnalyseMat(minTerms,results):
    mat = []
    for _ in range(len(minTerms)):
        mat.append([])
    for x in range(len(minTerms)):
        for y in range(len(results)):
            mat[x].append(equalsIngoreNull(minTerms[x],results[y]))
    return mat
    
def equalsIngoreNull(a,b):
    if len(b) != len(a): raise Exception(f"Impossible to compare this 2 terms {a} and {b}")
    for i in range(len(a)):
        if a[i]!=NULL_CHAR and b[i]!=NULL_CHAR:
            if a[i] != b[i]:
                return False
    return True

def getMinExpression(minTerms,n_var):
    minTerms = toBitsMinTerm(minTerms,n_var)
    minimise = getAdiacense(getBitSelection(minTerms,n_var))
    minimise = resultSelector(minTerms,minimise)
    return minimise

def getExpression(terms,bVars):
    return getMulOfSum(getMinExpression(terms,len(bVars)),bVars)
    

'''
Part for user requests
'''    

def inputNameVars():
    state = True
    while True:
        res = []
        state = True
        vars = input('Insert the name of variables separated with spaces:')
        vars = vars.split(' ')
        for ele in vars:
            if ele == '':
                pass
            elif ele.isalnum():
                if ele not in res:
                    res.append(ele)
            else:
                state = False
                break
        if state:
            return tuple(res)
        print('Insert legal names')

def inputMinTerms(n_var):
    state = True
    while True:
        res = []
        state = True
        max_value = 2**n_var-1
        vars = input(f'Insert bcd values separated with spaces MAX={max_value} :')
        vars = vars.split(' ')
        for ele in vars:
            if ele == '':
                pass
            elif ele.isnumeric() and int(ele)<= max_value :
                if int(ele) not in res:
                    res.append(int(ele))
            else:
                state = False
                break
        if state:
            res.sort()
            return tuple(res)
        print('Insert legal values')



def mainMenu():
    choise = MenuCreate(['- Insert expresion','- Insert results','- Exit'],"\nBoolean Resolver\n\n")
    if choise == 0:
        ex = input("Insert the expression:")
        #VERITY TABLE PRINT
        expression, bVars = getExpressionStructure(ex)
        results = getVerityTable(expression,bVars)
        printVerityTable(bVars,results,ex)
        #MINIMIZING
        print(f'\n\nMinimised Expression: {getExpression(getMinTerm(results),bVars)}\n')
    elif choise == 1:
        bVars = inputNameVars()
        if bVars != tuple([]):
            minTerms = inputMinTerms(len(bVars))
            print(f'\nExpession:{getExpression(minTerms,bVars)}')
        else:
            print('Cancelled!')
    if choise != 2:
        pause()
        
        




if __name__ == "__main__":
    try:
        mainMenu()
    except KeyboardInterrupt:
        print("\nProgram closed by user!")


