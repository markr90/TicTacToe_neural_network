 # A Tic Tac Toe python game
 
 Game consists of four diffent difficulty bots
 Play the game by running "python Main.py".

 Game controls use the numpad. Each number corresponds to that respective square on the board.
 7 8 9 
 4 5 6
 1 2 3
 
 ### A "hard" optimal strategy bot 
 
 This bot always uses an optimal strategy. Players can at best play a draw against this bot when it's gets first turn.
 
 ** The strategy implemented assumes it has first move. But if the optimal strategy bot is playing second it should adopt a different strategy. The tabular Q bot actually manages to exploit this weakness and win half its games against the optimal strategy bot!. If the TQ bot is trained against only this bot it learns to exploit this strategy in less than 1000 games. Trained on all 3 bots it takes around 20'000 games to find the optimal strategy.**
 
 ### A semi-deterministic "easy" bot
 
 This bot plays to win when it has 2 in a row and defends when the player has 2 in a row. Otherwise plays a random move on the board.
 
 ### A pure random bot
 
 This bot plays moves from a uniform distribution of the available movesets.

 ### Self learning bot 

 Self learning bot uses a tabular Q learning model. Results of trainig this bot are shown in the PDF file inside this repository.
 
 ## Tabular Q Learning model bot
 
 In the tabular Q model the bot keeps track of all its moves and adjusts values to all possible board combinations (moves) depending on the outcome of the match.
 
 The Q values are updated through Q(S, a) = (1 - k) Q(S, a) + k g  max_a' ( Q(S', a') ), with k the learning rate, g the discount factor. Based on [Carsten's blog](https://medium.com/@carsten.friedrich/part-3-tabular-q-learning-a-tic-tac-toe-player-that-gets-better-and-better-fa4da4b0892a)
 
 This model manages to figure out how to win / draw against any of the hard, easy, or random bots in about 20'000 iterations. 
