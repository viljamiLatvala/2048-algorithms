# Implementation Document

## Project structure

Project is divided into severall classes and modules with different purpose. These are:

### BrowserGame

This is the class which interfaces to play2048.co -website via selenium. It provides methods to move the tiles and to read the games state

### MiniMaxPlayer

This class represents the AI which plays the game using MiniMax -algorithm. It has a function play_round that is given the game's state and returns the direction which to play next.

### UserInputPlayer

Another class representing a player. This class was used for testing browser controls & basic application funtionality. Its play_round function simply prompts user for the next move and relays that to the app.py's main loop.

### boardfunctions

This module acts as a collection of functions used by both the app.py -file and MiniMaxPlayer -class. These are simple functions to get information and interact with the about the game grid

In addition to these classes. The game has its main file, the app.py which is used to launch the application. It provides simple UI to select how to run the application and controls the applications main loop which plays N games given by users input. Launches the game, reads its state and calls selected Player -classes play_round function with that state as input.

## Accomplished Big-O Time & Space Complexities

### Branching factor

The branching factor of the game tree varies based on whose moves the layer of nodes represents and how many empty tiles are there on the game board. The player usually has 4 moves available for them, with the exception of having a direction where moving there does not alter the board: these moves are not possible. The "computer" has two possible moves for each empty tile on the game grid. This ranges from 2\*15 in cases where there is only one tile on the board to 0 in cases when the board is full of tiles but still playable.

### Time and Space Complexity

The worst case time complexity of the minimax algorithm is O(m^d) where m is the available moves (branching factor) on each turn and d is the used search depth. The m is determined by the brancing factor explained above. Due to iterative deepening the search depth varies from 2 full-turns (= 4 half-turns) up. A new level is calculated if the time calculating the ongoing round has not passed 0.3 seconds when the maximizer returns the search result. The big-o complexity is not affected by the alpha beta pruning since in the worst case all nodes will be explored. The worst case space complexity for the algorithm is O(MD)

### Evaluation Heuristic

Having a meaningful evaluation function is critical for the AI to maintain the board in a decent shape. An evaluation that is solely aiming to maximize empty space or the highest tile leads to moves that allow the computer player to spawn tiles so that the small and high value tiles are highly mixed, preventing future merges.

When designing the heuristic the base thought was that the goal of the game is to survive as long as possible, and as the game progresses your outlook of survival decreases. Therefore it is only natural that the evaluation scores are negative and tend to get more negative as the game progresses.

To emphasize tile placement I count for each horizontal and column the accumulated absolute difference between the tiles in that set of four tiles, and take the negative of that. This values boards where the difference between neighboring tiles is as little as possible and is quite fast to calculate for each evaluation.

To emhasize board emptiness, the score calculated before is multiplied by the quantity of tiles present on the board.

## References

https://en.wikipedia.org/wiki/2048_(video_game)#AI
https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Expectiminimax
https://stanford-cs221.github.io/autumn2019-extra/posters/184.pdf
https://theresamigler.files.wordpress.com/2020/03/2048.pdf
