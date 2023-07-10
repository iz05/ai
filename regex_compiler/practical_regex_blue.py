import sys, re

# open text file in read mode
text_file = open(sys.argv[1], "r")
text = text_file.read()
text = text.lower()
text_file.close()
words = text.split()
 
# problem 1
print("#1: re.compile(r\"^(?=\\w*?a)(?=\\w*?e)(?=\\w*?i)(?=\\w*?o)(?=\\w*?u)[a-zA-Z]+$\")")
exp = re.compile(r"^(?=\w*?a)(?=\w*?e)(?=\w*?i)(?=\w*?o)(?=\w*?u)[a-zA-Z]+$")
results = []
for word in words:
    for result in exp.finditer(word):
        results.append(word[result.start() : result.end() + 1])
results = sorted(results, key = lambda x : len(x))
for i in range(0, len(results)):
    if len(results[i]) != len(results[0]):
        results = results[ : i]
        break
print("%s total matches" % len(results))
for i in range(0, min(len(results), 5)):
    print(results[i])
print()

# problem 2
print("#2: re.compile(r\"^([^aeiou]*[aeiou]){5}[^aeiou]*$\")")
exp = re.compile(r"^([^aeiou]*[aeiou]){5}[^aeiou]*$")
results = []
for word in words:
    for result in exp.finditer(word):
        results.append(word[result.start() : result.end() + 1])
results = sorted(results, key = lambda x : -1 * len(x))
for i in range(0, len(results)):
    if len(results[i]) != len(results[0]):
        results = results[ : i]
        break
print("%s total matches" % len(results))
for i in range(0, min(len(results), 5)):
    print(results[i])
print()

# problem 3, skip for now
print("#3: re.compile(r\"^(\\w)(?!\\w*\\1\\w*\\1)\\w*\\1$\")")
exp = re.compile(r"^(\w)(?!\w*\1\w*\1)\w*\1$")
results = []
for word in words:
    for result in exp.finditer(word):
        results.append(word[result.start() : result.end() + 1])
results = sorted(results, key = lambda x : -1 * len(x))
for i in range(0, len(results)):
    if len(results[i]) != len(results[0]):
        results = results[ : i]
        break
print("%s total matches" % len(results))
for i in range(0, min(len(results), 5)):
    print(results[i])
print()

# problem 4
print("#4: re.compile(r\"^(.).\\1$|^(.)(.).?\\3\\2$|^(.)(.)(.).*\\6\\5\\4*$\")")
exp = re.compile(r"^(.).\1$|^(.)(.).?\3\2$|^(.)(.)(.).*\6\5\4$")
results = []
for word in words:
    for result in exp.finditer(word):
        results.append(word[result.start() : result.end() + 1])
print("%s total matches" % len(results))
for i in range(0, min(len(results), 5)):
    print(results[i])
print()

# problem 5
print("#5: re.compile(r\"^([^aeiou]*[aeiou]){5}[^aeiou]*$\")")
exp = re.compile(r"^[^bt]*(bt|tb)[^bt]*$")
results = []
for word in words:
    for result in exp.finditer(word):
        results.append(word[result.start() : result.end() + 1])
print("%s total matches" % len(results))
for i in range(0, min(len(results), 5)):
    print(results[i])
print()

# problem 6
print("#6: re.compile(r\"^.*(.)\\1{%s}.*$\" % str(num - 1))")
num = 1
max_results = []
while(True):
    exp = re.compile(r"^.*(.)\1{%s}.*$" % str(num - 1))
    results = []
    for word in words:
        for result in exp.finditer(word):
            results.append(word[result.start() : result.end() + 1])
    if len(results) == 0:
        break
    max_results = results
    num += 1
print("%s total matches" % len(max_results))
for i in range(0, min(len(max_results), 5)):
        print(max_results[i])
print()

# problem 7
print("#7: re.compile(r\"^.*(.)(.*\1){%s}.*$\" % str(num - 1))")
num = 1
max_results = []
while(True):
    exp = re.compile(r"^.*(.)(.*\1){%s}.*$" % str(num - 1))
    results = []
    for word in words:
        for result in exp.finditer(word):
            results.append(word[result.start() : result.end() + 1])
    if len(results) == 0:
        break
    max_results = results
    num += 1
print("%s total matches" % len(max_results))
for i in range(0, min(len(max_results), 5)):
        print(max_results[i])
print()

# problem 8
print("#8: re.compile(r\"^.*(.)(.*\\1){%s}.*$\" % str(num - 1))")
num = 1
max_results = []
while(True):
    exp = re.compile(r"^.*(.)(.)(.*\1\2){%s}.*$" % str(num - 1))
    results = []
    for word in words:
        for result in exp.finditer(word):
            results.append(word[result.start() : result.end() + 1])
    if len(results) == 0:
        break
    max_results = results
    num += 1
print("%s total matches" % len(max_results))
for i in range(0, min(len(max_results), 5)):
        print(max_results[i])
print()

# problem 9
print("#9: re.compile(r\"^(.*[bcdfghjklmnpqrstvwxyz]){%s}.*$\" % str(num - 1))")
num = 1
max_results = []
while(True):
    exp = re.compile(r"^(.*[bcdfghjklmnpqrstvwxyz]){%s}.*$" % str(num - 1))
    results = []
    for word in words:
        for result in exp.finditer(word):
            results.append(word[result.start() : result.end() + 1])
    if len(results) == 0:
        break
    max_results = results
    num += 1
print("%s total matches" % len(max_results))
for i in range(0, min(len(max_results), 5)):
        print(max_results[i])
print()

# problem 10
print("#10: re.compile(r\"^(?!.*(.).*\\1.*\\1).*$\")")
exp = re.compile(r"^(?!.*(.).*\1.*\1).*$")
results = []
for word in words:
    for result in exp.finditer(word):
        results.append(word[result.start() : result.end() + 1])
results = sorted(results, key = lambda x : -1 * len(x))
for i in range(0, len(results)):
    if len(results[i]) != len(results[0]):
        results = results[ : i]
        break
print("%s total matches" % len(results))
for i in range(0, min(len(results), 5)):
    print(results[i])
print()