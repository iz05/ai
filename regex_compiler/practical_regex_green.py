from colorama import init, Back, Fore  # Note I have imported specific things here
init()
import sys, re

def regex(expression):
    expression = expression[1 :]
    index = expression.find("/")
    reg = expression[: index] # actual expression itself
    flags = expression[index + 1 :]
    exp = None
    if len(flags) == 0:
        exp = re.compile(r"%s" % reg)
    else:
        flag = None
        for char in flags:
            temp_flag = None
            if char == "i":
                temp_flag = re.I
            elif char == "m":
                temp_flag = re.M
            elif char == "s":
                temp_flag = re.S
            else:
                print("Error, different type of flag not considered.")
            if flag == None:
                flag = temp_flag
            else:
                flag = flag | temp_flag
        exp = re.compile(r"%s" % reg, flag)

    ends = set()
    d = {}
    cur_color = 0
    for result in exp.finditer(s):
        print(result)
        start = result.start()
        end = result.end()
        ends.add(end)
        if start in ends:
            cur_color = 1 - cur_color
        d[start] = (end, cur_color)
    
    i = 0
    text = ""
    while i < len(s):
        if i in d:
            end, color = d[i]
            if color == 0:
                text += Back.LIGHTYELLOW_EX + s[i : end] + Back.RESET
            else:
                text += Back.LIGHTCYAN_EX + s[i : end] + Back.RESET
            i = end
        else:
            text += s[i]
            i += 1
    
    print(text)

        

s = "This hello aeiou calculate physics physic"
regex(sys.argv[1])