# Weekly progress report - Week 2

## What has been done this week?
- Configured coverage.py for following up on test coverage
- Configured pylint as linter
- GameHandler now has a function to recognize game over states
- Created first unit tests for GameHandler
- Created UserInputPlayer -class, which plays the game on users input. AI -player will be implemented using the implicit Player -interface.
- Built a simple CLI for the main app, architecture of the project is now working and utilized in app.py
- Documented some of the project with docstrings

## How has the program progressed?
I consider to have progressed fairly well on the project. The main surroundings for the AI algorithm are pretty much done aside from logging. The quantity of tests or test coverage is still very small and is to be improved. However in the first weeks effort has gone towards outer layers of the application (CLI, controlling the game via browser) where the need for high unit test coverage may not apply as directly as with the algorithm itself.

## What did I learn during the week?
I've never used test coverage tools on Python before, so that was new. I have used linters, and mainly autoformatters in a set-and-forget fashion with Python. When setting up pylint now the stock experience seems to be very strict and will require some additional configuring. 

## What has been causing issues/slowed down progress?
Had some struggles Pythons import rules when setting up unit tests and wanted the tests to run no matter where from the coverage run command is run.

## What will be done next?
First create simple logging to .CSV -files. Then start implementing the actual expectiminimax algorithm.

## Other feedback or questions to the course instructor
Are the "outer parts" like CLI and controlling the game via browser expected to be unittested with same accuracy as the actual algorithm(s)? 

## Hours worked
| Day      | Hours worked | Description |
|----------|--------------|-------------|
| THU 15.9.| 2           | Setting up unit testing, coverage reporting and linting |
| THU 15.9.| 7           | Application structuring, ManualInputPlayer for manual testing, CLI for running the program, recognizing game over state, started logging |