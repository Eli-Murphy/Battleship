import random
from random import randint
from time import sleep
from tqdm import tqdm
import os
import ast


def main():
    hidden_board = [["~"] * 10 for x in range(10)]
    guess_board = [["~"] * 10 for x in range(10)]
    player_board = [["~"] * 10 for x in range(10)]

    hidden_board = generateShips(hidden_board)


    print("Welcome to Battleship!\n")
    
    while True:

        pullBoard = input("Would you like to pull the saved board? (y/n): ")
        if pullBoard in "nN":

            print("Let's create your board!")

            showBoard(player_board)

            player_board = placeShips(player_board)

            while True:
                saveBoard = input("Would you like to save your board layout for future games? (y/n): ").lower()
                if saveBoard in "yY":
                    testSave = saveBoatLayout(player_board)
                    if testSave == "fail":
                        print("Sorry, no saved game board detected. ")
                        main()
                    else:
                        break
                elif saveBoard in "nN":
                    break
                else:
                    print("Please enter either y or n. ")
                    pass
        elif pullBoard in "Yy":
            testVal = pullBoatLayout()
            if testVal == "fail":
                print("Game save file pulled unsucsessfully. Try making your own board.")
                pass
            else:
                player_board = testVal
                break
        else:
            print("Please enter either y or n")
            pass

    clearTerm(100)
    print("Your Boats:")
    showBoard(player_board)
    print("\nHere is your view of the enemy's sea. Shoot to find their boats!\n")
    showBoard(guess_board)
    

    turn = "player"

    while True:
        while turn == "player":
            position = input("Please input shot position (A1): ")
            clearTerm(100)
            row, column = locationFormat(position)
            if guess_board[row][column] == "Ø":
                print("You already guessed that spot!")
                showBoard(guess_board)
            elif hidden_board[row][column] == "X":
                print("Congradulations! You hit an enemy boat!")
                guess_board[row][column] = "X"
                showBoard(guess_board)
                turn = "bot"
            else:
                print("\nSorry, you missed!")
                guess_board[row][column] = "Ø"
                showBoard(guess_board)
                turn = "bot"
            if hitShips(guess_board) == 17:
                print("You hit them all, good job!")
                showBoard(guess_board)
                break
        while turn == "bot":
            turnMade = False
            for i in tqdm(range(0, 20), unit =" ticks", desc ="The enemy is thinking..."):
                sleep(.1)
            while turnMade == False:
                clearTerm(100)
                row = randint(0,9)
                col = randint(0,9)
                if player_board[row][col] == "#":
                    player_board[row][col] = "X"
                    print("Your board: \n")
                    showBoard(player_board)
                    print("\nDamn! Your hit!\n")
                    print("Your enemy's board: ")
                    showBoard(guess_board)
                    turnMade = True
                    turn = "player"
                elif player_board[row][col] == "X":
                    pass
                elif player_board[row][col] == "~":
                    player_board[row][col] = "Ø"
                    print("Your sea: \n")
                    showBoard(player_board)
                    print("Your enemy's sea: \n")
                    showBoard(guess_board)
                    print("\nThe computer missed!\n")
                    turnMade = True
                    turn = "player"
                if hitShips(player_board) == 17:
                    print("All your ships have been sunk. Better luck next time!")
                    break

def showBoard(board):
    print("    A B C D E F G H I J")
    print("   ---------------------")

    rownumb = 1
    for r in board:
        if rownumb == 10:
            space = " "
        else:
            space = "  "
        print("%d|%s|" % (rownumb, space + "|".join(r)))
        rownumb += 1

def placeShips(board):
    shipSize = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2} #size of each ship
    shipList = [['Carrier', 1], ['Battleship', 1], ['Cruiser', 1], ['Submarine', 1], ['Destroyer', 1]]
    
    
    

    for x in shipList: #place ships
        r = 0

        while x[1] > 0: #check there's ships available
            r += 1
            shipType = x[0]
            ship_size = shipSize[x[0]]
            boatMade = False
            while boatMade == False:
                testValidity = shipDeploy(board, ship_size, shipType)
                if testValidity == None:
                    pass
                else:
                    x[1] -= 1
                    board = testValidity
                    boatMade = True
                
    return board
    
def shipDeploy(board, ship_size, type):
    print("Where would you like to put your", str(type) + ", the", str(ship_size), "long boat? (A1)")
    pos = input("Input here: ")
    row, column = locationFormat(pos)
    while True:
        try:
            angle = input("Place it up, down, left, or right? (u,d,l,r): ").upper()
            if angle not in "UDLR":
                print("Please enter either u, l, d, or r.")
            if angle in "UDLR":
                break
        except:
            print("Please enter either U, L, D, or R.")
            pass
    shipsMade = 0
    while shipsMade != 5:
        if angle == "U":
            colission = False
            buildCount = 0
            if 0 <= (row+1 + int(-1 * ship_size)) <= 9:
                for i in range(ship_size):
                    buildCount += 1
                    if board[int(row)-i][int(column)] == "#": 
                        colission = True
                        pass
            else:
                colission = True
            
            if colission is False:
                for k in range(buildCount):
                    board[int(row)-k][int(column)] = "#"
                clearTerm(100)
                showBoard(board)
        
        if angle == "D":
            colission = False
            buildCount = 0
            if row + int(ship_size) <= 9: #WORKS
                for i in range(ship_size):
                    buildCount += 1
                    if board[int(row)+i][int(column)] == "#": 
                        colission = True
                        pass
            else:
                colission = True
            if colission is False:
                for k in range(buildCount):
                    board[int(row)+k][int(column)] = "#"
                clearTerm(100)
                showBoard(board)
        
        if angle == "R":
            colission = False
            buildCount = 0
            if 0 <= (column-1 + int(ship_size)) <= 9: #WORKS
                for i in range(ship_size):
                    buildCount += 1
                    if board[int(row)][int(column)+i] == "#": 
                        colission = True
                        pass
        
            else:
                colission = True
            if colission is False:
                for k in range(buildCount):
                    board[int(row)][int(column)+k] = "#"
                clearTerm(100)
                showBoard(board)

        if angle == "L":
            colission = False
            buildCount = 0
            if column - int(ship_size) <= 9:
                for i in range(ship_size):
                    buildCount += 1
                    if board[int(row)][int(column)-i] == "#": 
                        colission = True
                        pass
        
            else:
                colission = True
            if colission is False:
                for k in range(buildCount):
                    board[int(row)][int(column)-k] = "#"
                clearTerm(100)
                showBoard(board)
        if colission:
            clearTerm(100)
            showBoard(board)
            print("Can't put a ship there.")
            return None
        else:
            return board

def locationFormat(hitcoord):
    alphaConvert = {'A': 0, 'B':1, 'C':2,'D':3,'E':4,"F":5,'G':6,'H':7, 'I':8, "J":9}
    colPass = False
    rowPass = False
    while True:
        if len(hitcoord) == 2 or len(hitcoord) == 3 and hitcoord[0] in "ABCDEFGHIJabcdefghij" and hitcoord[1] in "1234567890":
            column = hitcoord[0].upper()
            colPass = True
            if len(hitcoord) == 2:    
                row = int(hitcoord[1])
                rowPass = True
            else:
                row = int(str(hitcoord[1]) + str(hitcoord[2]))
                rowPass = True
            if row > 10:
                print("Please input a row between 1-10.")
                rowPass = False
        if colPass and rowPass:
            return int(row)-1, alphaConvert[column]
        else:
            print("Please input a coordinate (A-J1-10)")
            hitcoord = list(input("Please input hit coordinates (ex. A1): "))
                 
def hitShips(board):
    hits = 0
    for row in board:
        for column in row:
            if column == "X":
                hits += 1
    return hits

def generateShips(board):
    
    shipLen = [5,4,3,3,2]
    shipAvalible = 5
    directionposibilities = ["vertical", "horizontal"]   

    
    for i in range(shipAvalible):
        boatMade = False

        #REGULAR VAR STATMENTS
         

        #DEBUG VAR STATMENTS
        #col = 6
        #row = 3
        #direction = "horizontal"
        

        while boatMade == False:
            direction = random.choice(directionposibilities)   
            col = randint(0,9)
            row = randint(0,9)
   
            if direction == "vertical":
                buildCount = 0
                if row + int(shipLen[i]) <= 9: 
                    colission = False
                    for j in range(0, int(shipLen[i])):
                        buildCount += 1
                        if board[int(row+j)][int(col)] == "X": 
                            colission = True
                            pass
                    if not colission:
                        for k in range(buildCount):
                            board[int(row+k)][int(col)] = "X"
                        boatMade = True
                        shipAvalible = shipAvalible - 1
                
            if direction == "horizontal":
                if col + int(shipLen[i]) <= 9: #check ship within boundaries BROKEN
                    colission = False
                    buildCount = 0
                    for j in range(0, int(shipLen[i])):
                        buildCount += 1
                        if board[int(row)][int(col)+j] == "X":
                            colission = True
                            pass
                    if not colission:
                        for k in range(buildCount):
                            board[int(row)][int(col)+k] = "X"
                        boatMade = True
                        shipAvalible = shipAvalible - 1
                else:
                    col = randint(0,9)
                    row = randint(0,9)
        
    return(board)

def clearTerm(n):
    print("\n" * n)

def saveBoatLayout(board):
    try:
        board = str(board)
        fileLoc = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
        

        saveFile = open(os.path.join(fileLoc, 'saveFile.txt'), "w")
        saveFile.write(board)
        saveFile.close()
        print("\nSaved!\n")
        return board
        
    except:
        return "fail"

def pullBoatLayout():
    fileLoc = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    saveFile = open(os.path.join(fileLoc, 'saveFile.txt'), "r")
    try:
        board = ast.literal_eval(saveFile.read())
        return board
    except:
        return "fail"
    



if __name__ == '__main__':
    main()