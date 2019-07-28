# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 16:30:51 2019

@author: Mark
"""

import random
import exitModule
import tictactoeBasics
import botDeterministic
import botSGD
import botRandom
import SGD_train
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.optimizers import SGD
import os.path



def replay():
    print("Do you want to play again (Y / N)?")
    ans = input().upper()
    
    if ans.lower() == "exit":
        exitModule.QUITGAME = True
    
    if ans == "Y":
        return True
    elif ans == "N":
        return False
    else:
        print("Not a valid choice")
        return replay()
    
def main(model):
    
    print("""Welcome to TicTacToe AI. Play TicTacToe against different kinds of bots.
          See if you are smarter than a neural network... Or if you can play a draw
          against the unbeatable hard mode bot every game!
          You can exit at any given time with <exit>.""")
    
    game = tictactoeBasics.TicTacToeGame()   
    
    while True:
        # Initialize the game
        print("""Choose your opponent 
          1) Difficulty bot: Hard
          2) Difficulty bot: Easy
          3) Random bot
          4) Self learning neural network bot (you need to train this bot first!)""")
    
        playMode = input()
        if playMode == "exit":
            print("Quitting game...")
            break
        if playMode == "4":
            if not model:
                print("Model has not been trained yet!!")
                continue
        playing = True
        game.newBoard()
        playerLetter, computerLetter = game.selectPlayer()
        if exitModule.QUITGAME:
            print("Quitting game...")
            break
        whosTurn = game.whoGoesFirst()
        print("It's", whosTurn, "turn:")
        
        while playing:
            if whosTurn == "player":
                game.drawBoard()
                print("Player's turn:")
                game.playerMove(playerLetter)
                if exitModule.QUITGAME:
                    print("Quitting game...")
                    break
                if game.isWinner(playerLetter):
                    game.drawBoard()
                    print ("Player has won the game, congratulations!")
                    playing = False
                elif game.boardFull():
                    game.drawBoard()
                    print("Too bad! Game is a tie, try again.")
                    playing = False
                else:
                    whosTurn = "computer"
            else:
                if playMode == "1":             
                    move = botDeterministic.getComputerMove(game, computerLetter, "hard")
                elif playMode == "2":
                    move = botDeterministic.getComputerMove(game, computerLetter, "easy")
                elif playMode == "3":
                    move = botRandom.getComputerMove(game, computerLetter)
                elif playMode == "4":
                    (move, new_board_state, score) = botSGD.move_selector(
                                                                model,
                                                                game.getBoard(),
                                                                computerLetter)
                    print("Bot played move:", move, "with score:", score)
                game.makeMove(computerLetter, move)
                if game.isWinner(computerLetter):
                    game.drawBoard()
                    print ("Game over! Computer has won the game.")
                    playing = False
                elif game.boardFull():
                    game.drawBoard()
                    print("Too bad! Game is a tie, try again.")
                    playing = False
                else:
                    whosTurn = "player"
        if exitModule.QUITGAME:
            break
        if not replay():
            break
        
        
model = Sequential()
model.add(Dense(18, input_dim=9,kernel_initializer='normal', activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(9, kernel_initializer='normal',activation='relu'))
model.add(Dropout(0.1))
# model.add(Dense(9, kernel_initializer='normal',activation='relu'))
# model.add(Dropout(0.1))
# model.add(Dense(5, kernel_initializer='normal',activation='relu'))
model.add(Dense(1,kernel_initializer='normal'))

learning_rate = 0.01
momentum = 0.8

sgd = SGD(lr=learning_rate, momentum=momentum, nesterov=False)
model.compile(loss='mean_squared_error', optimizer=sgd)
#model.summary()

        
def train_model(model, botsToTrain, nIterations, resolution = 10000):
    training_data = pd.DataFrame()
    progress_data = pd.DataFrame()
    game_counter = 1
    availableModes = ["hard", "easy", "random"]
    
    modes = []
    for i in botsToTrain:
        modes.append(availableModes[int(i) - 1])
        
    if len(modes) == 0:
        modes = availableModes[:]
    
    selected_mode = random.choice(modes)
    while game_counter <= nIterations:
        model, y, result = SGD_train.train(model, selected_mode, print_progress = False)
        training_data = training_data.append({"game_counter": game_counter, "result": result}, ignore_index = True)
        
        if game_counter % resolution == 1:
            print("Game #: ", game_counter)
            print("Mode:", selected_mode)
        
        if game_counter % resolution == 0:
            nWins = 0
            nDraws = 0
            nLosses = 0
            for i in range(100):   
                model, y, result = SGD_train.train(model, "easy", print_progress = False)
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
                        
            selected_mode = random.choice(modes)
            
        game_counter += 1
    return model, training_data, progress_data


if __name__ == "__main__":
    print("Do you want to train the model (Y / N)? Or use old saved model (enter \"old\")")
    toTrain = input().upper() 
    fileName = "trained_model.h5"    
    

    if toTrain == "Y":
        
        print("""Choose bots that the neural network should train against: 
          1) Difficulty bot: Hard
          2) Difficulty bot: Easy
          3) Random bot
          Pass argument of bots you want to use without spaces, for example "12", or "23".  """)
        botsToTrain = input()
        
        
        overwrite = "N"
        if os.path.isfile(fileName):
            print("File already exists, are you sure you want to overwrite? (Y / N)")
            overwrite = input().upper()
        print("How many iterations do you want to train?")
        nIts = int(input())
        print("How many bins?")
        nBins = int(input())
        model, training_data, progress_data = train_model(model, botsToTrain, nIts, resolution = nIts//nBins)
        
        fig1 = plt.figure()
        bins = np.arange(1, 20) * nIts//20
        training_data['game_counter_bins'] = np.digitize(training_data["game_counter"], bins, right=True)
        counts = training_data.groupby(['game_counter_bins', 'result']).game_counter.count().unstack()
        ax=counts.plot(kind='bar', stacked=True,figsize=(10,5))
        ax.set_xlabel("Count of Games in Bins of " + str(nIts//20) + "s")
        ax.set_ylabel("Counts of Draws/Losses/Wins")
        ax.set_title('Distribution of Results Vs Count of Games Played')
        plt.savefig("training_results.pdf")
        
        ax2 = progress_data.plot(x = "game_counter", y = ["winPercent", "drawPercent", "lossPercent"])
        plt.savefig("progress_results.pdf")
        
        if not os.path.isfile(fileName):
            model.save(fileName)            
        if overwrite == "Y":
            model.save(fileName)
    elif toTrain.lower() == "old":
        print("Loading model...")
        model = load_model(fileName)
    
    else:
        model = None
            
    main(model)
    
         
    
        