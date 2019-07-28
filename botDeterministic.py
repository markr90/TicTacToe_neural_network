# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 19:41:27 2019

@author: Mark
"""

import random
import tictactoeBasics

def boardCopy(board):
    brdcp = board[:]
    return brdcp

def findWinningMoves(board, letter):
    freespots = tictactoeBasics.freePositions(board)
    winningMoves = []
    for move in freespots:
        brdCopy = boardCopy(board)
        gameCopy = tictactoeBasics.TicTacToeGame()
        gameCopy.setBoard(brdCopy)
        gameCopy.makeMove(letter, move)
        if gameCopy.isWinner(letter):
            winningMoves.append(move)
    return winningMoves

def findForkMoves(board, letter):
    freespots = tictactoeBasics.freePositions(board)
    forkMoves = []
    for move in freespots:
        brdCopy = boardCopy(board)  
        gameCopy = tictactoeBasics.TicTacToeGame()
        gameCopy.setBoard(brdCopy)
        gameCopy.makeMove(letter, move)
        futureWinningMoves = findWinningMoves(brdCopy, letter)
        if len(futureWinningMoves) > 1:
            forkMoves.append(move)       
    return forkMoves

def createsTwoInRow(board, letter, move):
    brdCopy = boardCopy(board)
    gameCopy = tictactoeBasics.TicTacToeGame()
    gameCopy.setBoard(brdCopy)
    gameCopy.makeMove(letter, move)
    blockingMoves = findWinningMoves(brdCopy, letter)
    if len(blockingMoves) > 0:
        return [True] + blockingMoves
    else:
        return [False]
    
def doesNotCreateForkOpportunity(board, letter, blockmoves):
    potentialForkMoves = findForkMoves(board, letter)
    for move in blockmoves:
        if move in potentialForkMoves:
            return False
    
    return True
    
        
def getComputerMove(runningGame, letter, botDifficulty, printMoves = False):
    # random for now
    freespots = tictactoeBasics.freePositions(runningGame.getBoard())
    
    if letter == "X":
        oppLetter = "O"
    else:
        oppLetter = "X"
    
    # Check if the computer has winning moves, if so, make that any of those moves
    winningMoves = findWinningMoves(runningGame.getBoard(), letter)
    if len(winningMoves) > 0:
        if printMoves:
            print("Computer makes winning move")
        return winningMoves[0]
    
    # Check if player has winning moves, if so, block move
    playerWinningMoves = findWinningMoves(runningGame.getBoard(), oppLetter)
    if len(playerWinningMoves) > 0:
        if printMoves:
            print("Computer makes blocking move")
        return playerWinningMoves[0]
    
    
    if botDifficulty == "hard":    
        # Check if computer can create a fork, if so, play fork move
        forkMoves = findForkMoves(runningGame.getBoard(), letter)
        if len(forkMoves) > 0:
            if printMoves:
                print("Computer creates fork")
            return forkMoves[0]
        
        playerForkMoves = findForkMoves(runningGame.getBoard(), oppLetter)
        if len(playerForkMoves) == 1:
            if printMoves:
                print("Computer blocks players fork opportunity")
            return playerForkMoves[0]
        elif len(playerForkMoves) > 1:
            for move in playerForkMoves:
                twoInRowInfo = createsTwoInRow(runningGame.getBoard(), letter, move)
                if twoInRowInfo[0]:
                    if printMoves:
                        print("Computer blocks players fork and creates two in row")
                    return move
        else:
            for move in freespots:
                brdCopy = boardCopy(runningGame.getBoard())
                gameCopy = tictactoeBasics.TicTacToeGame()
                gameCopy.setBoard(brdCopy)
                gameCopy.makeMove(letter, move)
                twoInRowInfo = createsTwoInRow(runningGame.getBoard(), letter, move) # Array with [bool, blocking moves]
                if twoInRowInfo[0] and doesNotCreateForkOpportunity(brdCopy, oppLetter, twoInRowInfo[1:]):
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