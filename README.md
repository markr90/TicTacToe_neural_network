 # A Tic Tac Toe python game
 
 Code hasn't been commented yet.
 
 A Tic Tac Toe python game that Credits for inspiration of some of the snippets of code:
 [Code inspiration for the game basics definition](https://inventwithpython.com/chapter10.html)
 [Code inspiration for the neural network implementation](https://www.kaggle.com/kernels/scriptcontent/8507336/download)
 
 Would like to thank the people that worked on the above! It helped me loads with writing the game.
 
 The neural network uses methods from the TensorFlow Keras modules. 
 
 Game consists of four diffent difficulty bots
 
 ### A deterministic "hard" unbeatable bot 
 
 This bot always uses an optimal strategy. Players can at best play a draw against this bot. 
 
 ### A semi-deterministic "easy" bot
 
 This bot plays to win when it has 2 in a row and defends when the player has 2 in a row. Otherwise plays a random move on the board.
 
 ### A pure random bot
 
 This bot plays moves from a uniform distribution of the available movesets.
 
 ### Neural network trained bot
 
 This bot is pre-trained uniformly against the hard, easy, and random bots. 
 Bot can be retrained when running the game and bots to train against can be selected.
 It has two optimal deterministic moves to improve training: Winning when it can make 3 in a row, and blocking when opponent can make 3 in a row.
 
 