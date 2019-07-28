# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 19:41:27 2019

@author: Mark
"""

import random
import tictactoeBasics

def boardCopy(board):
    """ Copies the board and returns it """
    brdcp = board[:]
    return brdcp

def findWinningMoves(board, letter):
    """ Finds list of moves that can win the game"""
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
    """ Finds list of available fork moves and returns it"""
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
    """ Checks if the move creates a two in a row for player letter"""
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
    """ Checks if the any of the blocking moves in argument blockmoves
    does not create a fork opportunity for the opponent """
    
    potentialForkMoves = findForkMoves(board, letter)
    for move in blockmoves:
        if move in potentialForkMoves:
            return False
    
    return True

def defensiveMove(board, letter):
    """If bot is on the defensive it must always play the following counters to the first move
    center -> counter with corner move
    corner -> counter with center move then edge
    edge -> counter with center move"""
    
    if board[5] == letter:
        move = random.choice([1,3,7,9])
        return move, False
    elif board[1] == letter or board[3] == letter or board[7] == letter or board[9] == letter:
        return 5, True
        # center move counters everything except a corner move
        return 5, False
    
def getComputerMove(runningGame, letter, isOpening, printMoves = False):
    """
    If the bot is not opening the game it should follow the defensiveMove opening defined above and then continue
    with the priority list below.
    
    If bot opens the game follow belowp priority list
    
    The optimal strategy for any player is
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
    # Determine available spots on board
    freespots = tictactoeBasics.freePositions(runningGame.getBoard())
    
    # Find opponents symbol
    if letter == "X":
        oppLetter = "O"
    else:
        oppLetter = "X"
    
    # check if opening    
    if not isOpening:
        return defensiveMove(runningGame.getBoard(), oppLetter)
            
    
    # Check if the computer has winning moves, if so, make that any of those moves
    winningMoves = findWinningMoves(runningGame.getBoard(), letter)
    if len(winningMoves) > 0:
        if printMoves:
            print("Computer makes winning move")
        return winningMoves[0], False
    
    # Check if player has winning moves, if so, block move
    playerWinningMoves = findWinningMoves(runningGame.getBoard(), oppLetter)
    if len(playerWinningMoves) > 0:
        if printMoves:
            print("Computer makes blocking move")
        return playerWinningMoves[0], False
    
      
    # Check if computer can create a fork, if so, play fork move
    forkMoves = findForkMoves(runningGame.getBoard(), letter)
    if len(forkMoves) > 0:
        if printMoves:
            print("Computer creates fork")
        return forkMoves[0], False
    
    # Step 4 counter opponent fork move 
    playerForkMoves = findForkMoves(runningGame.getBoard(), oppLetter)
    if len(playerForkMoves) == 1:
        if printMoves:
            print("Computer blocks players fork opportunity")
        return playerForkMoves[0], False
    elif len(playerForkMoves) > 1:
        for move in playerForkMoves:
            twoInRowInfo = createsTwoInRow(runningGame.getBoard(), letter, move)
            if twoInRowInfo[0]:
                if printMoves:
                    print("Computer blocks players fork and creates two in row")
                return move, False
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
                return move, False
    # center move if board is empty
    if 5 in freespots and runningGame.boardEmpty():
        if printMoves:
            print("Computer plays center move")
        return 5, False
    # opposite corner move
    if runningGame.getBoard()[1] == oppLetter and 9 in freespots:
        if printMoves:
            print("Computer plays opposite corner move")
        return 9, False
    if runningGame.getBoard()[3] == oppLetter and 7 in freespots:
        if printMoves:
            print("Computer plays opposite corner move")
        return 7, False
    if runningGame.getBoard()[7] == oppLetter and 3 in freespots:
        if printMoves:
            print("Computer plays opposite corner move")
        return 3, False
    if runningGame.getBoard()[9] == oppLetter and 1 in freespots:
        if printMoves:
            print("Computer plays opposite corner move")
        return 1, False
    # empty corner
    emptyCorners = []
    for i in [1,3,7,9]:
        if runningGame.getBoard()[i] == " ":
            emptyCorners.append(i)
    # play random empty corner
    if len(emptyCorners) > 0:
        if printMoves:
            print("Computer plays empty corner")
        return random.choice(emptyCorners), False #doesn't matter which empty corner you take
    # play random empty side
    emptySides = []
    for i in [2,4,6,8]:
        if runningGame.getBoard()[i] == " ":
            emptySides.append(i)
    if len(emptySides) > 0:
        if printMoves:
            print("Computer playes empty side")
        return random.choice(emptySides), False
