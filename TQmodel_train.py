# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 22:05:59 2019

@author: Mark
"""

import tictactoeBasics
import botDeterministic
import botRandom

def trainTQbot(mode, bot, updateQ = True, print_progress = False):
    game = tictactoeBasics.TicTacToeGame()   
      

    """Initialize the game
    Two bots called Bob and Alice
    If neural network bot wins assign score
    win = 1, draw = 0, loss = -1"""
    game.newBoard()
    bobLetter, aliceLetter = "X", "O"
    whosTurn = game.whoGoesFirst()
    playing = True
    
    while playing:
        if whosTurn == "player": 
            # Deterministic bot plays
            if mode == "hard":
                if print_progress:                
                    print("playing against hard")
                move = botDeterministic.getComputerMove(game, bobLetter, mode)
            if mode == "easy":
                if print_progress:                
                    print("playing against easy")
                move = botDeterministic.getComputerMove(game, bobLetter, mode)
            if mode == "random":
                if print_progress:
                    print("playing against random")
                move = botRandom.getComputerMove(game, bobLetter)
            game.makeMove(bobLetter, move)
            if print_progress:
                print("Bob made move:", move)
                game.drawBoard()
                
            # machine_learning bot loses
            if game.isWinner(bobLetter):
                game_status = "lost"
                playing = False
            elif game.boardFull():
                game_status = "draw"
                playing = False
            else:
                whosTurn = "computer"
        else: 
            # Neural network bot plays
            (move, score) = bot.get_move(game.getBoard(), aliceLetter)
            game.makeMove(aliceLetter, move)
            if print_progress:
                print("Alice made move:", move, "with score:", score)
                game.drawBoard()
            if game.isWinner(aliceLetter):
                game_status = "won"
                playing = False
            elif game.boardFull():
                game_status = "draw"
                playing = False
            else:
                whosTurn = "player"
    
    if updateQ:
        bot.update_Qfunction(game_status)
    bot.reset_move_history()
    
    return game_status
    
            