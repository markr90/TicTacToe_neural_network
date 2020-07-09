        
import botTQ
from TicTacToeGame import TicTacToeGame
import TQmodel_train
import pandas as pd
import matplotlib.pyplot as plt   


if __name__ == "__main__":
    """ Main script execution. Asks if usere wants to train the bot
    then trains the bot if yes
    afterwards user can play against the bot"""
    
    print("Do you want to train the model (Y / N)?")
    toTrain = input()
    
    # define bot
    botAlice = botTQ.botTQ()
    
    # train the bot
    if toTrain.lower() == "y":
        
        print("How many iterations do you want to train?")
        nIts = int(input())
        
        progress_data = botTQ.train_model(botAlice, nIts)
        # Save results in graph on local folder
        ax2 = progress_data.plot(x = "game_counter", y = ["winPercent", "drawPercent", "lossPercent"])
        plt.savefig("TQPlayer_progress_results.pdf")
    
    # Let the player play against any of the bots   
    game = TicTacToeGame(botAlice)     
    game.play()