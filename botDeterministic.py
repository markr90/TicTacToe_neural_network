# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 19:41:27 2019

@author: Mark
"""

import random
from IBot import IBot
import TicTacToeGame

class botDeterministic(IBot):

    def __init__(self, botDifficulty):
        self.BotDifficulty = botDifficulty

    @staticmethod
    def __boardCopy(board):
        brdcp = board[:]
        return brdcp

    def findWinningMoves(self, board, letter):
        """Find moves that can win the game"""
        freespots = TicTacToeGame.getFreePositions(board)
        winningMoves = []
        for move in freespots:
            brdCopy = self.__boardCopy(board)
            brdCopy[move] = letter
            if TicTacToeGame.isWinner(brdCopy, letter):
                winningMoves.append(move)
        return winningMoves

    def findForkMoves(self, board, letter):
        """Find moves that create a fork"""
        freespots = TicTacToeGame.getFreePositions(board)
        forkMoves = []
        for move in freespots:
            brdCopy = self.__boardCopy(board)
            brdCopy[move] = letter
            futureWinningMoves = self.findWinningMoves(brdCopy, letter)
            if len(futureWinningMoves) > 1:
                forkMoves.append(move)       
        return forkMoves

    def createsTwoInRow(self, board, letter, move):
        """Find moves that create two in a row"""
        brdCopy = self.__boardCopy(board)
        brdCopy[move] = letter
        futWinMoves = self.findWinningMoves(brdCopy, letter)
        if len(futWinMoves) > 0:
            return [True] + futWinMoves
        else:
            return [False]
    
    def doesNotCreateForkOpportunity(self, board, letter, blockmoves):
        """Check if any of the moves in blockMoves creates a fork opportunity
        for the opponent"""
        potentialForkMoves = self.findForkMoves(board, letter)
        for move in blockmoves:
            if move in potentialForkMoves:
                return False
        
        return True

    def GetMove(self, game, letter):
        return self.getComputerMove(game, letter, self.BotDifficulty, False)    
        
    def getComputerMove(self, runningGame, letter, botDifficulty, printMoves = False):
        """
        If bot difficulty is set to "easy" only moves 1 and 2 are peformed
        If bot difficulty is set to hard moves 1 to 8 are executed
        
        Function returns a move depending on the current game state
        args:
        letter = symbol of the computer ("X" or "O")
        
        If the player is defending this is not an optimal strategy, but too lazy
        to implement an unbeatable bot...
        The optimal strategy for any player that is opening is:
        1. Win: If the player has two in a row, they can place a third to get three in a row.
        2. Block: If the opponent has two in a row, the player must play the third themselves to block the opponent.
        3. Fork: Create an opportunity where the player has two ways to win (two non-blocked lines of 2).
        4. Blocking an opponent's fork: If there is only one possible fork for the opponent, the player 
            should block it. Otherwise, the player should block any forks in any way that simultaneously 
            allows them to create two in a row. Otherwise, the player should create a two in a row to 
            force the opponent into defending, as long as it doesn't result in them creating a fork. 
            For example, if "X" has two opposite corners and "O" has the center, "O" must not play 
            a corner in order to win. (Playing a corner in this scenario creates a fork for "X" to win.)
        5. Center: A player marks the center. (If it is the first move of the game, playing on a corner 
            gives the second player more opportunities to make a mistake and may therefore be the better 
            choice; however, it makes no difference between perfect players.)
        6. Opposite corner: If the opponent is in the corner, the player plays the opposite corner.
        7. Empty corner: The player plays in a corner square.
        8. Empty side: The player plays in a middle square on any of the 4 sides. 
        """
        freespots = TicTacToeGame.getFreePositions(runningGame.getBoard())
        
        if letter == "X":
            oppLetter = "O"
        else:
            oppLetter = "X"
        
        # Check if the computer has winning moves, if so, make that any of those moves
        winningMoves = self.findWinningMoves(runningGame.getBoard(), letter)
        if len(winningMoves) > 0:
            if printMoves:
                print("Computer makes winning move")
            return winningMoves[0]
        
        # Check if player has winning moves, if so, block move
        playerWinningMoves = self.findWinningMoves(runningGame.getBoard(), oppLetter)
        if len(playerWinningMoves) > 0:
            if printMoves:
                print("Computer makes blocking move")
            return playerWinningMoves[0]
        
        
        if botDifficulty == "hard":    
            # Check if computer can create a fork, if so, play fork move
            forkMoves = self.findForkMoves(runningGame.getBoard(), letter)
            if len(forkMoves) > 0:
                if printMoves:
                    print("Computer creates fork")
                return forkMoves[0]
            
            playerForkMoves = self.findForkMoves(runningGame.getBoard(), oppLetter)
            if len(playerForkMoves) == 1:
                if printMoves:
                    print("Computer blocks players fork opportunity")
                return playerForkMoves[0]
            elif len(playerForkMoves) > 1:
                for move in playerForkMoves:
                    twoInRowInfo = self.createsTwoInRow(runningGame.getBoard(), letter, move)
                    if twoInRowInfo[0]:
                        if printMoves:
                            print("Computer blocks players fork and creates two in row")
                        return move
            else:
                for move in freespots:
                    brdCopy = self.__boardCopy(runningGame.getBoard())
                    brdCopy[move] = letter
                    twoInRowInfo = self.createsTwoInRow(runningGame.getBoard(), letter, move) # Array with [bool, blocking moves]
                    if twoInRowInfo[0] and self.doesNotCreateForkOpportunity(brdCopy, oppLetter, twoInRowInfo[1:]):
                        if printMoves:
                            print("Computer creates two in row and does not create fork opportunity")
                        return move
            # center move if board is empty
            if 5 in freespots and runningGame.boardEmpty():
                if printMoves:
                    print("Computer plays center move")
                return 5
            # opposite corner move
            if runningGame.getBoard()[1] == oppLetter and 9 in freespots:
                if printMoves:
                    print("Computer plays opposite corner move")
                return 9
            if runningGame.getBoard()[3] == oppLetter and 7 in freespots:
                if printMoves:
                    print("Computer plays opposite corner move")
                return 7
            if runningGame.getBoard()[7] == oppLetter and 3 in freespots:
                if printMoves:
                    print("Computer plays opposite corner move")
                return 3
            if runningGame.getBoard()[9] == oppLetter and 1 in freespots:
                if printMoves:
                    print("Computer plays opposite corner move")
                return 1
            # empty corner
            emptyCorners = []
            for i in [1,3,7,9]:
                if runningGame.getBoard()[i] == " ":
                    emptyCorners.append(i)
            
            if len(emptyCorners) > 0:
                if printMoves:
                    print("Computer plays empty corner")
                return random.choice(emptyCorners) #doesn't matter which empty corner you take
            # empty side
            emptySides = []
            for i in [2,4,6,8]:
                if runningGame.getBoard()[i] == " ":
                    emptySides.append(i)
            if len(emptySides) > 0:
                if printMoves:
                    print("Computer playes empty side")
                return random.choice(emptySides)
            
        if botDifficulty == "easy":
            move = random.choice(freespots)
            return move