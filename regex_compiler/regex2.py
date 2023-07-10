import sys; args = sys.argv[1:]
idx = int(args[0])-40

myRegexLst = [
  r"/^[xo.]{64}$/i", # 40
  r"/^[xo]*\.[xo]*$/i", # 41
  r"/^\.|\.$|^x+o*\.|\.o*x+$/i", # 42
  r"/^.(..)*$/s", # 43
  r"/^(0|(1[01]))([01]{2})*$/", # 44
  r"/\w*((a[eiou])|(e[aiou])|(i[aeou])|(o[aeiu])|(u[aeio]))\w*/i", # 45
  r"/^(0|10)*1?1?$|^1*$/", # 46
  r"/^[bc]*(a|[bc])[bc]*$/", # 47
  r"/^((([bc]*a){2})+|[bc])[bc]*$/", # 48
  r"/^(2|1([02]*1))(([02]*1){2})*[02]*$/", # 49
  ]

if idx < len(myRegexLst):
  print(myRegexLst[idx])

# Isabella Zhu, 2, 2023