# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 17:07:19 2019

@author: Mark
"""

from tictactoeBasics import freePositions
import numpy as np

WIN_VALUE = 1.0  # type: float
DRAW_VALUE = 0.5  # type: float
LOSS_VALUE = 0.0  # type: float

def hash_value(board_state):
        res = ""
        for i in range(1,10):
            res = res + board_state[i]
        return res

class botTQ(object):
    
    def __init__(self, alpha = 0.9, gamma = 0.95, q_init = 0.6):
        self.q = {}
        self.move_history = []
        self.learning_rate = alpha
        self.value_discount = gamma
        self.q_init_val = q_init
    
    def get_q(self, board_hash):
        
        if board_hash in self.q:
            qvals = self.q[board_hash]
        else:
            qvals = [0] + [self.q_init_val for i in range(1,10)]
            self.q[board_hash] = qvals
        
        return qvals
    
    def get_move(self, board_state, letter):
        board_hash = hash_value(board_state)
        qvals = self.get_q(board_hash)
        freeMoves = freePositions(board_state)
        
        
        while True:
            bestMove = np.argmax(qvals)  # type: int
            if bestMove in freeMoves:
                self.q[board_hash] = qvals
                self.move_history.append((board_hash, bestMove))
                return bestMove, qvals
            else:
                qvals[bestMove] = -1.0
     
    def update_Qfunction(self, result):
        
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
        self.move_history = []
        
        
        
        
        