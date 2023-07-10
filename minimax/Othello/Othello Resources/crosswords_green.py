import sys; args = sys.argv[1:]

#____inputs_______________
#dictionary = sys.argv[1] #python.exe crosswords_green.py dict.txt 13x10 32 ceher
# hxw = args[0]
# num_blocked = int(args[1])
# seedstrings= args[2:]
hxw = sys.argv[2]
num_blocked = int(sys.argv[3])
seedstrings= sys.argv[4:]


#set up board + dimensiosn
dimensions = hxw.split("x")
nrows = int(dimensions[0])
ncols = int(dimensions[1])
board= []
for i in range(nrows):
    board.append(["-"]*ncols)

def place_v(word, b):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    #extracting
    board = b.copy()
    row = ""
    for i in word:
        if i not in alphabet:
            row += i
        else:
            break
    word = word[len(row)+1:]
    row = int(row)
    col = ""
    for i in word:
        if i not in alphabet:
            col+=i
        else:
            break
    word = word[len(col):] #the character is left
    col = int(col)
    r= row
    chara = list(word)
    while len(chara) > 0:
        board[r][col] = chara[0]
        chara.remove(chara[0])
        r+=1
    return board

def place_h(word, b):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    #extracting
    board = b.copy()
    row = ""
    for i in word:
        if i not in alphabet:
            row += i
        else:
            break
    word = word[len(row)+1:]
    row = int(row)
    col = ""
    for i in word:
        if i not in alphabet:
            col+=i
        else:
            break
    word = word[len(col):] #the character is left
    col = int(col)
    c=col
    chara = list(word)
    while len(chara) > 0:
        board[row][c] = chara[0]
        chara.remove(chara[0])
        c+=1
    return board
def display(board):
    for i in range(len(board)):
        print(board[i])
#place the seed strings
for i in range(len(seedstrings)):
    word = seedstrings[i]
    if word[:1] == "V": #vertical orientation
        board = place_v(word[1:], board)
    else: #hori
        board = place_h(word[1:], board)

def place_blocks(num_blocks, board):
    global ncols, nrows
    if num_blocks == ncols * nrows:
        for i in range(len(board)):
            board[i] = ["#"] * ncols
    else:
        for i in range(1, len(board)-1):
            if num_blocks <0: 
                    return 
            for j in range(len(board[i])//2):
                if num_blocks <0: 
                    return 
                if board[i][j] !="-":
                    pass
           #     elif (board[i+1][j] and board[i-1][j] !="-") and (board[i][j-1] and board[i][j+1] != "-"):
             #       pass
              #  elif board[i].count("#") == len(board[i]):
              #      pass
                else:
                    if num_blocks <0: 
                        return 
                    board[i][j] = "#"
                    board[nrows-1-i][ncols-1-j] = "#"
                    num_blocks-=2

# place_blocks(num_blocked, board)
# print(board)


#Elina Liu, 1, 2023