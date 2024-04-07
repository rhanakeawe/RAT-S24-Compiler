import warnings
from tabulate import tabulate

myTable = []
keyword = ["function","while","endwhile","if","endif","else","integer","boolean","real","assign","compound","return","print","scan","true","false"]
operators = ["==","!=","<=","=>","+","-","/","=","<",">","*"]
seperators = ["(",")","{","}",",",";","$"]

def check_keyword(word):
    if any(word == key for key in keyword):
        myTable.append(["keyword",token3])
    elif word[0].isalpha():
        myTable.append(["id",word])

def check_number(number):
    if any(num.isdigit() for num in number):
        if any(chr == '.' for chr in number):
            myTable.append(["real",number])
        else:
            myTable.append(["integer",number])

def check_operator(oper):
    if any(oper == op for op in operators):
        myTable.append(["operator",oper])

# Copying from file to string
lines = ""
with open('./test_1.txt','r') as input_file:
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
# 9; ????
unstuck_list = []
for token1 in split_lines:
    temp_list = []
    j = 0
    range_start = None
    range_end = None
    for c in token1:
        if not [sep for sep in seperators if(sep in c)]:
            if range_start == None:
                range_start = j
            else:
                range_end = j+1
        temp_list.append(c)
        j += 1
    temp_list[range_start:range_end] = [''.join(temp_list[range_start:range_end])]
    unstuck_list.append(temp_list)
print(unstuck_list)

for token2 in unstuck_list:
    # print(token2)
    for token3 in token2:
        done2 = 0
        if any(token3 == sep2 for sep2 in seperators):
            myTable.append(["separator",token3])
            done2 = 1
        if done2 == 0:
            check_keyword(token3)
            check_number(token3)
            check_operator(token3)

col_names = ["Token","Lexeme"]
with open("table_test_1.txt",'w') as output_file:
    output_file.write(tabulate(myTable,headers=col_names,tablefmt="grid"))
output_file.close()