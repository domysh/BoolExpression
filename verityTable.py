'''
        Code by DomySh!
    Boolean Expression solver
    Minimising verity table 
    and a general expression
  GNU 3.0 General Public License
'''
from utils import toBits, ANDSYM, ORSYM, OPER, NOTSYM, OPEN_BRA, CLOSE_BRA, BRACKETS 

def throwError(s):
    raise Exception(s)
    
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

