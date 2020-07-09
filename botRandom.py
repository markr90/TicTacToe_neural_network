# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 22:44:58 2019

@author: Mark
"""

import random
import TicTacToeGame
from IBot import IBot

class botRandom(IBot):
    def GetMove(self, runningGame, letter):        
        freespots = TicTacToeGame.getFreePositions(runningGame.getBoard())        
        move = random.choice(freespots)
        return move
    