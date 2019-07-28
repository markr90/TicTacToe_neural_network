# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 19:43:33 2019

The building blocks for the tic tac toe game:
    Board drawing
    Board generation
    Determining who plays first
    Test if moves are valid
    

@author: Mark
"""

import exitModule
import random

    
def freePositions(board):
    free = []
    for i in range(1,10):
        if board[i] == " ":
            free.append(i)
    return free

def legal_moves_generator(board, letter):
    """ Creates a dictionary with the set of all possible moves
    and resulting board states for a given board state and player (letter: X or O)
    """
    legal_moves_dict = {}
    legalMoves = freePositions(board)
    
    for move in legalMoves:
        brdCopy = board[:]
        brdCopy[move] = letter
        legal_moves_dict[move] = brdCopy[:]
    return legal_moves_dict        

class TicTacToeGame(object):
    
    def __init__(self):
        self.board = [" " for i in range(10)]
        
    def setBoard(self, brd):
        self.board = brd
    def getBoard(self):
        return self.board
    def newBoard(self):
        self.board = [" " for i in range(10)]

    def drawBoard(self):
        
        print("", self.board[7], "|", self.board[8], "|", self.board[9])
        print("___|___|___")
        print("   |   |   ")
        print("", self.board[4], "|", self.board[5], "|", self.board[6])
        print("___|___|___")
        print("   |   |   ")
        print("", self.board[1], "|", self.board[2], "|", self.board[3])
        
    
   
    
    def selectPlayer(self):
        print("Do you want to be X or O?")
        playerLetter = input().upper()  
        if exitModule.exitCondition(playerLetter):
            exitModule.QUITGAME = True
            return (-1, -1)
        
        if playerLetter == "X":
            computerLetter = "O"
            return playerLetter, computerLetter
        elif playerLetter == "O":
            computerLetter = "X"
            return playerLetter, computerLetter
        else:
            print("Not a valid choice.")
            return self.selectPlayer()
    
        return playerLetter, computerLetter

    def whoGoesFirst(self):
        # randomly choose who goes first
        if random.randint(0,1) == 0:
            return "computer"
        else:
            return "player"
    
    def validMove(self, move):
        return self.board[move] == " "

    def makeMove(self, letter, move):
        self.board[move] = letter
    
    def playerMove(self, letter):
        move = input()
        
        if exitModule.exitCondition(move):
            exitModule.QUITGAME = True
            return
        
        if move in "123456789":
            if self.validMove(int(move)):
                self.makeMove(letter, int(move))
            else:
                print("Board position already taken")
                self.playerMove(letter)
        else:
            print("Not a valid move entry")
            self.playerMove(letter) 
        
    def boardEmpty(self):
        return all([self.board[i] == " " for i in range(1,10)])
    
    def isWinner(self, letter):
        return ((self.board[1] == letter and self.board[2] == letter and self.board[3] == letter) or
                (self.board[4] == letter and self.board[5] == letter and self.board[6] == letter) or 
                (self.board[7] == letter and self.board[8] == letter and self.board[9] == letter) or 
                (self.board[1] == letter and self.board[4] == letter and self.board[7] == letter) or 
                (self.board[2] == letter and self.board[5] == letter and self.board[8] == letter) or 
                (self.board[3] == letter and self.board[6] == letter and self.board[9] == letter) or 
                (self.board[1] == letter and self.board[5] == letter and self.board[9] == letter) or 
                (self.board[3] == letter and self.board[5] == letter and self.board[7] == letter))
                
    
    def boardFull(self): 
        return all([self.board[i] != " " for i in range(1,10)])