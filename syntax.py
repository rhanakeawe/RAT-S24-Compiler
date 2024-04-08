import warnings
import lexical_3 as lexical
import sys

token_list = []

#has_invalid = False
switch = True

def Rat24S():
    if switch == True:
        print("<Rat24S> -> $ <Opt Function Definitions> $ <Opt Declaration List> $ <Statement List> $")
    if token_list[0] == '$':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Opt_Function_Def()
        if token_list[0] == '$':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)
            Opt_Declaration_List()
            if token_list[0] == '$':
                print(lexical.lexer(token_list[0]))
                token_list.pop(0)
                Statement_List()
                if token_list[0] == '$':
                    print(lexical.lexer(token_list[0]))
                    token_list.pop(0)
                    print("success")
                else:
                    print ("failed at fourth dollar")
            else:
                print ("failed at third dollar")
        else:
            print ("failed at second dollar")
    else:
        print ("failed at first dollar")
                            

def Opt_Function_Def():
    if switch == True:
        print("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
    if Function_Def():
        return
    elif EEmpty():
        return

            
def Function_Def():
    if switch == True:
        print("<Function Definitions> -> <Function> <Function Definitions>'")
    FFunction()
    Function_Def_Dash()


# epsilon
def Function_Def_Dash():
    if switch == True:
        print("<Function Definitions>' -> <Function Definitions> | ϵ")
    if Function_Def():
        return True
    else:
        return True


def FFunction():
    if switch == True:
        print("<Function> -> function <Identifier> ( <Opt Parameter List> ) <Opt Declaration List> <Body>")
    if token_list[0] == 'function':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        if (lexical.lexer(token_list[0])[0] == 'id'):
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)
            if (token_list[0]) == '(':
                print(lexical.lexer(token_list[0]))
                token_list.pop(0)
                Opt_Parameter_List()
                if token_list[0] == ')':
                    print(lexical.lexer(token_list[0]))
                    token_list.pop(0)
                    Opt_Declaration_List()
                    Body()


def Opt_Parameter_List():
    if switch == True:
        print("<Opt Parameter List> -> <Parameter List> | <Empty>")
    if Parameter_List():
        return
    elif EEmpty():
        return


def Parameter_List():
    if switch == True:
        print("<Parameter List> -> <Parameter> <Parameter List>'")
    PParameter()
    Parameter_List_Dash()


def PParameter():
    if switch == True:
        print("<Parameter> -> <IDs> <Qualifier>")
    IDs()
    Qualifier()


# epsilon
def Parameter_List_Dash():
    if switch == True:
        print("<Parameter List>' -> , <Parameter List> | ϵ")
    if token_list[0] == ',':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Parameter_List()
    else:
        return True


def Qualifier():
    if switch == True:
        print("<Qualifier> -> integer | boolean | real")
    if token_list[0] == 'integer' or token_list[0] == 'real' or token_list[0] == 'boolean':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)


def Body():
    if switch == True:
        print("<Body> -> { <Statement List> }")
    if token_list[0] == '{':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Statement_List()
        if token_list[0] == '}':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)


def Opt_Declaration_List():
    if switch == True:
        print("<Opt Declaration List> -> <Declaration List> | <Empty>")
    if Declaration_List():
        return True
    elif EEmpty():
        return True


def Declaration_List():
    if switch == True:
        print("<Declaration List> -> <Declaration>; <Declaration List>'")
    Declaration()
    if token_list[0] == ';':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Declaration_List_Dash()


# epsilon
def Declaration_List_Dash():
    if switch == True:
        print("<Declaration List>' -> <Declaration List> | ϵ")
    if Declaration_List():
        return True
    else:
        return True


def Declaration():
    if switch == True:
        print("<Declaration> -> <Qualifier> <IDs>")
    Qualifier()
    IDs()


def IDs():
    if switch == True:
        print("<IDs> -> <Identifier> <IDs>'")
    if lexical.lexer(token_list[0])[0] == 'id':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        IDs_Dash()


# epsilon
def IDs_Dash():
    if switch == True:
        print("<IDs>' -> , <IDs> | ϵ")
    if token_list[0] == ',':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        IDs()
    else:
        return True


def Statement_List():
    if switch == True:
        print("<Statement List> -> <Statement> <Statement List>'")
    Statement()
    Statement_List_Dash()


# epsilon
def Statement_List_Dash():
    if switch == True:
        print("<Statement List>' -> <Statement List> | ϵ")
    if Statement_List():
        return True
    else:
        return True


def Statement():
    if switch == True:
        print("<Statement> -> <Compound> | <Assign> | <If> | <Return> | <Print> | <Scan> | <While>")
    if Compound():
        return
    elif Assign():
        return
    elif IIf():
        return
    elif RReturn():
        return
    elif PPrint():
        return
    elif Scan():
        return
    elif While():
        return


def Compound():
    if switch == True:
        print("<Compound> -> { <Statement List> }")
    if token_list[0] == '{':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Statement_List()
        if token_list[0] == '}':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)


def Assign():
    if switch == True:
        print("<Assign> -> <Identifier> = <Expression> ;")
    if lexical.lexer(token_list[0])[0] == 'id':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        if token_list[0] == '=':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)
            Expression()
            if token_list[0] == ';':
                print(lexical.lexer(token_list[0]))
                token_list.pop(0)


def IIf():
    if switch == True:
        print("<If> -> if ( <Condition> ) <Statement> <If>'")
    if token_list[0] == 'if':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        if token_list[0] == '(':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)
            CCondition()
            if token_list[0] == ')':
                print(lexical.lexer(token_list[0]))
                token_list.pop(0)
                Statement()
                IIf_Dash()
        
def IIf_Dash():
    if switch == True:
        print("<If>' -> endif | else <Statement> endif")
    if token_list[0] == 'endif':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
    elif token_list[0] == 'else':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Statement()
        if token_list[0] == 'endif':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)

def RReturn():
    if switch == True:
        print("<Return> -> return <Return>'")
    if token_list[0] == 'return':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        RReturn_Dash()


def RReturn_Dash():
    if switch == True:
        print("<Return>' -> ; | <Expression> ;")
    if token_list[0] == ';':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
    elif Expression():
        if token_list[0] == ';':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)


def PPrint():
    if switch == True:
        print("<Print> -> print ( <Expression> );")
    if token_list[0] == 'print':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        if token_list[0] == '(':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)
            Expression()
            if token_list[0] == ')':
                print(lexical.lexer(token_list[0]))
                token_list.pop(0)
                if token_list[0] == ';':
                    print(lexical.lexer(token_list[0]))
                    token_list.pop(0)


def Scan():
    if switch == True:
        print("<Scan> -> scan ( <IDs> );")
    if token_list[0] == 'scan':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        if token_list[0] == '(':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)
            IDs()
            if token_list[0] == ')':
                print(lexical.lexer(token_list[0]))
                token_list.pop(0)
                if token_list[0] == ';':
                    print(lexical.lexer(token_list[0]))
                    token_list.pop(0)


def While():
    if switch == True:
        print("<While> -> while ( <Condition> ) <Statement> endwhile")
    if token_list[0] == 'while':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        if token_list[0] == '(':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)
            CCondition()
            if token_list[0] == ')':
                print(lexical.lexer(token_list[0]))
                token_list.pop(0)
                Statement()
                if token_list[0] == 'endwhile':
                    print(lexical.lexer(token_list[0]))
                    token_list.pop(0)


def CCondition():
    if switch == True:
        print("<Condition> -> <Expression> <Relop> <Expression>")
    Expression()
    Relop()
    Expression()


def Relop():
    if switch == True:
        print("<Relop> -> == | != | > | < | <= | =>")
    if token_list[0] == '==' or token_list[0] == '!=' or token_list[0] == '>' or token_list[0] == '<' or token_list[0] == '<=' or token_list[0] == '=>':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)


def Expression():
    if switch == True:
        print("<Expression> -> <Term> <Expression>'")
    Term()
    Expression_Dash()


def Term():
    if switch == True:
        print("<Term> -> <Factor> <Term>'")
    Factor()
    Term_Dash()


# epsilon
def Expression_Dash():
    if switch == True:
        print("<Expression>' -> + <Term> <Expression>' | - <Term> <Expression>' | ϵ")
    if token_list[0] == '+':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Term()
        Expression_Dash()
    elif token_list[0] == '-':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Term()
        Expression_Dash()
    else:
        return True


# epsilon
def Term_Dash():
    if switch == True:
        print("<Term>' -> * <Factor> <Term>' | / <Factor> <Term>' | ϵ")
    if token_list[0] == '*':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Factor()
        Term_Dash()
    elif token_list[0] == '/':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Factor()
        Term_Dash()
    else:
        return True


def Factor():
    if switch == True:
        print("<Factor> -> - <Primary> | <Primary>")
    if token_list[0] == '-':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Primary()
        return
    elif Primary():
        return


def Primary():
    if switch == True:
        print("<Primary> -> <Identifier> <Primary>' | <Integer> | ( <Expression> ) | <Real> | true | false")
    if lexical.lexer(token_list[0])[0] == 'id':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Primary_Dash()
    elif lexical.lexer(token_list[0])[0] == 'integer':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
    elif token_list[0] == '(':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        Expression()
        if token_list[0] == ')':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)
    elif lexical.lexer(token_list[0])[0] == 'real':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
    elif token_list[0] == 'true':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
    elif token_list[0] == 'false':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)

# epsilon
def Primary_Dash():
    if switch == True:
        print("<Primary>' -> ( <IDs> ) | ϵ")
    if token_list[0] == '(':
        print(lexical.lexer(token_list[0]))
        token_list.pop(0)
        IDs()
        if token_list[0] == ')':
            print(lexical.lexer(token_list[0]))
            token_list.pop(0)
    else:
        return True
        


def EEmpty():
    if switch == True:
        print("<Empty> -> ϵ")
    return True


""" for token in lexical.tokenizer():
    for token2 in token:
        pair = lexical.lexer(token2)
        if not (pair[0] == 'invalid'):
            token_list.append(pair)
        else:
            warnings.warn("Invalid token! : " + pair[1])
            has_invalid = True """

""" if has_invalid == True:
    print("\nCould not finish because of invalid token(s)!\n")
    exit() """

for token in lexical.tokenizer():
    for token2 in token:
        token_list.append(token2)
Rat24S()