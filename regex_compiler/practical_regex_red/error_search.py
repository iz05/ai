import sys, re

text_file = open("error_example.py", "r")
text = text_file.read()
text = text.lower()
text_file.close()
lines = text.split("\n")
for i in range(0, len(lines)):
    if lines[i].find("#") != -1:
        lines[i] = lines[i][:lines[i].find("#")]

# error type 1: variables can't begin with digits
nums = []
for i in range(0, len(lines)):
    line = lines[i]
    exp = re.compile(r"\b\d\w*[a-zA-Z_]\w*\b") # to differentiate between variables and numbers
    count = 0
    for result in exp.finditer(line):
        if not line[result.start() : result.end() + 1].isdecimal():
            count += 1
    if count >= 1:
        nums.append(i + 1)
print("Variable name starts with a digit on lines %s." % str(nums)[1:-1])

# error type 2: using = instead of ==
nums = []
for i in range(0, len(lines)):
    line = lines[i]
    exp = re.compile(r"(if|elif|return)[^=]*=[^=]") 
    count = 0
    for result in exp.finditer(line):
        count += 1
    if count >= 1:
        nums.append(i + 1)
print("Used = instead of == on lines %s." % str(nums)[1:-1])

nums = []
# error type 3: using == instead of =
for i in range(0, len(lines)):
    line = lines[i]
    exp = re.compile(r"^(?!.*\bif\b)(?!.*\breturn\b)(?!.*\belif\b).*==.*$") # == can only appear with if, elif, or return
    count = 0
    for result in exp.finditer(line):
        count += 1
    if count >= 1:
        nums.append(i + 1)
print("Used == instead of = on lines %s." % str(nums)[1:-1])

nums = []
# error type 4: lacking a colon
for i in range(0, len(lines)):
    line = lines[i]
    exp = re.compile(r"^(?=.*(def|if|elif|else|for|while))[^:]*$") # : appears after def, if, elif, else, for, while
    count = 0
    for result in exp.finditer(line):
        count += 1
    if count >= 1:
        nums.append(i + 1)
print("Missing colon on lines %s." % str(nums)[1:-1])

nums = []
# error type 5: undefined variables
cur_variables = set() # keeps track of current variables
for i in range(0, len(lines)):
    line = lines[i]
    exp = re.compile(r"\b\w*[a-zA-Z_]\w*\b(?=\s*=([^=]|^))") # test for assigned variables
    for result in exp.finditer(line):
        cur_variables.add(line[result.start() : result.end() + 1].strip())
    exp = re.compile(r"(?<=\()\w*[a-zA-Z_]\w*(?=\))|\b\w*[a-zA-Z_]\w*(?=\s*==)|\b\w*[a-zA-Z_]\w*\b(?=\.)") # isolate variables
    for result in exp.finditer(line):
        st = line[result.start() : result.end() + 1].strip()
        if st[-1] == "." or st[-1] == ")":
            st = st[:-1]
        if st != "true" and st != "false":
            if st not in cur_variables:
                nums.append(i + 1)
print("Undefined variable on lines %s." % str(nums)[1:-1])