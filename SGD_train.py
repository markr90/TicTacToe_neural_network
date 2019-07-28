# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 22:05:59 2019

@author: Mark
"""

import tictactoeBasics
import botDeterministic
import botRandom
import botSGD
import numpy as np

from scipy.ndimage.interpolation import shift

def train(model, mode, print_progress = False):
    game = tictactoeBasics.TicTacToeGame()   
    
    scores_list = []
    corrected_scores_list = []
    new_board_states_list = []
    

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
            (move, new_board_state, score) = botSGD.move_selector(
                                                            model,
                                                            game.getBoard(),
                                                            aliceLetter)

            scores_list.append(score[0][0])
            new_board_integer = botSGD.board_integer_representation(new_board_state)
            new_board_states_list.append(new_board_integer)
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
    

    # Correct the scores, assigning 1/0/-1 to the winning/drawn/losing final board state, 
    # and assigning the other previous board states the score of their next board state           
    new_board_states_list = tuple(new_board_states_list)
    new_board_states_list = np.vstack(new_board_states_list)
    if game_status == "won":
        corrected_scores_list = shift(scores_list, -1, cval = 1.0)
    if game_status == "draw": 
        corrected_scores_list = shift(scores_list, -1, cval = 0.0)
    if game_status == "lost":
        corrected_scores_list = shift(scores_list, -1, cval = -1.0)
    if print_progress:
        print("Program has ", game_status)
        print("\n Correcting the Scores and Updating the model weights:")
        print("___________________________________________________________________\n")
    	
    x = new_board_states_list
    y = corrected_scores_list
    
    def unison_shuffled_copies(a, b):
        assert len(a) == len(b)
        p = np.random.permutation(len(a))
        return a[p], b[p]
    
    # shuffle x and y in unison
    x, y = unison_shuffled_copies(x, y)
    x = x.reshape(-1, 9)
    
    model.fit(x, y, epochs = 1, batch_size = 1, verbose = 0)
    return model, y, game_status
    
            