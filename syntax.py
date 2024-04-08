import lexical_3 as lexical
import sys

token_list = []

lexer_list = []

#has_invalid = False
switch = True
error_message_toggle = True

def Missing_Message(func_name, failure):
    if error_message_toggle == True:
        s = func_name + ": no " + failure + " | Token at: " + token_list[0]
        print(s)


def SyntaxLogger(syntax):
    if switch == True:
        print(syntax)


def Terminate_Lexer():
    print(lexical.lexer(token_list[0]))
    lexer_list.append(lexical.lexer(token_list[0]))
    token_list.pop(0)


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
                            

def Opt_Function_Def():
    SyntaxLogger("<Opt Function Definitions> -> <Function Definitions> | <Empty>")
    if Function_Def():
        return True
    elif EEmpty():
        return True
    else:
        Missing_Message("Opt_Function_Def","Function_Def or EEmpty")

            
def Function_Def():
    SyntaxLogger("<Function Definitions> -> <Function> <Function Definitions>'")
    if FFunction():
        if Function_Def_Dash():
            return True
        else:
            Missing_Message("Function_Def","Function_Def_Dash")
    else:
        Missing_Message("Function_Def","FFunction")


# epsilon
def Function_Def_Dash():
    SyntaxLogger("<Function Definitions>' -> <Function Definitions> | ϵ")
    if Function_Def():
        return True
    else:
        return True


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


def Opt_Parameter_List():
    SyntaxLogger("<Opt Parameter List> -> <Parameter List> | <Empty>")
    if Parameter_List():
        return True
    elif EEmpty():
        return True


def Parameter_List():
    SyntaxLogger("<Parameter List> -> <Parameter> <Parameter List>'")
    if PParameter():
        if Parameter_List_Dash():
            return True
        else:
            Missing_Message("Parameter_List","Parameter_List_Dash")
    else:
        Missing_Message("Parameter_List","PParameter")


def PParameter():
    SyntaxLogger("<Parameter> -> <IDs> <Qualifier>")
    if IDs():
        if Qualifier():
            return True
        else:
            Missing_Message("PParameter","Qualifier")
    else:
        Missing_Message("PParameter","IDs")


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


def Qualifier():
    SyntaxLogger("<Qualifier> -> integer | boolean | real")
    if token_list[0] == 'integer' or token_list[0] == 'real' or token_list[0] == 'boolean':
        Terminate_Lexer()
        return True
    else:
        Missing_Message("Qualifier", "integer or real or boolean")


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
        Terminate_Lexer()
        if token_list[0] == '=':
            Terminate_Lexer()
            if Expression():
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
        Terminate_Lexer()
        if token_list[0] == '(':
            Terminate_Lexer()
            if CCondition():
                if token_list[0] == ')':
                    Terminate_Lexer()
                    if Statement():
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


def CCondition():
    SyntaxLogger("<Condition> -> <Expression> <Relop> <Expression>")
    if Expression():
        if Relop():
            if Expression():
                return True
            else:
                Missing_Message("CCondition","Expression 2")
        else:
            Missing_Message("CCondition","Relop")
    else:
        Missing_Message("CCondition","Expression 1")


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
            if Term_Dash():
                return True
            else:
                Missing_Message("Term_Dash", "Term_Dash 1")
        else:
            Missing_Message("Term_Dash", "Factor 1")
    elif token_list[0] == '/':
        Terminate_Lexer()
        if Factor():
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
        Terminate_Lexer()
        if Primary_Dash():
            return True
    elif lexical.lexer(token_list[0])[0] == 'integer':
        Terminate_Lexer()
        return True
    elif token_list[0] == '(':
        Terminate_Lexer()
        if Expression():
            if token_list[0] == ')':
                Terminate_Lexer()
                return True
    elif lexical.lexer(token_list[0])[0] == 'real':
        Terminate_Lexer()
        return True
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