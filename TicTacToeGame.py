# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 16:30:51 2019

@author: Mark
"""

import random
import botDeterministic
import botTQ
import botRandom

def isWinner(board, letter):
    return ((board[1] == letter and board[2] == letter and board[3] == letter) or
            (board[4] == letter and board[5] == letter and board[6] == letter) or 
            (board[7] == letter and board[8] == letter and board[9] == letter) or 
            (board[1] == letter and board[4] == letter and board[7] == letter) or 
            (board[2] == letter and board[5] == letter and board[8] == letter) or 
            (board[3] == letter and board[6] == letter and board[9] == letter) or 
            (board[1] == letter and board[5] == letter and board[9] == letter) or 
            (board[3] == letter and board[5] == letter and board[7] == letter))        

def getFreePositions(board):
    free = []
    for i in range(1,10):
        if board[i] == " ":
            free.append(i)
    return free
   

class TicTacToeGame(object):
    """The main tictactoe game. Players can choose what bot they want to play against
    the function has multiple points where players can provide input"""

    def __init__(self, trainedBot):
        self.trainedBot = trainedBot
        self.Bot = trainedBot
        self.IsRunning = False
        self.board = [" " for i in range(10)]
        self.PlayerLetter = "X"
        self.ComputerLetter = "O"
    
    def replay(self):
        """Queries the player if it wants to replay again, returns boolean depending
        on the players response"""
        print("Do you want to play again (Y / N)?")
        ans = input()
        
        if ans.lower() == "y":
            self.play()
        elif ans.lower() == "n":
            return
        else:
            print("Not a valid choice")
            self.replay()

    def play(self):    
        print("""Welcome to TicTacToe AI. Play TicTacToe against different kinds of bots.
            See if you are smarter than a TQ bot... Or if you can play a draw
            against the unbeatable hard mode bot every game!
            You can exit at any given time with <exit>.""")
        self.__GameLoop()

    def __isExitCommand(self, s):
        return s == "exit"

    def __handleExitCommand(self):
        print("Quitting game...")
        self.IsRunning = False
        self.IsQuitting = True

    def __selectBot(self):
        # Ask what bot the player wants to play against
        print("""Choose your opponent 
        1) Difficulty bot: Hard
        2) Difficulty bot: Easy
        3) Random bot
        4) Self learning TQ bot """)
        playMode = input()
        if self.__isExitCommand(playMode):
            self.__handleExitCommand()
        if playMode == "1":             
            self.Bot = botDeterministic.botDeterministic("hard")
        elif playMode == "2":
            self.Bot = botDeterministic.botDeterministic("easy")
        elif playMode == "3":
            self.Bot = botRandom.botRandom()
        elif playMode == "4":
            self.Bot = self.trainedBot 

    def __GameLoop(self):
        self.IsRunning = True
        self.IsQuitting = False
        self.__selectBot()
        # some initialization values
        self.resetBoard()
        whosTurn = self.whoGoesFirst()
        if not self.IsQuitting:
            print(whosTurn + " starts!")            
        # The actual game
        while self.IsRunning and not self.IsQuitting:
            if whosTurn == "player":
                self.drawBoard()
                print("Player's turn:")
                move = input()
                if self.__isExitCommand(move):
                    self.__handleExitCommand()
                    break
                self.playerMove(move)
                # check if win / draw conditions are met otherwise give turn
                # to next player
                if isWinner(self.board, self.PlayerLetter):
                    self.drawBoard()
                    game_status = "lost"
                    print ("Player has won the game, congratulations!")
                    self.IsRunning = False
                elif self.boardFull():
                    self.drawBoard()
                    game_status = "draw"
                    print("Too bad! Game is a tie, try again.")
                    self.IsRunning = False
                else:
                    whosTurn = "computer"
            else:
                move = self.Bot.GetMove(self, self.ComputerLetter)
                self.makeMove(self.ComputerLetter, move)
                # check if win / draw conditions are met otherwise give turn
                # to next player
                if isWinner(self.board, self.ComputerLetter):
                    self.drawBoard()
                    game_status = "won"
                    print ("Game over! Computer has won the game.")
                    self.IsRunning = False
                elif self.boardFull():
                    self.drawBoard()
                    game_status = "draw"
                    print("Too bad! Game is a tie, try again.")
                    self.IsRunning = False
                else:
                    whosTurn = "player"
        # Update bot Q function             
        if isinstance(self.Bot, type(self.trainedBot)) and not self.IsQuitting:
            self.Bot.update_Qfunction(game_status)
            self.Bot.reset_move_history()
        if not self.IsQuitting:
            self.replay()

    def getBoard(self):
        return self.board    
    
    def boardEmpty(self):
        return all([self.board[i] == " " for i in range(1,10)])  
    
    def boardFull(self): 
        return all([self.board[i] != " " for i in range(1,10)]) 

    def whoGoesFirst(self):
        # randomly choose who goes first
        if random.randint(0,1) == 0:
            return "computer"
        else:
            return "player"

    def resetBoard(self):
        self.board = [" " for i in range(10)]

    def drawBoard(self):        
        print("", self.board[7], "|", self.board[8], "|", self.board[9])
        print("___|___|___")
        print("   |   |   ")
        print("", self.board[4], "|", self.board[5], "|", self.board[6])
        print("___|___|___")
        print("   |   |   ")
        print("", self.board[1], "|", self.board[2], "|", self.board[3])
    
    def __isValidMove(self, move):
        return self.board[move] == " "

    def makeMove(self, letter, move):
        self.board[move] = letter
    
    def playerMove(self, move):
        if move != "" and move in "123456789":
            if self.__isValidMove(int(move)):
                self.makeMove(self.PlayerLetter, int(move))
            else:
                print("Board position already taken. Select another move.")
                move = input()
                self.playerMove(move)
        else:
            print("Not a valid move entry. Use numbers of numpad to select square.")
            move = input()
            self.playerMove(move) 

    def generateLegalBoardStatesDict(self, letter):
        """ Creates a dictionary with the set of all possible moves
        and resulting board states for a given board state and player (letter: X or O)
        """
        legal_moves_dict = {}
        legalMoves = freePositions(self.board)
        
        for move in legalMoves:
            brdCopy = self.board[:]
            brdCopy[move] = letter
            legal_moves_dict[move] = brdCopy[:]
        return legal_moves_dict     
        

        

    
         
    
        