'''
        Code by DomySh!
    Boolean Expression solver
    Minimising verity table 
    and a general expression
  GNU 3.0 General Public License
'''
import sys
import verityTable
from TerminalMenu import MenuCreate
from utils import getMulOfSum

from petrick import toBitsMinTerm, petrickMethod, getPatrickExpression
from mcCluskey import getTerms

#Pause Function
def pause():input("Press Enter...")

#Error Function
def throwError(s):
    print(f"\nERRORE INDIVIDUATO!\n{s}")
    pause()
    sys.exit()

#--------------------
#--- Minimization ---
#--------------------

def getMinExpression(minTerms,n_var):
    minTerms = toBitsMinTerm(minTerms,n_var)
    minimise = getTerms(minTerms,n_var)
    return petrickMethod(getPatrickExpression(minTerms,minimise))

def getRepeted(tab,minTerms,y,chk):
    count = 0
    for x in range(len(tab)):
        if tab[x][y]:
            if minTerms[x] in chk:
                count+=1
    return count


def getExpression(terms,bVars):
    expr = getMinExpression(terms,len(bVars))
    res = []
    for ele in expr:
        #print(ele,bVars)
        res.append(getMulOfSum(ele,bVars))
    return res
    
def printExp(ex):
    for ele in ex:
        print("-------------------------------")
        print(ele)
    print("-------------------------------")
'''
Part for user requests
'''    

def inputNameVars():
    state = True
    while state:
        n_var = input('Insert how many variables to put:')
        try:
            n_var = int(n_var)
            if n_var>0:
                state = False
            else:
                print("Insert positive number")
        except:
            print("Insert valid value!")
    name_var = []
    for i in range(n_var):
        name_var.append(getLetter(i))
    return name_var

def getLetter(n):
    state = int(n/26)
    if state>=1:
            return getLetter(state-1)+getLetter(int(n%26))      
    else:
        return chr(65+n)

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
        expression, bVars = verityTable.getExpressionStructure(ex)
        results = verityTable.getVerityTable(expression,bVars)
        verityTable.printVerityTable(bVars,results,ex)
        #MINIMIZING
        print(f'\n\nMinimised Expressions:\n')
        printExp(getExpression(verityTable.getMinTerm(results),bVars))
    elif choise == 1:
        bVars = inputNameVars()
        if bVars != tuple([]):
            minTerms = inputMinTerms(len(bVars))
            print(f'\nExpessions:\n')
            printExp(getExpression(minTerms,bVars))
        else:
            print('Cancelled!')
    elif choise == 2:
        sys.exit()
    
    pause()
            
            

if __name__ == "__main__":
    try:
        mainMenu()
    except KeyboardInterrupt:
        print("\nProgram closed by user!")
    except Exception as e:
        throwError(str(e))


