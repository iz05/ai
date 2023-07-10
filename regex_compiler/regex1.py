import sys; args = sys.argv[1:]
idx = int(args[0])-30

myRegexLst = [
  r"/^0$|^100$|^101$/", # 30
  r"/^[01]*$/", # 31
  r"/[01]*0$/", # 32
  r"/\w*[aeiou]\w*[aeiou]\w*/i", # 33
  r"/^1[01]*0$|^0$/", # 34
  r"/^[01]*110[01]*$/", # 35
  r"/^.{2,4}$/s", # 36
  r"/^\d{3} *-? *\d{2} *-? *\d{4}$/", # 37
  r"/^.*?d\w*/im", # 38
  r"/^0[01]*0$|^1[01]*1$|^[01]?$/", # 39
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Isabella Zhu, 2, 2023