# Implementation Document

## Project structure

Project is divided into severall classes with different purpose. These classes are:

### BrowserGame

This is the class which interfaces to play2048.co -website via selenium. It provides methods to move the tiles and to read the games state

### MiniMaxPlayer

This class represents the AI which plays the game using MiniMax -algorithm. It has a function play_round that is given the game's state and returns the direction which to play next.

### UserInputPlayer

Another class representing a player. This class was used for testing browser controls & basic application funtionality. Its play_round function simply prompts user for the next move and relays that to the app.py's main loop.

### GameHandler

This class acts as a collection of functions used by both the app.py -file and MiniMaxPlayer -class. These are simple functions to get information about the game grid

In addition to these classes. The game has its main file, the app.py which is used to launch the application. It provides simple UI to select how to run the application and controls the applications main loop which plays N games given by users input. Launches the game, reads its state and calls selected Player -classes play_round function with that state as input.

## Accomplished Big-O Time & Space Complexities

TBD

## Development Ideas / Next Steps

TBD

## References

https://en.wikipedia.org/wiki/2048_(video_game)#AI
https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Expectiminimax
https://stanford-cs221.github.io/autumn2019-extra/posters/184.pdf
https://theresamigler.files.wordpress.com/2020/03/2048.pdf
