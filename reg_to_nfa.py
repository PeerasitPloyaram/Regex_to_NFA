import json

non_symbols = ['u', '*', '.', '(', ')'] # Operation

'''
u = Union
* = Kleene
. = Concat
( ) = paren

จัดทำโดย
    นาย กิตติกานต์ มากผล 6410450087
    นาย นิสิต นะมิตร 6410451148
    นาย พีรสิษฐ์ พลอยอร่าม 6410451237
    นาย ศิวกร ภาสว่าง 6410451423
    ข้อ 1
'''

nfa = {}        # Define to Global Save Startstate, Acceptstate

class Operation:
    SYMBOL = 1

    CONCAT = 2
    UNION  = 3
    KLEENE = 4


class Tree:
    def __init__(self, Operation, value=None)-> None:
        self.Operation = Operation
        self.value = value
        self.left = None
        self.right = None


class NFAState:
    def __init__(self)-> None:
        self.next_state = {}
    

def createTree(regex)-> list:
    data = []
    for _ in regex:
        if _ == "u": # Union
            buffer = Tree(Operation.UNION)
            buffer.right = data.pop()
            buffer.left = data.pop()
            data.append(buffer)

        elif _ == ".":  # Concat
            buffer = Tree(Operation.CONCAT)
            buffer.right = data.pop()
            buffer.left = data.pop()
            data.append(buffer)

        elif _ == "*":  # Kleene
            buffer = Tree(Operation.KLEENE)
            # buffer.right = data.pop()
            buffer.left = data.pop()
            data.append(buffer)

        elif _ == "(" or _ == ")": # pass if not a operation
            continue

        else:
            data.append(Tree(Operation.SYMBOL, _))

    return data[0]



def compPrecedence(a, b):
    p = ["u", ".", "*"]             # * = 2, . = 1, u = 0
    return p.index(a) > p.index(b)  # return if index a > index b

def compute_regex(exp_t):
    if exp_t.Operation == Operation.CONCAT:
        return concat(exp_t)
    elif exp_t.Operation == Operation.UNION:
        return union(exp_t)
    elif exp_t.Operation == Operation.KLEENE:
        return kleeneStar(exp_t)
     
    else:
        return symbol(exp_t)


#===============Operations==================
def concat(exp_t):
    left_nfa  = compute_regex(exp_t.left)
    right_nfa = compute_regex(exp_t.right)

    left_nfa[1].next_state['E'] = [right_nfa[0]]
    return left_nfa[0], right_nfa[1]

def union(exp_t):
    start = NFAState()
    end = NFAState()

    first_nfa = compute_regex(exp_t.left)
    second_nfa = compute_regex(exp_t.right)

    start.next_state['E'] = [first_nfa[0], second_nfa[0]]
    first_nfa[1].next_state['E'] = [end]
    second_nfa[1].next_state['E'] = [end]

    return start, end

def kleeneStar(exp_t):
    start = NFAState()
    end = NFAState()

    starred_nfa = compute_regex(exp_t.left)

    start.next_state['E'] = [starred_nfa[0], end]
    starred_nfa[1].next_state['E'] = [starred_nfa[0], end]

    return start, end

def symbol(exp_t):
    start = NFAState()
    end = NFAState()
    
    start.next_state[exp_t.value] = [end]
    return start, end
#=====================================



def arrange_transitions(state, states_done, symbol_table):
    global nfa

    if state in states_done:
        return

    states_done.append(state)

    for symbol in list(state.next_state):
        if symbol not in nfa['letters']:
            nfa['letters'].append(symbol)
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = sorted(symbol_table.values())[-1] + 1
                q_state = "Q" + str(symbol_table[ns])
                nfa['states'].append(q_state)
            nfa['transition'].append(["Q" + str(symbol_table[state]), symbol, "Q" + str(symbol_table[ns])])

        for ns in state.next_state[symbol]:
            arrange_transitions(ns, states_done, symbol_table)

def final_st_dfs():
    global nfa

    for _ in nfa["states"]:
        counter = 0

        for val in nfa['transition']:
            if val[0] == _ and val[2] != _:
                counter += 1
        if counter == 0 and _ not in nfa["final_states"]:
            nfa["final_states"].append(_)


def arrange_nfa(fa):
    global nfa

    # Define nfa for save
    nfa['states'] = []
    nfa['letters'] = []
    nfa['transition'] = []
    nfa['start_states'] = []
    nfa['final_states'] = []

    q_1 = "Q" + str(1)                          # State Pattern
    nfa['states'].append(q_1)                   # Add to nfa
    arrange_transitions(fa[0], [], {fa[0] : 1}) # Cut
    
    nfa["start_states"].append("Q1")            # Add a Start State
    final_st_dfs()  # Find Final State


def appendConcat(regex):
    global non_symbols
    l = len(regex)
    buffer = []         # new REGEX after add concat aub(ab) -> 

    for i in range(l - 1):
        buffer.append(regex[i])

        if regex[i] not in non_symbols:
            if regex[i + 1] not in non_symbols or regex[i + 1] == '(':
                buffer += '.'

        if regex[i] == ')' and regex[i + 1] == '(':
            buffer += '.'

        if regex[i] == '*' and regex[i + 1] == '(':
            buffer += '.'

        if regex[i] == '*' and regex[i + 1] not in non_symbols:
            buffer += '.'

        if regex[i] == ')' and regex[i + 1] not in non_symbols:
            buffer += '.'

    buffer += regex[l - 1]
    return buffer

def notation_to_num(str):
    return int(str[1:])


def compute_postfix(regex):
    stk = []
    buffer = ""

    for c in regex:
        if c not in non_symbols or c == "*":
            buffer += c
        elif c == ")":
            while len(stk) > 0 and stk[-1] != "(":
                buffer += stk.pop()
            stk.pop()
        elif c == "(":
            stk.append(c)
        elif len(stk) == 0 or stk[-1] == "(" or compPrecedence(c, stk[-1]):
            stk.append(c)
        else:
            while len(stk) > 0 and stk[-1] != "(" and not compPrecedence(c, stk[-1]):
                buffer += stk.pop()
            stk.append(c)

    while len(stk) > 0:
        buffer += stk.pop()

    return buffer

def convertRegex(regex):
    reg = appendConcat(regex)
    return compute_postfix(reg)

def createNfa(regex):
    tree = createTree(regex)
    treeCompute = compute_regex(tree)
    return arrange_nfa(treeCompute)


def saveToJson(fileName:str )->None:
    global nfa

    with open(fileName, 'w') as file:
        file.write(json.dumps(nfa, indent = 4))

        
def showNfaTable()->None:
    global nfa
    # Print Table


    size_col = len(nfa["letters"])  # Size Spacee Column
    # Pattern
    upper_col_border = "----------"
    states_border = " --------"
    lower_col_border = "---------|"
    transition_space = "         "



    print(f"{states_border}{upper_col_border * size_col}")

    if size_col > 3:
        print(f"| States |{transition_space} Transitions{transition_space * (size_col - 2)}|")  # Print Transitions Header
    else:
        print(f"| States |{transition_space}Transitions{transition_space * (size_col - 2)}|")   # Print Transitions Header
    print("|        |", end="") # Print Space States

    for l in nfa['letters']:
        print("    {}    |".format(l), end="")          # All Letter

    print(f"\n|--------|{upper_col_border * size_col}") # Lower Table Border

    for state in nfa['states']:
        if len(state) <= 2:                     # IF Q < 10
            print("|  ", state, "  |", end="")   # state and Transitions
            for trans in nfa["transition"]:
                if state == trans[0]:           # If Round Q State
                    # print(trans)
                    space = " "                 # Space for correct col
                    sequence = 1                # Position of States

                    for i in nfa["letters"]:    # Loop fin State Q-
                        if trans[1] == i:
                            print(f"{space * sequence}{trans[2]}",end="")  # Print State Transitions by sequence Position
                        sequence += 11          # Col Margin
        else:                                   # IF Q > 10
            print("|  ",state," |",end="")
            for trans in nfa["transition"]:
                if state == trans[0]:           # If Rouond Q State
                    space = " "
                    sequence = 1

                    for i in nfa["letters"]:
                        if trans[1] == i:
                            print(f"{space * sequence}{trans[2]}",end="") # Print State Transitions by sequence Position
                        sequence += 11
        # print(f"\n|--------|{lower_state_border * size_col}") # Lower Table Border
        print(f"\n|--------|{lower_col_border * size_col}") # Lower Table Border

    print("\nStart state is: {}".format(nfa["start_states"][0]))    # Print Start State
    print("Final states is: ", end="")                              # Print Final State
    for state in nfa["final_states"]:
        print( state, end="")                                       # Print State
    print("\n")


# if __name__ == "__main__":
#     regex = input()
#     convert = convertRegex(regex)
#     te = createNfa(convert)
#     saveToJson("NFAoutput.json")
#     showNfaTable()