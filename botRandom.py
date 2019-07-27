# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 22:44:58 2019

@author: Mark
"""

import tictactoeBasics
import random

def getComputerMove(runningGame, letter):
    
    freespots = tictactoeBasics.freePositions(runningGame.getBoard())
    
    move = random.choice(freespots)
    return move
    