# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 17:07:19 2019

@author: Mark
"""

import numpy as np
import TicTacToeGame
from IBot import IBot
import pandas as pd
import random
import TQmodel_train

WIN_VALUE = 1.0  # type: float
DRAW_VALUE = 0.5  # type: float
LOSS_VALUE = 0.0  # type: float

def hash_value(board_state):
    """ Creates a special ID for the board state which is just a string
    representation of the board, i.e "  X O   X" with spaces denoting empty
    board positions
    """
    res = ""
    for i in range(1,10):
        res = res + board_state[i]
    return res        
      
def train_model(bot, nIterations, resolution = 50):
    """args
    bot: the bot to be trained
    nIterations how many training iterations do you want to do
    approximately 20'000 are needed to train against all 3 bots
    resolution is the distance between the points in the training graph
    in the x axis (game_counter axis)

    returns the training progress dataframe progress_data"""
    
    # Track training progress
    progress_data = pd.DataFrame()
    # Define bots to train against
    modes = ["hard", "easy", "random"]
    selected_mode = random.choice(modes)
    
    # Train the bot
    for game_counter in range(nIterations):
        if game_counter % resolution == 0:
            print("Game #: ", game_counter)
            print("Mode:", selected_mode)
            selected_mode = random.choice(modes)
            
            nWins = 0
            nDraws = 0
            nLosses = 0
            
            # Track training progress by playing 50 dummy games without training
            # the bot and saving the data to progress_data
            # probabl a way to track the progress of the bot more efficiently
            # but too lazy to think of a way since this algorithm is so fast
            for measGame in range(50):
                # Play 20 bot matches against the deterministic optimal bot
                # to track learning progress
                result = TQmodel_train.trainTQbot("easy", bot, updateQ = False, print_progress = False)
                if result == "won":
                    nWins += 1
                elif result == "draw":
                    nDraws += 1
                else:
                    nLosses += 1
                    
            progress_data = progress_data.append({"game_counter": game_counter, 
                           "nWins": nWins, 
                           "nDraws": nDraws, 
                           "nLosses": nLosses,
                           "winPercent": nWins / (nWins + nDraws + nLosses),
                           "drawPercent": nDraws / (nWins + nDraws + nLosses),
                           "lossPercent": nLosses / (nWins + nDraws + nLosses)}, 
                        ignore_index = True)   
        # this result isn't used but you can if you want 
        result = TQmodel_train.trainTQbot(selected_mode, bot, updateQ = True, print_progress = False)
    
    return progress_data

class botTQ(IBot):
    """ The tabular Q learning bot
    What it does is it tracks all its historic moves and keeps a dictionary with
    all past board states in hash form
    i.e q = {board_hash: qvals for the moves 1-9}
    """
    def __init__(self, alpha = 0.9, gamma = 0.95, q_init = 0.6):
        self.q = {}
        self.move_history = []
        self.learning_rate = alpha
        self.value_discount = gamma
        self.q_init_val = q_init
    
    def get_q(self, board_hash):
        """ gets the q values for the board board_hash """
        if board_hash in self.q:
            qvals = self.q[board_hash]
        else:
            qvals = [0] + [self.q_init_val for i in range(1,10)]
            self.q[board_hash] = qvals
        
        return qvals

    def GetMove(self, game, letter):
        (move, score) = self.get_move(game.getBoard(), letter)
        return move
    
    def get_move(self, board_state, letter):
        """ Takes argument board_state and letter (symbol) 
        finds the optimal move by taking the move that has the highest
        q value associated to it, returns that move
        if a move is illegal it associates the value -1.0 to that move"""
        board_hash = hash_value(board_state)
        qvals = self.get_q(board_hash)
        freeMoves = TicTacToeGame.getFreePositions(board_state)        
        
        while True:
            bestMove = np.argmax(qvals)  # type: int
            if bestMove in freeMoves:
                self.q[board_hash] = qvals
                self.move_history.append((board_hash, bestMove))
                return bestMove, qvals
            else:
                qvals[bestMove] = -1.0
     
    def update_Qfunction(self, result):
        """ Updates the Q function for the bot depending on if the bot won
        lost or drawed. With values 1, 0.5, and 0 correspondingly 
        Updates the q values according to learning rate and value discount
        Q(S,A) = Q(S, A) * (1 - lr) + lr * vd * max_a Q(S', a)
        Where A is the move on board S and Q(S', a) is the max value q for the
        next board state S'. Loops all historic moves ( in reverse ) and assigns
        new q values for all the boards S that occured during the game"""
        if result == "won":
            final_value = WIN_VALUE
        elif result == "draw":
            final_value = DRAW_VALUE
        elif result == "lost":
            final_value = LOSS_VALUE
            
        self.move_history.reverse()
        next_max = -1.0
        
        for h in self.move_history:
            qvals = self.get_q(h[0])
            m = h[1]
            
            if next_max < 0:
                qvals[m] = final_value
            else:
                qvals[m] = qvals[m] * (1.0 - self.learning_rate) + self.learning_rate * self.value_discount * next_max
            
            self.q[h[0]] = qvals                        
            next_max = max(qvals)
    
    def reset_move_history(self):
        # resets move history
        self.move_history = []
        
        
        
        
        