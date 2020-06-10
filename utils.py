'''
        Code by DomySh!
    Boolean Expression solver
    Minimising verity table 
    and a general expression
  GNU 3.0 General Public License
'''


ANDSYM = '*' #or space 
ORSYM = '+'
OPER = [ANDSYM,ORSYM]
NOTSYM = '!'
OPEN_BRA = ['(', '[', '{']
CLOSE_BRA = [')', ']', '}']
BRACKETS = OPEN_BRA+CLOSE_BRA

NULL_CHAR = '-' # have to be different from 0 and 1

def toBits(num,lenght):
    bitTester = 2**(lenght-1)
    val = []
    for _ in range(lenght):
        val.append(bool(int(int(num) & int(bitTester)) !=0))
        bitTester = int(bitTester//2)
    return tuple(val) 

def getMulOfSum(minimized,sym):
    ex = ""
    for comb in minimized:
        #print(comb)
        for iBit in range(len(comb)):
            #print(iBit)
            if comb[iBit] == '1':
                ex+=(sym[iBit]+' ')
            elif comb[iBit] == '0':
                ex+= (NOTSYM+sym[iBit]+' ')
        ex+= (ORSYM+' ')
    ex = ex[:len(ex)-len(ORSYM+' ')]
    return ex
