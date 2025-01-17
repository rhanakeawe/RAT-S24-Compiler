import warnings
import lexical_3 as lexical
import sys

token_list = []

has_invalid = False
switch = True
global number

def Rat24S(number):
    token = token_list[number][1]
    if switch == True:
        print("<Rat24S> -> $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $")
    if token_list[number][1] == '$':
        number = number + 1
        if Opt_Function_Def(number):
            if token_list[number][1] == '$':
                number = number + 1
                if Opt_Declaration_List(number):
                    if token_list[number][1] == '$':
                        number = number + 1
                        if Statement_List(number):
                            print("Syntax Good!")
                        else:
                            print("Failed at Statement_List")
                            exit()
                    else:
                        print("Failed at dollar 3")
                        exit()
                else:
                    print("Failed at Opt_Declaration_List")
                    exit()
            else:
                print("Failed at dollar 2")
                exit()
        else:
            print("Failed at Opt_Function_Def")
            exit()
    else:
        print("Failed at dollar 1")
        exit()


def Opt_Function_Def(number):
    print(number)
    if switch == True:
        print("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
    if Function_Def(number):
        return True
    elif EEmpty(number):
        return True
    else:
        return False
            
def Function_Def(number):
    print(number)
    if switch == True:
        print("<Function Definitions> -> <Function> <Function Definitions>'")
    if FFunction(number):
        if Function_Def_Dash(number+1):
            return True
        else:
            return False
    else:
        return False

# epsilon
def Function_Def_Dash(number):
    print(number)
    if switch == True:
        print("<Function Definitions>' -> <Function Definitions> | ϵ")
    if Function_Def(number):
        return True
    else:
        #return False
        return True

def FFunction(number):
    print(number)
    if switch == True:
        print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    if token_list[number][1] == 'function':
        number = number + 1
        if token_list[number][0] == 'id':
            number = number + 1
            if token_list[number][1] == '(':
                number = number + 1
                if Opt_Parameter_List(number):
                    if token_list[number][1] == ')':
                        number = number + 1
                        if Opt_Parameter_List(number):
                            if Opt_Parameter_List(number):
                                return True
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def Opt_Parameter_List(number):
    print(number)
    if switch == True:
        print("<Opt Parameter List> -> <Parameter List> | <Empty>")
    if Parameter_List(number):
        return True
    elif EEmpty(number):
        return True
    else:
        return False

def Parameter_List(number):
    print(number)
    if switch == True:
        print("<Parameter List> -> <Parameter> <Parameter List>'")
    if PParameter(number):
        if Parameter_List_Dash(number):
            return True
        else:
            return False
    else:
        return False

def PParameter(number):
    print(number)
    if switch == True:
        print("<Parameter> -> <IDs> <Qualifier>")
    if IDs(number):
        if Qualifier(number):
            return True
        else:
            return False
    else:
        return False

# epsilon
def Parameter_List_Dash(number):
    print(number)
    if switch == True:
        print("<Parameter List>' -> , <Parameter List> | ϵ")
    if token_list[number][1] == ',':
        number = number + 1
        if Parameter_List(number):
            return True
        else:
            return False
    else:
        #return False
        return True

def Qualifier(number):
    print(number)
    if switch == True:
        print("<Qualifier> -> integer | boolean | real")
    if (token_list[number][0] == 'integer' or token_list[number][0] == "real"):
        number = number + 1
        return True
    elif (token_list[number][1] == 'false' or token_list[number][1] == 'true'):
        number = number + 1
        return True
    else:
        return False

def Body(number):
    print(number)
    if switch == True:
        print("<Body> -> { <Statement List> }")
    if token_list[number][1] == '{':
        if Statement_List(number):
            if token_list[number] == '}':
                number = number + 1
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def Opt_Declaration_List(number):
    print(number)
    if switch == True:
        print("<Opt Declaration List> -> <Declaration List> | <Empty>")
    if Declaration_List(number):
        return True
    elif EEmpty(number):
        return True
    else:
        return False

def Declaration_List(number):
    print(number)
    if switch == True:
        print("<Declaration List> -> <Declaration>; <Declaration List>'")
    if Declaration(number):
        if token_list[number][1] == ';':
            number = number + 1
            if Declaration_List_Dash(number):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# epsilon
def Declaration_List_Dash(number):
    print(number)
    if switch == True:
        print("<Declaration List>' -> <Declaration List> | ϵ")
    if Declaration_List(number):
        return True
    else:
        #return False
        return True

def Declaration(number):
    print(number)
    if switch == True:
        print("<Declaration> -> <Qualifier> <IDs>")
    if Qualifier(number):
        if IDs(number):
            return True
        else:
            return False
    else:
        return False

def IDs(number):
    print(number)
    if switch == True:
        print("<IDs> -> <Identifier> <IDs>'")
    if token_list[number][0] == 'id':
        number = number + 1
        if IDs_Dash(number):
            return True
        else:
            return False
    else:
        return False

# epsilon
def IDs_Dash(number):
    print(number)
    if switch == True:
        print("<IDs>' -> , <IDs> | ϵ")
    if token_list[number][1] == ',':
        if IDs(number):
            number = number + 1
            return True
        else:
            return False
    else:
        #return False
        return True

def Statement_List(number):
    print(number)
    if switch == True:
        print("<Statement List> -> <Statement> <Statement List>'")
    if Statement(number):
        if Statement_List_Dash(number):
            return True
        else:
            return False
    else:
        return False

# epsilon
def Statement_List_Dash(number):
    print(number)
    if switch == True:
        print("<Statement List>' -> <Statement List> | ϵ")
    if Statement_List(number):
        return True
    else:
        #return False
        return True

def Statement(number):
    print(number)
    if switch == True:
        print("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
    if (Compound(number) or Assign(number) or If(number) or Return(number) or PPrint(number) or Scan(number) or While(number)):
        return True
    else:
        return False

def Compound(number):
    print(number)
    if switch == True:
        print("<Compound> -> { <Statement List> }")
    if token_list[number][1] == '{':
        number = number + 1
        if Statement_List(number):
            if token_list[number] == '}':
                number = number + 1
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def Assign(number):
    print(number)
    if switch == True:
        print("<Assign> -> <Identifier> = <Expression> ;")
    if token_list[number][0] == 'id':
        number = number + 1
        if token_list[number][1] == '=':
            number = number + 1
            if Expression(number):
                if token_list[number] == ';':
                    number = number + 1
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def If(number):
    print(number)
    if switch == True:
        print("<If> -> if ( <Condition> ) <Statement> endif | if ( <Condition> ) <Statement> else <Statement> endif")
    if token_list[number][1] == 'if':
        number = number + 1
        if token_list[number][1] == '(':
            number = number + 1
            if CCondition(number):
                if token_list[number][1] == ')':
                    number = number + 1
                    if Statement(number):
                        if token_list[number][1] == 'endif':
                            number = number + 1
                            return True
                        elif token_list[number][1] == 'else':
                            number = number + 1
                            if Statement(number):
                                if token_list[number][1] == 'endif':
                                    number = number + 1
                                    return True
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def Return(number):
    print(number)
    if switch == True:
        print("<Return> -> return; | return <Expression>;")
    if token_list[number][1] == 'return':
        number = number + 1
        if token_list[number][1] == ';':
            number = number + 1
            return True
        elif Expression(number):
            if token_list[number][1] == ';':
                number = number + 1
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def PPrint(number):
    print(number)
    if switch == True:
        print("<Print> -> print ( <Expression> );")
    if token_list[number][1] == 'print':
        number = number + 1
        if token_list[number][1] == '(':
            number = number + 1
            if Expression(number):
                if token_list[number][1] == ')':
                    number = number + 1
                    if token_list[number][1] == ';':
                        number = number + 1
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def Scan(number):
    print(number)
    if switch == True:
        print("<Scan> -> scan ( <IDs> );")
    if token_list[number][1] == 'scan':
        if token_list[number][1] == '(':
            number = number + 1
            if IDs(number):
                if token_list[number][1] == ')':
                    number = number + 1
                    if token_list[number][1] == ';':
                        number = number + 1
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def While(number):
    print(number)
    if switch == True:
        print("while ( <Condition> ) <Statement> endwhile")
    if token_list[number][1] == 'while':
        number = number + 1
        if token_list[number][1] == '(':
            number = number + 1
            if CCondition(number):
                if token_list[number][1] == ')':
                    number = number + 1
                    if Statement(number):
                        if token_list[number][1] == 'endwhile':
                            number = number + 1
                            return True
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

def CCondition(number):
    print(number)
    if switch == True:
        print("<Condition> -> <Expression> <Relop> <Expression>")
    if Expression(number):
        if Relop(number):
            if Expression(number):
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def Relop(number):
    print(number)
    token = token_list[number][1]
    if switch == True:
        print("<Relop> -> == | != | > | < | <= | =>")
    if (token == '==' or token == '!=' or token == '>' or token == '<' or token == '<=' or token == '=>'):
        number = number + 1
        return True
    else:
        return False

def Expression(number):
    print(number)
    if switch == True:
        print("<Expression> -> <Term> <Expression>'")
    if Term(number):
        if Expression_Dash(number):
            return True
        else:
            return False
    else:
        return False

def Term(number):
    print(number)
    if switch == True:
        print("<Term> -> <Factor> <Term>'")
    if Factor(number):
        if Term_Dash(number):
            return True
        else:
            return False
    else:
        return False

# epsilon
def Expression_Dash(number):
    print(number)
    if switch == True:
        print("<Expression>' -> + <Term> <Expression>' | - <Term> <Expression>' | ϵ")
    if token_list[number][1] == '+':
        number = number + 1
        if Term(number):
            if Expression_Dash(number):
                return True
            else:
                return False
        else:
            return False
    elif token_list[number][1] == '-':
        number = number + 1
        if Term(number):
            if Expression_Dash(number):
                return True
            else:
                return False
        else:
            return False
    else:
        #return False
        return True

# epsilon
def Term_Dash(number):
    print(number)
    if switch == True:
        print("<Term>' -> * <Factor> <Term>' | / <Factor> <Term>' | ϵ")
    if token_list[number][1] == '*':
        number = number + 1
        if Factor(number):
            if Term_Dash(number):
                return True
            else:
                return False
        else:
            return False
    elif token_list[number][1] == '/':
        number = number + 1
        if Factor(number):
            if Term_Dash(number):
                return True
            else:
                return False
        else:
            return False
    else:
        #return False
        return True

def Factor(number):
    print(number)
    if switch == True:
        print("<Factor> -> - <Primary> | <Primary>")
    if token_list[number][1] == '-':
        number = number + 1
        if Primary(number):
            return True
        else:
            return False
    elif Primary(number):
        return True
    else:
        return False

def Primary(number):
    print(number)
    if switch == True:
        print("<Primary> -> <Identifier> | <Integer> | <Identifier> ( <IDs> ) | ( <Expression> ) | <Real> | true | false")
    if token_list[number][0] == 'id':
        number = number + 1
        return True
    elif token_list[number][0] == 'integer':
        number = number + 1
        return True
    elif token_list[number][0] == 'id':
        number = number + 1
        if token_list[number][1] == '(':
            number = number + 1
            if IDs(number):
                if token_list[number][2] == ')':
                    number = number + 1
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    elif token_list[number][1] == '(':
        number = number + 1
        if Expression(number):
            if token_list[number][1] == '(':
                number = number + 1
                return True
            else:
                return False
        else:
            return False
    elif token_list[number][1] == 'true':
        number = number + 1
        return True
    elif token_list[number][1] == 'false':
        number = number + 1
        return True
    else:
        return False

def EEmpty(number):
    print(number)
    if switch == True:
        print("<Empty> -> ϵ")
    return True

for token in lexical.tokenizer():
    for token2 in token:
        pair = lexical.lexer(token2)
        if not (pair[0] == 'invalid'):
            token_list.append(pair)
        else:
            warnings.warn("Invalid token! : " + pair[1])
            has_invalid = True

if has_invalid == True:
    print("\nCould not finish because of invalid token(s)!\n")
    exit()
else:
    Rat24S(number = 0)