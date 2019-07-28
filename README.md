 # A Tic Tac Toe python game
 
 A Tic Tac Toe python game that Credits for inspiration of some of the snippets of code:
 [Code inspiration for the game basics definition](https://inventwithpython.com/chapter10.html)
 [Code inspiration for the neural network implementation](https://www.kaggle.com/dhanushkishore/a-self-learning-tic-tac-toe-program)
 
 Would like to thank the people that worked on the above! It helped me loads with writing the game.
 
 The neural network uses methods from the TensorFlow Keras modules. 
 
 Game consists of four diffent difficulty bots
 
 ### A "hard" optimal strategy bot 
 
 This bot always uses an optimal strategy. Players can at best play a draw against this bot when it's gets first turn.
 
 ** The strategy implemented assumes it has first move. But if the optimal strategy bot is playing second it should adopt a different strategy. The tabular Q bot actually manages to exploit this weakness and win half its games against the optimal strategy bot!. If the TQ bot is trained against only this bot it learns to exploit this strategy in less than 1000 games. Trained on all 3 bots it takes around 20'000 games to find the optimal strategy.**
 
 ### A semi-deterministic "easy" bot
 
 This bot plays to win when it has 2 in a row and defends when the player has 2 in a row. Otherwise plays a random move on the board.
 
 ### A pure random bot
 
 This bot plays moves from a uniform distribution of the available movesets.
 
 ### Neural network trained bot
 
 This bot is pre-trained uniformly against the hard, easy, and random bots. 
 Bot can be retrained when running the game and bots to train against can be selected.
 It has two optimal deterministic moves to improve training: Winning when it can make 3 in a row, and blocking when opponent can make 3 in a row.
 
 
 ## Issues with the SGD (stochastic gradient descent) model
 
 It takes a lot of iterations to see any effect. At 10'000 iterations the model still has not improved much. I am unsure as to why this is the case. 
 Even with two optimal moves preprogrammed it does not manage to improve over time. One would expect the drawPercentage to go to 0 if given  enough training, but this is not the case.
 
 ## Tabular Q Learning model: Second attempt at learning the Tic Tac Toe bot
 
 In the tabular Q model the bot keeps track of all its moves and adjusts values to all possible board combinations (moves) depending on the outcome of the match.
 
 The Q values are updated through Q(S, a) = (1 - k) Q(S, a) + k g  max_a' ( Q(S', a') ), with k the learning rate, g the discount factor. Based on [Carsten's blog](https://medium.com/@carsten.friedrich/part-3-tabular-q-learning-a-tic-tac-toe-player-that-gets-better-and-better-fa4da4b0892a)
 
 This model manages to figure out how to win / draw against any of the hard, easy, or random bots in about 20'000 iterations. The models algorithm is also many times faster due to its simplicity.
 
 ## The code has room for improvement
 
 The code is somewhat messy, looking back at the code I should have defined classes for the players and built it up from there. Currently only the TQ bot is a class. If anybody feels like improving the code, be my guest... It was just an exercise for me to see if I could get a tic tac toe bot to learn!
