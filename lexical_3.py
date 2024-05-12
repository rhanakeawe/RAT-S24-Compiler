import sys
import warnings

keyword = ["function","while","endwhile","if","endif","else","integer","boolean","real","return","print","scan","true","false"]
operators = ["==","!=","<=","=>","+","-","/","=","<",">","*"]
seperators = ["(",")","{","}",",",";","$"]

# The Lexical Analyzer
def lexer(token):
    if token[0].isalpha():
        output = id_state(token)
    elif token[0].isdigit():
        output = num_state(token)
    elif token.startswith("-") and any(chr.isdigit() for chr in token):
        output = num_state(token)
    elif any(token == sep2 for sep2 in seperators):
        output = ["separator",token]
    elif any(token == op for op in operators):
        output = ["operator",token]
    else:
        output = ["invalid",token]
        warnings.warn("Invalid token! : " + token)
    return output

# Identifier Check
def id_state(token):
    if any(token == key for key in keyword):
        output = ["keyword",token]
    elif all(char3.isalnum() for char3 in token) and len(token) > 1:
        output = ["id",token]
    else:
        for char4 in token:
            invalid = False
            if char4.isalnum() or char4 == '_':
                invalid = False
            else:
                invalid = True
                break
        if invalid == False and len(token) > 0:
            output = ["id",token]
        else:
            output = ["invalid",token]
            warnings.warn("Invalid token! : " + token)
    return output

# Real or Integer Check
def num_state(token):
    multinum = False
    num_list = [token.split('.')]
    for num in num_list:
        while("" in num):
            num.remove("")
        if (len(num) < 2):
            multinum = True
    try: 
        float(token) 
        res1 = True
    except:
        res1 = False
    try: 
        int(token) 
        res2 = True
    except:
        res2 = False
    if (res1 == True) and (multinum == False):
        output = ["real",token]
    elif (res1 == True) and (multinum == True):
        if (res2 == True):
            output = ["integer",token]
        else:
            output = ["invalid",token]
            warnings.warn("Invalid token! : " + token)
    else:
        output = ["invalid",token]
        warnings.warn("Invalid token! : " + token)
    return output

# The Tokenizer
def tokenizer():
    lines = ""
    with open(str(sys.argv[1]),'r', encoding="utf-8") as input_file:
        for x in input_file:
            lines += x
    input_file.close()

    # Removing Comments
    split_lines = lines.split()
    i = 0
    range_start = None
    range_end = None
    for line in split_lines:
        if line == "[*":
            range_start = i
        if line == "*]":
            range_end = i
        if range_end != None and range_start != None:
            del split_lines[range_start:range_end+1]
            range_start = None
            range_end = None
        i += 1

    # Unstick Separators
    unstuck_list = []
    for token1 in split_lines:
        temp_list = []
        j = 0
        range_start = None
        range_end = None
        for char1 in token1:
            if not [sep for sep in seperators if(sep in char1)]:
                if range_start == None:
                    range_start = j
                else:
                    range_end = j+1
            temp_list.append(char1)
            j += 1
        k = 0
        temp_list[range_start:range_end] = [''.join(temp_list[range_start:range_end])]
        for token2 in temp_list:
            if any(sept in token2 for sept in seperators) and len(token2) > 1:
                for char2 in token2:
                    temp_list.append(char2)
                del temp_list[k]
            k += 1
        unstuck_list.append(temp_list)
    return unstuck_list