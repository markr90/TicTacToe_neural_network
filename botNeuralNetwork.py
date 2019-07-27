# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 20:36:12 2019

@author: Mark
"""

import numpy as np
import tictactoeBasics

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import SGD

model = Sequential()
model.add(Dense(18, input_dim=9,kernel_initializer='normal', activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(9, kernel_initializer='normal',activation='relu'))
model.add(Dropout(0.1))
# model.add(Dense(9, kernel_initializer='normal',activation='relu'))
# model.add(Dropout(0.1))
# model.add(Dense(5, kernel_initializer='normal',activation='relu'))
model.add(Dense(1,kernel_initializer='normal'))

learning_rate = 0.001
momentum = 0.8

sgd = SGD(lr=learning_rate, momentum=momentum,nesterov=False)
model.compile(loss='mean_squared_error', optimizer=sgd)
#model.summary()

def board_integer_representation(board):
    boardArray = []
    for i in range(1, 10):
        if board[i] == " ":
            boardArray.append(0)
        elif board[i] == "X":
            boardArray.append(1)
        else:
            boardArray.append(2)
    return np.array(boardArray)
            

def move_selector(model, board, letter):
    """"Function that selects the next move based on a set of legal moves
    Args: evaluator model, current board state board, and turn indicator letter
    Returns selected move integer between 1 and 9 that indicates position on board
    corresponding to numpad of a keyboard"""
    
    tracker = {}
    legal_moves_dict = tictactoeBasics.legal_moves_generator(board, letter)
    for legal_move in legal_moves_dict:
        
        boardArray = board_integer_representation(legal_moves_dict[legal_move])
        score = model.predict(boardArray.reshape(1,9))
        tracker[legal_move] = score
        
    selected_move = max(tracker, key = tracker.get)
    new_board_state = legal_moves_dict[selected_move]
    score = tracker[selected_move]
    return selected_move, new_board_state, score