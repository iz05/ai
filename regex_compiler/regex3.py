import sys; args = sys.argv[1:]
idx = int(args[0])-50

myRegexLst = [
  r"/\b\w*(\w)\w*\1\w*\b/i", # 50
  r"/\b\w*(\w)(\w*\1){3}\w*\b/i", # 51
  r"/^([01])([01]*\1|)$/", # 52
  r"/\b(?=\w*cat)\w{6}\b/i", # 53
  r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i", # 54
  r"/\b(?!\w*cat)\w{6}\b/i", # 55
  r"/\b(?!\w*(\w)\w*\1)\w+\b/i", # 56
  r"/^(?![01]*10011)[01]*$/", # 57
  r"/\b\w*([aeiou])(?!\1)[aeiou]\w*\b/i", # 58
  r"/^(?!.*1[01]1)[01]*$/", # 59
  ] # 225

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Isabella Zhu, 2, 2023