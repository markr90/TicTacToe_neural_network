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
    """Queries the player if it wants to replay again, returns boolean depending
    on the players response"""
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
    """The main tictactoe game. Players can choose what bot they want to play against
    the function has multiple points where players can provide input"""
    
    print("""Welcome to TicTacToe AI. Play TicTacToe against different kinds of bots.
          See if you are smarter than a TQ bot... Or if you can play a draw
          against the unbeatable hard mode bot every game!
          You can exit at any given time with <exit>.""")
    
    # Initialize the game classs
    game = tictactoeBasics.TicTacToeGame()   
    
    while True:
        # Ask what bot the player wants to play against
        print("""Choose your opponent 
          1) Difficulty bot: Hard
          2) Difficulty bot: Easy
          3) Random bot
          4) Self learning TQ bot """)
        playMode = input()
        # if exit command is given exit
        if playMode == "exit":
            print("Quitting game...")
            break
        # some initialization values
        playing = True
        game.newBoard()
        playerLetter, computerLetter = "X", "O"
        whosTurn = game.whoGoesFirst()
        print("It's", whosTurn, "turn:")
        
        # The actual game
        while playing:
            if whosTurn == "player":
                game.drawBoard()
                print("Player's turn:")
                game.playerMove(playerLetter)
                if exitModule.QUITGAME:
                    print("Quitting game...")
                    break
                # check if win / draw conditions are met otherwise give turn
                # to next player
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
                # check if win / draw conditions are met otherwise give turn
                # to next player
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
        # Update bot Q function             
        if updateQ:
            bot.update_Qfunction(game_status)
        bot.reset_move_history()
        if exitModule.QUITGAME:
            break
        if not replay():
            break
        
        
      
def train_model(bot, botsToTrain, nIterations, resolution = 50):
    """args
    bot: the bot to be trained
    botsToTrain: list of bots you want to train against in string format 
        for example "123" is against bots 1 2 and 3
    nIterations how many training iterations do you want to do
    approximately 20'000 are needed to train against all 3 bots
    resolution is the distance between the points in the training graph
    in the x axis (game_counter axis)
    
    returns the training progress dataframe progress_data"""
    
    # Track training progress
    progress_data = pd.DataFrame()
    # Define bots to train against
    availableModes = ["hard", "easy", "random"]
    modes = []
    for i in botsToTrain:
        modes.append(availableModes[int(i) - 1])
    if len(modes) == 0:
        modes = availableModes[:]  
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
        
        
        


if __name__ == "__main__":
    """ Main script execution. Asks if usere wants to train the bot
    then trains the bot if yes
    afterwards user can play against the bot"""
    
    print("Do you want to train the model (Y / N)?")
    toTrain = input().upper()
    
    # define bot
    botAlice = botTQ.botTQ()
    
    # train the bot
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
        # Save results in graph on local folder
        ax2 = progress_data.plot(x = "game_counter", y = ["winPercent", "drawPercent", "lossPercent"])
        plt.savefig("TQPlayer_progress_results.pdf")
    
    # Let the player play against any of the bots        
    main(botAlice)
    
         
    
        