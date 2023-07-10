# regex black option 1
# personal project: write a grammar check software using regex

from colorama import init, Back, Fore
init()

import sys, re

text_file = open(sys.argv[1], "r")
text = text_file.read()
text_file.close()
error_messages = []
d = {}

# special case: check for captalization at the start of the text (red)
exp = re.compile(r"^[a-z]\w*")
for result in exp.finditer(text):
    start, end = result.start(), result.end()
    substring = text[start : end]
    d[start] = (end, "red")
    error_messages.append("Error: \"%s\" should be capitalized." % substring)

# check for captalization at the start of a sentence (red)
exp = re.compile(r"[.?!]\s*\b[a-z]\w*")
for result in exp.finditer(text):
    start, end = result.start(), result.end()
    substring = text[start : end]
    word = substring[1 : ].strip()
    start = start + len(substring) - len(word)
    d[start] = (end, "red")
    error_messages.append("Error: \"%s\" should be capitalized." % word)

# apostrophe must be followed by s, re, ll, t, ve, d, nt (red)
exp = re.compile(r"\b\w*'(?!(s|re|ll|t|ve|d|nt)\b)\w*\b", re.I)
for result in exp.finditer(text):
    start, end = result.start(), result.end()
    word = text[start : end]
    d[start] = (end, "red")
    error_messages.append("Error: \"%s\" should not have an apostrophe." % word)

# missing apostrophe for common contractions (red)
exp = re.compile(r"\b(werent|cant|dont|shouldnt|havent|didnt|youre|arent|theyre)\b", re.I)
for result in exp.finditer(text):
    start, end = result.start(), result.end()
    word = text[start : end]
    d[start] = (end, "red")
    error_messages.append("Error: \"%s\" should have an apostrophe." % word)

# missing a quotation mark (red)
exp = re.compile(r"^.*\".*((\".*\".*){2})*.*$", re.S)
count = 0
for result in exp.finditer(text):
    count += 1
if count > 0:
    error_messages.append("Error: missing a quotation mark somewhere in text.")

# there should be a space after punctuation
exp = re.compile(r"\b\w+\b(?=[.?!,][^ \n\t])")
for result in exp.finditer(text):
    start, end = result.start(), result.end()
    word = text[start : end]
    d[start] = (end, "red")
    error_messages.append("Error: space missing after punctuation after \"%s\"" % word)

# punctuation with quotation marks (punctuation is usually inside the quotation) (yellow)
exp = re.compile(r"\b\w+\b(?=\"[!?,.])")
for result in exp.finditer(text):
    start, end = result.start(), result.end()
    word = text[start : end]
    d[start] = (end, "yellow")
    error_messages.append("Warning: Punctuation should be inside the quotation mark after \"%s\"." % word)

# capitalization (yellow)
exp = re.compile(r"(?<=\w)\s+[A-Z]\w*\b")
for result in exp.finditer(text):
    start, end = result.start(), result.end()
    substring = text[start : end]
    word = substring.strip()
    start = start + len(substring) - len(word)
    d[start] = (end, "yellow")
    error_messages.append("Warning: \"%s\" should not be capitalized unless it is a proper noun or pronoun." % word)

output = ""
i = 0
while i < len(text):
    if i in d:
        end, color = d[i]
        if color == "red":
            output += Back.RED + text[i : end] + Back.RESET
        elif color == "yellow":
            output += Back.LIGHTYELLOW_EX + text[i : end] + Back.RESET
        i = end
    else:
        output += text[i]
        i += 1

print(output)
print()
print("Here are the grammar mistakes found:")
print()
for message in error_messages:
    print(message)
