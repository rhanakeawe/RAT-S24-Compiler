import lexical_3 as lexical
import pathlib
import sys

token_list = []

# Toggles
switch = False
error_message_toggle = True

instruction_table = []
#              [0]        [1]
# "Address", "Operator","Operand"
#  1          PUSHM      5001

symbol_table = []
#   [0]              [1]            [2]
# "Identifier", "MemoryLocation", "Type"
#   max             5000              integer

jump_stack = []

instr_address = 1
memory_address = 5000
symbol_type = ''

def change_type():
    global symbol_type
    symbol_type = token_list[0]

def insert_symbol():
    global memory_address
    if not any(token_list[0] in symbol for symbol in symbol_table):
        symbol_table.append([token_list[0], memory_address, symbol_type])
        memory_address += 1
    else:
        print(f"{token_list[0]} is already in symbol table!")

def print_instruction():
    print("=================\nInstruction Table\n=================",file=output_file)
    for number, instructions in enumerate(instruction_table):
        if instructions[1] == 'nil':
            instructions[1] = ''
        print(number+1,".","{: >8} {: >8}".format(*instructions),file=output_file)

def print_symbol():
    print("\n=============\nSymbol Table\n=============",file=output_file)
    print("Identifier   MemoryLocation   Type\n",file=output_file)
    for symbol in symbol_table:
        print("{: >8} {: >13} {: >12}".format(*symbol),file=output_file)

def get_Address(token):
    for symbol in symbol_table:
        if token == symbol[0]:
            return symbol[1]

def generate_instruction(op, oprnd):
    global instr_address
    instruction_table.append([op, oprnd])
    instr_address += 1

def push_jumpstack(jump_address):
    jump_stack.append(jump_address)

def pop_jumpstack():
    out = jump_stack[-1]
    jump_stack.pop()
    return out

def back_patch(jump_address):
    addr = pop_jumpstack()
    instruction_table[addr-1][1] = jump_address

# Prints fails to terminal
def Missing_Message(func_name, failure):
    if error_message_toggle == True:
        s = func_name + ": no " + failure + " | Token at: " + token_list[0]
        print(s)

# Prints production rules used
def SyntaxLogger(syntax):
    if switch == True:
        print(syntax,file=output_file)

# Prints Lexical analysis and Pops token from list
def Terminate_Lexer():
    #print('―' * 100,file=output_file)
    #print(lexical.lexer(token_list[0]),file=output_file)
    #print('―' * 100,file=output_file)
    token_list.pop(0)

### Check the "SyntaxLogger()" at the begging of each function for what it does

# The Main Function
def Rat24S():
    SyntaxLogger("<Rat24S> -> $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $")
    if token_list[0] == '$':
        Terminate_Lexer()
        if Opt_Function_Def():
            if token_list[0] == '$':
                Terminate_Lexer()
                if Opt_Declaration_List():
                    if token_list[0] == '$':
                        Terminate_Lexer()
                        if Statement_List():
                            if token_list[0] == '$':
                                Terminate_Lexer()
                                print("This has great grammar! Good job!")
                            else:
                                Missing_Message("Rat24S","$ 4")
                        else:
                            Missing_Message("Rat24S","Statement_List")
                    else:
                        Missing_Message("Rat24S","$ 3")
                else:
                    Missing_Message("Rat24S","Opt_Declaration_List")
            else:
                Missing_Message("Rat24S","$ 2")
        else:
            Missing_Message("Rat24S","Opt_Function_Def")
    else:
        Missing_Message("Rat24S","$ 1")
    print_instruction()
    print_symbol()
                            
# no change
def Opt_Function_Def():
    SyntaxLogger("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
    if Function_Def():
        return True
    elif EEmpty():
        return True
    else:
        Missing_Message("Opt_Function_Def","Function_Def or EEmpty")

# no change      
def Function_Def():
    SyntaxLogger("<Function Definitions> -> <Function> <Function Definitions>'")
    if FFunction():
        if Function_Def_Dash():
            return True
        else:
            Missing_Message("Function_Def","Function_Def_Dash")
    else:
        Missing_Message("Function_Def","FFunction")

# no change
# epsilon
def Function_Def_Dash():
    SyntaxLogger("<Function Definitions>' -> <Function Definitions> | ϵ")
    if Function_Def():
        return True
    else:
        return True

# no change
def FFunction():
    SyntaxLogger("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    if token_list[0] == 'function':
        Terminate_Lexer()
        if (lexical.lexer(token_list[0])[0] == 'id'):
            Terminate_Lexer()
            if (token_list[0]) == '(':
                Terminate_Lexer()
                if Opt_Parameter_List():
                    if token_list[0] == ')':
                        Terminate_Lexer()
                        if Opt_Declaration_List():
                            if Body():
                                return True
                            else:
                                Missing_Message("FFunction","Body")
                        else:
                            Missing_Message("FFunction","Opt_Declaration_List")
                    else:
                        Missing_Message("FFunction",")")
                else:
                    Missing_Message("FFunction","Opt_Declaration_List")
            else:
                Missing_Message("FFunction","(")
        else:
            Missing_Message("FFunction","id")
    else:
        Missing_Message("FFunction","function")

# no change
def Opt_Parameter_List():
    SyntaxLogger("<Opt Parameter List> -> <Parameter List> | <Empty>")
    if Parameter_List():
        return True
    elif EEmpty():
        return True

# no change
def Parameter_List():
    SyntaxLogger("<Parameter List> -> <Parameter> <Parameter List>'")
    if PParameter():
        if Parameter_List_Dash():
            return True
        else:
            Missing_Message("Parameter_List","Parameter_List_Dash")
    else:
        Missing_Message("Parameter_List","PParameter")

# no change
def PParameter():
    SyntaxLogger("<Parameter> -> <IDs> <Qualifier>")
    if IDs():
        if Qualifier():
            return True
        else:
            Missing_Message("PParameter","Qualifier")
    else:
        Missing_Message("PParameter","IDs")

# no change
# epsilon
def Parameter_List_Dash():
    SyntaxLogger("<Parameter List>' -> , <Parameter List> | ϵ")
    if token_list[0] == ',':
        Terminate_Lexer()
        if Parameter_List():
            return  True
        else:
            Missing_Message("Parameter_List_Dash","Parameter_List")
    else:
        return True

# no change
def Qualifier():
    SyntaxLogger("<Qualifier> -> integer | boolean | real")
    if token_list[0] == 'integer' or token_list[0] == 'boolean':
        change_type()
        Terminate_Lexer()
        return True
    elif token_list[0] == 'real':
        print("Real is not allowed! Exiting")
        exit()
    else:
        Missing_Message("Qualifier", "integer or real or boolean")

# no change
def Body():
    SyntaxLogger("<Body> -> { <Statement List> }")
    if token_list[0] == '{':
        Terminate_Lexer()
        if Statement_List():
            if token_list[0] == '}':
                Terminate_Lexer()
                return True
            else:
                Missing_Message("Body","}")
        else:
            Missing_Message("Body","Statement_List")
    else:
        Missing_Message("Body","{")


def Opt_Declaration_List():
    SyntaxLogger("<Opt Declaration List> -> <Declaration List> | <Empty>")
    if Declaration_List():
        return True
    elif EEmpty():
        return True
    else:
        Missing_Message("Opt_Declaration_List","Declaration_List or EEmpty")


def Declaration_List():
    SyntaxLogger("<Declaration List> -> <Declaration>; <Declaration List>'")
    if Declaration():
        if token_list[0] == ';':
            Terminate_Lexer()
            if Declaration_List_Dash():
                return True
            else:
                Missing_Message("Declaration_List","Declaration_List_Dash")
        else:
            Missing_Message("Declaration_List",";")
    else:
        Missing_Message("Declaration_List","Declaration")


# epsilon
def Declaration_List_Dash():
    SyntaxLogger("<Declaration List>' -> <Declaration List> | ϵ")
    if Declaration_List():
        return True
    else:
        return True


def Declaration():
    SyntaxLogger("<Declaration> -> <Qualifier> <IDs>")
    if Qualifier():
        if IDs():
            return True
        else:
            Missing_Message("Declaration","IDs")
    else:
        Missing_Message("Declaration","Qualifier")


def IDs():
    SyntaxLogger("<IDs> -> <Identifier> <IDs>'")
    if lexical.lexer(token_list[0])[0] == 'id':
        insert_symbol()
        Terminate_Lexer()
        if IDs_Dash():
            return True
        else:
            Missing_Message("IDs","IDs_Dash")
    else:
        Missing_Message("IDs","id")


# epsilon
def IDs_Dash():
    SyntaxLogger("<IDs>' -> , <IDs> | ϵ")
    if token_list[0] == ',':
        Terminate_Lexer()
        if IDs():
            return True
    else:
        return True


def Statement_List():
    SyntaxLogger("<Statement List> -> <Statement> <Statement List>'")
    if Statement():
        if Statement_List_Dash():
            return True
        else:
            Missing_Message("Statement_List","Statement_List_Dash")
    else:
        Missing_Message("Statement_List","Statement")


# epsilon
def Statement_List_Dash():
    SyntaxLogger("<Statement List>' -> <Statement List> | ϵ")
    if Statement_List():
        return True
    else:
        return True


def Statement():
    SyntaxLogger("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
    if Compound():
        return True
    elif Assign():
        return True
    elif IIf():
        return True
    elif RReturn():
        return True
    elif PPrint():
        return True
    elif Scan():
        return True
    elif While():
        return True
    else:
        Missing_Message("Statement","Compound etc")


def Compound():
    SyntaxLogger("<Compound> -> { <Statement List> }")
    if token_list[0] == '{':
        Terminate_Lexer()
        if Statement_List():
            if token_list[0] == '}':
                Terminate_Lexer()
                return True
            else:
                Missing_Message("Compound","}")
        else:
            Missing_Message("Compound","Statement_List")
    else:
        Missing_Message("Compound","{")


def Assign():
    SyntaxLogger("<Assign> -> <Identifier> = <Expression> ;")
    if lexical.lexer(token_list[0])[0] == 'id':
        save = token_list[0]
        Terminate_Lexer()
        if token_list[0] == '=':
            Terminate_Lexer()
            if Expression():
                generate_instruction('POPM',get_Address(save))
                if token_list[0] == ';':
                    Terminate_Lexer()
                    return True
                else:
                    Missing_Message("Assign",";")
            else:
                Missing_Message("Assign","Expression")
        else:
            Missing_Message("Assign","=")
    else:
        Missing_Message("Assign","id")


def IIf():
    SyntaxLogger("<If> -> if ( <Condition> ) <Statement> <If>'")
    if token_list[0] == 'if':
        Terminate_Lexer()
        if token_list[0] == '(':
            Terminate_Lexer()
            if CCondition():
                if token_list[0] == ')':
                    Terminate_Lexer()
                    if Statement():
                        if IIf_Dash():
                            return True
                        else:
                            Missing_Message("IIf","IIf_Dash")
                    else:
                        Missing_Message("IIf","Statement")
                else:
                    Missing_Message("IIf",")")
            else:
                Missing_Message("IIf","CCondition")
        else:
            Missing_Message("IIf","(")
    else:
        Missing_Message("IIf","if")
        
def IIf_Dash():
    SyntaxLogger("<If>' -> endif | else <Statement> endif")
    if token_list[0] == 'endif':
        Terminate_Lexer()
    elif token_list[0] == 'else':
        Terminate_Lexer()
        if Statement():
            back_patch(instr_address)
            if token_list[0] == 'endif':
                Terminate_Lexer()
                return True
            else:
                Missing_Message("IIf_Dash","endif")
        else:
            Missing_Message("IIf_Dash","Statement")
    else:
        Missing_Message("IIf_Dash","else")

def RReturn():
    SyntaxLogger("<Return> -> return <Return>'")
    if token_list[0] == 'return':
        Terminate_Lexer()
        if RReturn_Dash():
            return True
        else:
            Missing_Message("IIf_Dash","RReturn_Dash")
    else:
        Missing_Message("IIf_Dash","return")


def RReturn_Dash():
    SyntaxLogger("<Return>' -> ; | <Expression> ;")
    if token_list[0] == ';':
        Terminate_Lexer()
        return True
    elif Expression():
        if token_list[0] == ';':
            Terminate_Lexer()
            return True
        else:
            Missing_Message("IIf_Dash",";")
    else:
        Missing_Message("IIf_Dash","Expression")


def PPrint():
    SyntaxLogger("<Print> -> print ( <Expression> );")
    if token_list[0] == 'print':
        Terminate_Lexer()
        if token_list[0] == '(':
            Terminate_Lexer()
            if Expression():
                generate_instruction('SOUT', 'nil')
                if token_list[0] == ')':
                    Terminate_Lexer()
                    if token_list[0] == ';':
                        Terminate_Lexer()
                        return True
                    else:
                        Missing_Message("PPrint",";")
                else:
                    Missing_Message("PPrint",")")
            else:
                Missing_Message("PPrint","Expression")
        else:
            Missing_Message("PPrint","(")
    else:
        Missing_Message("PPrint","print")


def Scan():
    SyntaxLogger("<Scan> -> scan ( <IDs> );")
    if token_list[0] == 'scan':
        Terminate_Lexer()
        if token_list[0] == '(':
            Terminate_Lexer()
            generate_instruction('SIN', 'nil')
            generate_instruction('POPM', get_Address(token_list[0]))
            if IDs():
                if token_list[0] == ')':
                    Terminate_Lexer()
                    if token_list[0] == ';':
                        Terminate_Lexer()
                        return True
                    else:
                        Missing_Message("Scan",";")
                else:
                    Missing_Message("Scan",")")
            else:
                Missing_Message("Scan","IDs")
        else:
            Missing_Message("Scan","(")
    else:
        Missing_Message("Scan","scan")


def While():
    SyntaxLogger("<While> -> while ( <Condition> ) <Statement> endwhile")
    if token_list[0] == 'while':
        Ar = instr_address
        generate_instruction('LABEL','nil')
        Terminate_Lexer()
        if token_list[0] == '(':
            Terminate_Lexer()
            if CCondition():
                if token_list[0] == ')':
                    Terminate_Lexer()
                    if Statement():
                        generate_instruction('JUMP',Ar)
                        back_patch(instr_address)
                        if token_list[0] == 'endwhile':
                            Terminate_Lexer()
                            return True
                        else:
                            Missing_Message("While","endwhile")
                    else:
                        Missing_Message("While","Statement")
                else:
                    Missing_Message("While",")")
            else:
                Missing_Message("While","CCondition")
        else:
            Missing_Message("While","(")
    else:
        Missing_Message("While","while")

# apart of while
def CCondition():
    SyntaxLogger("<Condition> -> <Expression> <Relop> <Expression>")
    if Expression():
        op = token_list[0]
        if Relop():
            if Expression():
                match op:
                    case '<':
                        generate_instruction('LES','nil')
                        push_jumpstack(instr_address)
                        generate_instruction('JUMP0','nil')
                    case '>':
                        generate_instruction('GRT','nil')
                        push_jumpstack(instr_address)
                        generate_instruction('JUMP0','nil')
                    case '==':
                        generate_instruction('EQU','nil')
                        push_jumpstack(instr_address)
                        generate_instruction('JUMP0','nil')
                    case '!=':
                        generate_instruction('NEQ','nil')
                        push_jumpstack(instr_address)
                        generate_instruction('JUMP0','nil')
                    case '=>':
                        generate_instruction('GEQ','nil')
                        push_jumpstack(instr_address)
                        generate_instruction('JUMP0','nil')
                    case '<=':
                        generate_instruction('LEQ','nil')
                        push_jumpstack(instr_address)
                        generate_instruction('JUMP0','nil')
                return True
            else:
                Missing_Message("CCondition","Expression 2")
        else:
            Missing_Message("CCondition","Relop")
    else:
        Missing_Message("CCondition","Expression 1")

# apart of while
def Relop():
    SyntaxLogger("<Relop> -> == | != | > | < | <= | =>")
    if token_list[0] == '==' or token_list[0] == '!=' or token_list[0] == '>' or token_list[0] == '<' or token_list[0] == '<=' or token_list[0] == '=>':
        Terminate_Lexer()
        return True
    else:
        Missing_Message("Relop","== or != or etc")


def Expression():
    SyntaxLogger("<Expression> -> <Term> <Expression>'")
    if Term():
        if Expression_Dash():
            return True
        else:
            Missing_Message("Expression","Expression_Dash")
    else:
        Missing_Message("Expression","Term")


def Term():
    SyntaxLogger("<Term> -> <Factor> <Term>'")
    if Factor():
        if Term_Dash():
            return True
        else:
            Missing_Message("Term","Term_Dash")
    else:
        Missing_Message("Term","Factor")


# epsilon
def Expression_Dash():
    SyntaxLogger("<Expression>' -> + <Term> <Expression>' | - <Term> <Expression>' | ϵ")
    if token_list[0] == '+':
        Terminate_Lexer()
        if Term():
            generate_instruction('A','nil')
            if Expression_Dash():
                return True
            else:
                Missing_Message("Expression_Dash","Expression_Dash")
        else:
            Missing_Message("Expression_Dash","Term")
    elif token_list[0] == '-':
        Terminate_Lexer()
        if Term():
            if Expression_Dash():
                return True
            else:
                Missing_Message("Expression_Dash","Expression_Dash 2")
        else:
            Missing_Message("Expression_Dash","Term 2")
    else:
        return True


# epsilon
def Term_Dash():
    SyntaxLogger("<Term>' -> * <Factor> <Term>' | / <Factor> <Term>' | ϵ")
    if token_list[0] == '*':
        Terminate_Lexer()
        if Factor():
            generate_instruction('M','nil')
            if Term_Dash():
                return True
            else:
                Missing_Message("Term_Dash", "Term_Dash 1")
        else:
            Missing_Message("Term_Dash", "Factor 1")
    elif token_list[0] == '/':
        Terminate_Lexer()
        if Factor():
            generate_instruction('D','nil')
            if Term_Dash():
                return True
            else:
                Missing_Message("Term_Dash", "Term_Dash 2")
        else:
            Missing_Message("Term_Dash", "Factor 2")
    else:
        return True


def Factor():
    SyntaxLogger("<Factor> -> - <Primary> | <Primary>")
    if token_list[0] == '-':
        Terminate_Lexer()
        if Primary():
            return True
    elif Primary():
        return True
    else:
        Missing_Message("Factor","- or Primary")


def Primary():
    SyntaxLogger("<Primary> -> <Identifier> <Primary>' | <Integer> | ( <Expression> ) | <Real> | true | false")
    if lexical.lexer(token_list[0])[0] == 'id':
        generate_instruction('PUSHM', get_Address(token_list[0]))
        Terminate_Lexer()
        if Primary_Dash():
            return True
    elif lexical.lexer(token_list[0])[0] == 'integer':
        generate_instruction('PUSHI', token_list[0])
        Terminate_Lexer()
        return True
    elif token_list[0] == '(':
        Terminate_Lexer()
        if Expression():
            if token_list[0] == ')':
                Terminate_Lexer()
                return True
    elif lexical.lexer(token_list[0])[0] == 'real':
        print("Real not allowed! Exiting")
        exit()
    elif token_list[0] == 'true':
        Terminate_Lexer()
        return True
    elif token_list[0] == 'false':
        Terminate_Lexer()
        return True
    else:
        Missing_Message("Primary","Identifier Primary_Dash or Integer or etc")


# epsilon
def Primary_Dash():
    SyntaxLogger("<Primary>' -> ( <IDs> ) | ϵ")
    if token_list[0] == '(':
        Terminate_Lexer()
        if IDs():
            if token_list[0] == ')':
                Terminate_Lexer()
                return True
            else:
                Missing_Message("Primary_Dash",")")
        else:
            Missing_Message("Primary_Dash","IDs")
    else:
        return True


def EEmpty():
    SyntaxLogger("<Empty> -> ϵ")
    return True

for token in lexical.tokenizer():
    for token2 in token:
        token_list.append(token2)

path = pathlib.Path('./output')
path.mkdir(parents=True,exist_ok=True)

output = str(sys.argv[1])
output = output.replace('.txt','')
output_syntax = "./output/simple_" + output + ".txt"
with open(output_syntax,'w', encoding="utf-8") as output_file:
    Rat24S()
output_file.close()