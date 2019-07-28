# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 22:05:59 2019

@author: Mark
"""

import tictactoeBasics
import botDeterministic
import botRandom

def trainTQbot(mode, bot, updateQ = True, print_progress = False):
    """
    Trains the tabular Q bot. Plays against any of the hard, easy or 
    random bots. If updateQ = False the Q function for the bot will not be modified
    
    Returns the result of the game "won" or "draw" or "loss"
    """
    
    # Initialize the game
    game = tictactoeBasics.TicTacToeGame()   
    game.newBoard()
    bobLetter, aliceLetter = "X", "O"
    whosTurn = game.whoGoesFirst()
    playing = True
    
    # play the game
    while playing:
        if whosTurn == "player": 
            # hard / easy / random bot turn
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
                
            # Check if player X wins or created a draw
            if game.isWinner(bobLetter):
                game_status = "lost"
                playing = False
            elif game.boardFull():
                game_status = "draw"
                playing = False
            else:
                whosTurn = "computer"
        else: 
            # Machine learning bot plays
            (move, score) = bot.get_move(game.getBoard(), aliceLetter)
            game.makeMove(aliceLetter, move)
            if print_progress:
                print("Alice made move:", move, "with score:", score)
                game.drawBoard()
            
            # Check if player O wins or created a draw
            if game.isWinner(aliceLetter):
                game_status = "won"
                playing = False
            elif game.boardFull():
                game_status = "draw"
                playing = False
            else:
                whosTurn = "player"
    
    # update Q function
    if updateQ:
        bot.update_Qfunction(game_status)
    bot.reset_move_history()
    
    return game_status
    
            