# Project definition document - 2048-algorithms
This project is done for University of Helsinki's course TKT20010 which I am participating as a student in the TKT -programme.

## Project Topic and Scope
For my coursework I will implement a program where AI attemps to solve 2048 puzzles. The program will be implemented in Python.

The goal is to produce an algorithm that plays 2048 on the standard 4x4 grid as well as possible, with a goal of producing a tile with as large value as possible.

The algorithm to implement will be an minimax algorithm with alpha-beta pruning or an minimax variant expectiminimax. Creation of such algorithm also requires the creation of a tree data structure.

The big-O complexity of such algorithm should be 0(b^d) where b is the branching factor and d is the used search depth. For 2048 the branching factor is defined by possible player-moves up, down, left right (4) and possible generated new tiles by the game. New tiles can be either 2 or 4 and spawned in to any free slot on the game grid. Since there is always at least one occupied slot in the grid, the maximum number of possible moves for the game is 30. The minimum is having one free slot on the grid and spawing either a 2 or a 4, resulting in 2 possible moves by the game. The branching factor for one full round will vary between 8 and 120.

I chose this topic for a couple of reasons. Firstly, based on the idea to explore game AI creation seemed interesting and having many interesting applications. Second, I wanted to avoid selecting a topic that would require alot of time to be used in gathering background knowledge and setting up suitable environment (UI, input-system, output formats etc.) to even begin develop such algorithm. As 2048 is an already somewhat familiar game and I believe my past experience allows me to get into building the actual algorithm quicker, it seemed as a good fit for a project topic.

## Implementation and Peer Review Languages
The program will be implemented in Python. If needed, I am also able to peer review Java programs. 

## References
https://en.wikipedia.org/wiki/2048_(video_game)#AI
https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
https://en.wikipedia.org/wiki/Minimax
https://en.wikipedia.org/wiki/Expectiminimax
https://stanford-cs221.github.io/autumn2019-extra/posters/184.pdf