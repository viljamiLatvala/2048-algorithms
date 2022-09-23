# Weekly progress report - Week 3

## What has been done this week?

Started implementing MinMax -algorithm: Child state generation, heuristic function are done. Minimizer and maximizer are close to being finished. Wrote more conclusive unit tests and docstring. Generated HTML format documentation.

## How has the program progressed?

I feel good about the progression and think that it is in line with the given schedule. First two weeks for me were more about building the framework for the algorithm. This week I got into constructing the algorithm itself. This also meant more unit testing, whereas in previous week it was not done as extensively.

## What did I learn during the week?

Constructing minimax algorithm, including generation of child game states, alfa-beta pruning

## What has been causing issues/slowed down progress?

## What will be done next?

Currently minimizer and maximizer only relay the state value, this is to be modified to carry the state and the direction that leads to that state. After that the algorithm and thus the application should be totally usable and performance testing and improving/optimizing the algorithm can be started. This includes at least alpha-beta pruning and possibly taking into account the propability with which the computer player places different value tiles. After this, performance testing can be started. More testing is also needed for minimax-algorithm. Testing is currently in place but needs to be more extensive.

Some refactoring need to be done: GameHandler should likely be just a collection of helper functions rather than a class. Alternatively the functions could also be just included into the algorithm player class as well.

## Other feedback or questions to the course instructor

## Hours worked

| Day       | Hours worked | Description                                                                                                                   |
| --------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| WED 21.9. | 5            | Started creating MinMax -algorithm: Child state generation methods for MinMaxPlayer, heuristic function for evaluating states |
| FRI 23.9. | 7            | Minimizer and maximizer for minimax algorith, Documentation generation with pydoc3, Test document written                     |
