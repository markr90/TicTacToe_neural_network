# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 16:30:51 2019

@author: Mark
"""

import random
import exitModule
import tictactoeBasics
import botDeterministic
import botNeuralNetwork
import botRandom
import train
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
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
                    (move, new_board_state, score) = botNeuralNetwork.move_selector(
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
        
def train_model(model, nIterations, resolution = 10000):
    training_data = pd.DataFrame()
    game_counter = 1
    modes = ["deterministic", "random"]
    while game_counter <= nIterations:
        selected_mode = random.choice(modes)
        model, y, result = train.train(model, selected_mode, print_progress = False)
        training_data = training_data.append({"game_counter": game_counter, "result": result}, ignore_index = True)
        if game_counter % resolution == 0:
            print("Game #: ", game_counter)
        game_counter += 1
    return model, training_data


if __name__ == "__main__":
    print("Do you want to train the model (Y / N)? Or use old saved model (enter \"old\")")
    toTrain = input().upper() 
    fileName = "trained_model.h5"    
    

    if toTrain == "Y":
        overwrite = "N"
        if os.path.isfile(fileName):
            print("File already exists, are you sure you want to overwrite? (Y / N)")
            overwrite = input().upper()
        print("How many iterations do you want to train?")
        nIts = int(input())
        print("How many bins?")
        nBins = int(input())
        model = botNeuralNetwork.model
        model, training_data = train_model(model, nIts, resolution = nIts//nBins)
        
        bins = np.arange(1, nBins) * nIts//nBins
        training_data['game_counter_bins'] = np.digitize(training_data["game_counter"], bins, right=True)
        counts = training_data.groupby(['game_counter_bins', 'result']).game_counter.count().unstack()
        ax=counts.plot(kind='bar', stacked=True,figsize=(10,5))
        ax.set_xlabel("Count of Games in Bins of " + str(nIts//nBins) + "s")
        ax.set_ylabel("Counts of Draws/Losses/Wins")
        ax.set_title('Distribution of Results Vs Count of Games Played')
        plt.savefig("training_results.pdf")
        
        if not os.path.isfile(fileName):
            model.save(fileName)            
        if overwrite == "Y":
            model.save(fileName)
    elif toTrain.lower() == "old":
        print("Loading model...")
        model = load_model(fileName)
    
    else:
        model = None
            
    if not model:
        main(model)
    else:
        main(model)
    
         
    
        