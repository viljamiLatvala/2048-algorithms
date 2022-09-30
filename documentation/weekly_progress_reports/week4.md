# Weekly progress report - Week 4

## What has been done this week?

Finished MiniMax to be capable of playing the game, created dynamic generation of child states, optimized child state generation on game's turn. Attempted performance increases

## How has the program progressed?

Functionality wise the program progressed fine, is now intact and usable. With the search depth of 5 the algorithm is capable of playing faster than move per second (on mine and department's PC's anyway) With the depth of 6 it is very close to 1 second average but individual moves might take up to 5 seconds. The game has been able to reach the score of 2048 but does not do this consistently.

## What did I learn during the week?

I deepened my shallow understanding about minimax & A/B -pruning and learned about various possibilities to boost algorithm performance.

## What has been causing issues/slowed down progress?

Finding actual performance boosting optimizations. Some work marginally, others seem to require calculation that eats the possible performance gains elsewhere.

## What will be done next?

Algorithms search depth could still be improved. Sorting play -directions for player and game to boost A/B -pruning performance would propably be the most efficient way. Speed of copying, altering and comparing lists and 2-d lists could be looked into.

In addition tweaks to the heuristic function should be tested to see if they yield better results.

## Other feedback or questions to the course instructor

In this course, is Python List treated as comparable to for example Java's array despite giving slighly more inbuilt features, in other words can the final application use it and its methods or should it be replaced with other or own data structure? Could there be possible performance advantages in using some other data structure (for example tuple -based) giving?

## Hours worked

| Day       | Hours worked | Description                                                                      |
| --------- | ------------ | -------------------------------------------------------------------------------- |
| WED 28.9. | 7            | Finished MiniMax to be capable of playing the game, added a/b -pruning           |
| THU 29.9. | 2            | Dynamic generation of child states                                               |
| FRI 30.9. | 7            | Optimized child state generation on game's turn. Attempted performance increases |
