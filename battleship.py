"""
Created by Elijah Murphy on 23 January 2022

Battleship PvE is a game in which the player plays the 1967 board game made by The Milton Bradley Company. 
The player places their own ships then attempts to sink the computers randomly generated ships before the 
computer sinks their's. This is part of a project for a CS2 class for high school.

LOGS:
As of 3 Febuary 2022: Basic game completed. Function documentation completed. More to come.
As of 9 Febuary 2022: Player AI upgraded, sound FX, HTML documentation created

BUGS:

BONUS:
1. Make the dots into shapes (like battleship).
3. Make the dots move one box in a random direction every round
4. Tell the user how close to the nearest dot their shot was.
5. Play sounds for ‘hit’ & ‘miss’ & ‘kaboom’
*. Saves a ship layout for future use and retrives it

"""

#REQ LIBRARYS
import random
from random import randint
from time import sleep
from tqdm import tqdm
from playsound import playsound
import os
import ast

#SOUND FILE PATHS
realPath = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))) #finds the location of this file so it works on all computers 
print(realPath)
explosion = os.path.join(realPath + '\Sound Files\explosion.wav')
missSound = os.path.join(realPath + '\Sound Files\splash.mp3')


def main():
    hidden_board = [["~"] * 10 for x in range(10)] #Single line to make a 10x10 array
    guess_board = [["~"] * 10 for x in range(10)]
    player_board = [["~"] * 10 for x in range(10)]

    hidden_board = generateShips(hidden_board)


    print("Welcome to Battleship!\n")
    
    while True:

        pullBoard = input("Would you like to pull the saved board? (y/n): ")
        if pullBoard in "nN":

            print("Let's create your board!")

            showBoard(player_board)

            player_board = shipManager(player_board)

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
            if guess_board[row][column] in "ØX":                                                #If the coordinate was already shot
                print("You already guessed that spot!")
                showBoard(guess_board)
            elif hidden_board[row][column] == "X":                                              #If the guess coordinate hits a boat on the hidden board
                print("Congradulations! You hit an enemy boat!")
                guess_board[row][column] = "X"                                                  #Sets guess board as a hit
                showBoard(guess_board)
                playsound(explosion)
                turn = "bot"
            else:                                                                               #If the guess coordinate misses on the hidden board
                print("\nSorry, you missed!") 
                guess_board[row][column] = "Ø"                                                  #Sets the guess board as a miss
                showBoard(guess_board)
                playsound(missSound)
                turn = "bot"
            if hitShips(guess_board) == 17:                                                     #If all ships have been hit, a total of 17 tiles
                print("You hit them all, good job!")
                showBoard(guess_board)
                break
        while turn == "bot":
            turnMade = False
            for i in tqdm(range(0, 20), unit =" ticks", desc ="The enemy is thinking..."):      #Uses tqdm to create a loading bar
                sleep(.1)
            while turnMade == False:
                clearTerm(100)
                row = randint(0,9)                                                              #Makes random coordinate guess
                col = randint(0,9)
                if player_board[row][col] == "#":                                               #If the guess coordinate hits
                    player_board[row][col] = "X"
                    print("Your board: \n")
                    showBoard(player_board)
                    print("\nDamn! Your hit!\n")
                    print("Your enemy's board: ")
                    showBoard(guess_board)
                    turnMade = True
                    turn = "player"
                elif player_board[row][col] in "XØ":                                            #Retries if already shot there
                    pass
                elif player_board[row][col] == "~":                                             #If the guess coordiate misses
                    player_board[row][col] = "Ø"
                    print("Your sea: \n")
                    showBoard(player_board)
                    print("Your enemy's sea: \n")
                    showBoard(guess_board)
                    print("\nThe computer missed!\n")
                    turnMade = True
                    turn = "player"
                if hitShips(player_board) == 17:                                                #If all the ships
                    print("All your ships have been sunk. Better luck next time!")
                    break

def showBoard(board):
    '''
    Displays the player board
 
    :param name: board the array that is displayed
    :param type: list
    :returns: null
    :return type: null
    :raises: null
    '''
    print("    A B C D E F G H I J")
    print("   ---------------------")

    rownumb = 1
    for r in board:
        if rownumb == 10:                                        #If the number of the line is 10, it will remove one space due to the extra digit
            space = " "
        else:
            space = "  "
        print("%d|%s|" % (rownumb, space + "|".join(r)))         #formats and prints the row of the board
        rownumb += 1

def shipManager(board):
    '''
    handles order of user ship placments
 
    :param name: board: the array that is displayed
    :param type: list
    :returns: board: the origional array with boats applied
    :return type: list
    :raises: null
    '''
    
    #A dictionary to store value of each boat
    shipSize = {'Carrier': 5, 'Battleship': 4, 'Cruiser': 3, 'Submarine': 3, 'Destroyer': 2} 

    #An array to store amount of ships avalible
    shipList = [['Carrier', 1], ['Battleship', 1], ['Cruiser', 1], ['Submarine', 1], ['Destroyer', 1]]

    for x in shipList: 

        while x[1] > 0:                                                 #If the ship selected is avalible
            shipType = x[0]
            ship_size = shipSize[x[0]]
            boatMade = False
            while boatMade == False:
                testValidity = shipDeploy(board, ship_size, shipType)   #Calls function to place ships
                if testValidity == None:
                    pass
                else:
                    x[1] -= 1
                    board = testValidity
                    boatMade = True
                
    return board
    
def shipDeploy(board, ship_size, type):
    '''
    Places ships and makes sure they do not collide or exit the bountry of the array
 
    :param names: | board: the array that is displayed | ship_size: size of ship being placed | type: name of ship being placed
    :param type:  | list | integer | string
    :returns: board: The array with the ships placed
    :return type: list
    :raises: null
    '''

    print("Where would you like to put your", str(type) + ", the", str(ship_size), "long boat? (A1)") #Prints the and length of the ship being placed
    pos = input("Input here: ")
    row, column = locationFormat(pos)                                                                 #Formats alpha-neumeric coordinate to row and column
    while True:
        try:
            angle = input("Place it up, down, left, or right? (u,d,l,r): ").upper()                   #Gets orientation
            if angle not in "UDLR":
                print("Please enter either u, l, d, or r.")
            if angle in "UDLR":
                break
        except:
            print("Please enter either U, L, D, or R.")
            pass
    shipsMade = 0
    while shipsMade != 5:
        if angle == "U":                                                                              #Code for each direction is the same except for collision checking numbers and placment numbers
            colission = False
            buildCount = 0
            if 0 <= (row+1 + int(-1 * ship_size)) <= 9:                                               #Checks to see if the length of the ship will collide with the end of the array
                for i in range(ship_size):
                    buildCount += 1
                    if board[int(row)-i][int(column)] == "#":                                         #If ship collides with another ship
                        colission = True                                                              #Marks a collision and will retry
                        pass
            else:
                colission = True
            
            if colission is False:
                for k in range(buildCount):
                    board[int(row)-k][int(column)] = "#"                                              #Creates ship
                clearTerm(100)
                showBoard(board)
        
        if angle == "D":                                                                              #See above documentation
            colission = False
            buildCount = 0
            if row + int(ship_size) <= 9: 
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
        
        if angle == "R":                                                                              #See above documentation
            colission = False
            buildCount = 0
            if 0 <= (column-1 + int(ship_size)) <= 9: 
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

        if angle == "L":                                                                              #See above documentation
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
    '''
    Formats alpha-numeric coordinate to row and column variables

    :param name: hitcoord: the user inputted coordinate
    :param type: string
    :returns: | row: value of x coordinate on array | column: value of y coordinate on array
    :return type: | int | int |
    :raises: null
    '''
    alphaConvert = {'A': 0, 'B':1, 'C':2,'D':3,'E':4,"F":5,'G':6,'H':7, 'I':8, "J":9}                                           #Dict with letter's numerical value
    colPass = False
    rowPass = False
    while True:
        if len(hitcoord) == 2 or len(hitcoord) == 3 and hitcoord[0] in "ABCDEFGHIJabcdefghij" and hitcoord[1] in "1234567890":  #If the input is 2-3 characters long and contains only alphabtical characters            
            column = hitcoord[0].upper()
            colPass = True
            if len(hitcoord) == 2:                                                                                              #Seperated 1-9 and 10 due to digit lengths
                row = int(hitcoord[1])
                rowPass = True
            else:
                row = int(str(hitcoord[1]) + str(hitcoord[2]))
                rowPass = True
            if row > 10:
                print("Please input a row between 1-10.")
                rowPass = False
        if colPass and rowPass:
            return int(row)-1, alphaConvert[column]                                                                             #Returns row and column value
        else:
            print("Please input a coordinate (A-J1-10)")
            hitcoord = list(input("Please input hit coordinates (ex. A1): "))
                 
def hitShips(board):
    '''
    returns amount of hit shots 
 
    :param name: board: the gameboard
    :param type: array
    :returns: board: hits: the number of shots that have hit a boat
    :return type: int
    :raises: null
    '''
    
    hits = 0
    for row in board:
        for column in row:
            if column == "X":
                hits += 1
    return hits

def generateShips(board):
    '''
    handles computer automatic ship generation
 
    :param name: board: the gameboard
    :param type: list
    :returns: board: the original array with boats applied
    :return type: list
    :raises: null
    '''
    
    shipLen = [5,4,3,3,2]
    shipAvalible = 5
    directionposibilities = ["vertical", "horizontal"]   

    
    for i in range(shipAvalible):
        boatMade = False

        while boatMade == False:
            direction = random.choice(directionposibilities)            #Random ship placements
            col = randint(0,9)
            row = randint(0,9)
   
            if direction == "vertical":
                buildCount = 0
                if row + int(shipLen[i]) <= 9:                          #Checks to see if ship will wrap
                    colission = False
                    for j in range(0, int(shipLen[i])):                 
                        buildCount += 1
                        if board[int(row+j)][int(col)] == "X":          #Checks to see if ship collides
                            colission = True
                            pass
                    if not colission:
                        for k in range(buildCount):
                            board[int(row+k)][int(col)] = "X"           #Print Ships
                        boatMade = True
                        shipAvalible = shipAvalible - 1
                
            if direction == "horizontal":                               #If statment above's documentation is the same as below
                if col + int(shipLen[i]) <= 9: 
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
    '''
    Simple 1 line function to print a newline to hide unwanted terminal output

    :param name: n: the amount of lines to be cleared
    :param type: int
    :returns: board: null
    :return type: null
    :raises: null
    '''
    print("\n" * n)

def saveBoatLayout(board):
    '''
    Saves boat placment to a text file to be used in later games
 
    :param name: board: the gameboard

    :param type: list
    :returns: board OR "fail": sent back to the call for verification purposes
    :return type: list OR string
    :raises: null
    '''
    try:
        board = str(board)                                                          #Converts array to string for document saving
        fileLoc = os.path.realpath(                                                 
        os.path.join(os.getcwd(), os.path.dirname(__file__)))                       #Gets the local path to this file
        

        saveFile = open(os.path.join(fileLoc, 'saveFile.txt'), "w")                 #Opens save file to be written in
        saveFile.write(board)                                                       #Writes board to file
        saveFile.close()
        print("\nSaved!\n")
        return board
        
    except:
        return "fail"

def pullBoatLayout():
    '''
    loads game save file
 
    :param name: null
    :param type: null
    :returns: board: the saved game board
    :return type: list
    :raises: null
    '''
    fileLoc = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))                           #Gets the local path to this file
    try:
        saveFile = open(os.path.join(fileLoc, 'saveFile.txt'), "r")                 #Reads in the save file
        board = ast.literal_eval(saveFile.read())                                   #Reads the text in the file as the array it is and not the string it is stored as
        return board
    except:
        return "fail"

if __name__ == '__main__':
    main()

# Copyright (c) 2022 Elijah A. Murphy
# Distributed under the terms of the MIT License. 
# SPDX-License-Identifier: MIT
# This code is part of the Battleship project (https://github.com/Eli-Murphy/Battleship)