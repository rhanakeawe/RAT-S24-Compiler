import re
import warnings
from tabulate import tabulate

# Defining table and regex
myTable = []
reg_key = r"(function)|(while)|(endwhile)|(if)|(endif)|(else)|(integer)|(boolean)|(real)|(assign)|(compound)|(return)|(print)|(scan)|(true)|(false)"
reg_op = r"==|!=|<=|=>|\+|\-|/|=|<|>"
reg_sep = r'[(]|[)]|[{]|[}]|[,]|[;]|[$]'
reg_int = r'-?[0-9]+'
reg_real = r'-?[0-9]+.[0-9]+'
reg_illegal = r"(^[0-9]|_)+([a-z]|[A-Z])"

# Sorting function
def sorter(input):
    if re.match(reg_key,input) != None:
        myTable.append(["keyword",input])
    elif (re.match(reg_illegal,input)):
        warnings.warn('Illegal!! -> ' + input)
        myTable.append(["illegal",input])
    elif re.match(reg_op,input) != None:
        if re.match(reg_int,input) == None:
            myTable.append(["operator",input])
        else:
            if re.match(reg_real,input):
                myTable.append(["real",input])
            else:
                myTable.append(["int",input])
    elif re.match(reg_int,input) != None:
        if re.match(reg_real,input):
            myTable.append(["real",input])
        else:
            myTable.append(["int",input])
    else:
        myTable.append(["identifier",input])

# Copying from file to string
lines = ""
with open('./test.txt','r') as input_file:
    for line in input_file:
        lines += line
input_file.close()

# Removing Comments
pre_list = (re.sub(r"\[.*?]","",lines, flags=(re.DOTALL|re.MULTILINE))).split("\n")
clean_text = "".join(pre_list)
list_text = clean_text.split()

# Unsticking Separators and sorting
for word in list_text:
    if re.search(reg_sep,word) != None:
        x = list(filter(None,re.split(r'('+reg_sep+'+)',word)))
        for token in x:
            if re.search(reg_sep,token) != None:
                myTable.append(["separator",token])
            else:
                sorter(token)
    else:
        sorter(word)

# Writing table to output file
output_name = re.sub(r'./',"",input_file.name)
output_name = re.sub(r'.txt',"_table.txt",output_name)
col_names = ["Token","Lexeme"]
with open(output_name,'w') as output_file:
    output_file.write(tabulate(myTable,headers=col_names,tablefmt="grid"))
output_file.close()
print(tabulate(myTable,headers=col_names,tablefmt="grid"))