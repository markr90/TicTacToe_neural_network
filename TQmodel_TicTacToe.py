# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 16:30:51 2019

@author: Mark
"""

import random
import exitModule
import tictactoeBasics
import botDeterministic
import botTQ
import botRandom
import TQmodel_train
import pandas as pd
import matplotlib.pyplot as plt



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
    
def main(bot, updateQ = True):
    
    print("""Welcome to TicTacToe AI. Play TicTacToe against different kinds of bots.
          See if you are smarter than a TQ bot... Or if you can play a draw
          against the unbeatable hard mode bot every game!
          You can exit at any given time with <exit>.""")
    
    game = tictactoeBasics.TicTacToeGame()   
    
    while True:
        # Initialize the game
        print("""Choose your opponent 
          1) Difficulty bot: Hard
          2) Difficulty bot: Easy
          3) Random bot
          4) Self learning TQ bot """)
    
        playMode = input()
        if playMode == "exit":
            print("Quitting game...")
            break
        playing = True
        game.newBoard()
        playerLetter, computerLetter = "X", "O"
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
                    game_status = "lost"
                    print ("Player has won the game, congratulations!")
                    playing = False
                elif game.boardFull():
                    game.drawBoard()
                    game_status = "draw"
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
                    (move, score) = bot.get_move(game.getBoard(), computerLetter)
                game.makeMove(computerLetter, move)
                if game.isWinner(computerLetter):
                    game.drawBoard()
                    game_status = "won"
                    print ("Game over! Computer has won the game.")
                    playing = False
                elif game.boardFull():
                    game.drawBoard()
                    game_status = "draw"
                    print("Too bad! Game is a tie, try again.")
                    playing = False
                else:
                    whosTurn = "player"
                    
        if updateQ:
            bot.update_Qfunction(game_status)
        bot.reset_move_history()
        if exitModule.QUITGAME:
            break
        if not replay():
            break
        
        
      
def train_model(bot, botsToTrain, nIterations, resolution = 50):
    progress_data = pd.DataFrame()
    availableModes = ["hard", "easy", "random"]
    modes = []
    for i in botsToTrain:
        modes.append(availableModes[int(i) - 1])
    if len(modes) == 0:
        modes = availableModes[:]  
    selected_mode = random.choice(modes)
    
    for game_counter in range(nIterations):
        if game_counter % resolution == 0:
            print("Game #: ", game_counter)
            print("Mode:", selected_mode)
            selected_mode = random.choice(modes)
            
            nWins = 0
            nDraws = 0
            nLosses = 0
            
            for measGame in range(50):
                # Play 20 bot matches against the deterministic optimal bot
                # to track learning progress
                result = TQmodel_train.trainTQbot("hard", bot, updateQ = False, print_progress = False)
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
        
        result = TQmodel_train.trainTQbot(selected_mode, bot, updateQ = True, print_progress = False)
    
    return progress_data
        
        
        


if __name__ == "__main__":
    print("Do you want to train the model (Y / N)?")
    toTrain = input().upper()
    
    botAlice = botTQ.botTQ()
    

    if toTrain == "Y":
        print("""Choose bots that the neural network should train against: 
          1) Difficulty bot: Hard
          2) Difficulty bot: Easy
          3) Random bot
          Pass argument of bots you want to use without spaces, for example "12", or "23".  """)
        botsToTrain = input()
        
        print("How many iterations do you want to train?")
        nIts = int(input())
        
        progress_data = train_model(botAlice, botsToTrain, nIts)
        
        ax2 = progress_data.plot(x = "game_counter", y = ["winPercent", "drawPercent", "lossPercent"])
        plt.savefig("TQPlayer_progress_results.pdf")
            
    main(botAlice)
    
         
    
        