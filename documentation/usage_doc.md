# Usage

Follow the steps below to succesfully run the program. To run the program you'll need Python (developed on 3.10.6) with pip and Google Chrome browser. If you don't wish to use Chrome, it is likely very simple to change the Selenium webdriver in browsergame.py to suit your wishes.

Clone the repository and navigate to the project folder:

```
> git clone https://github.com/viljamiLatvala/2048-algorithms.git
Cloning into '2048-algorithms'...
> cd 2048-algorithms
```

Install requirements:

```
> python -m pip install -r requirements.txt
```

Run the app.py -file:

```
> python src/app.py
```

The program should now execute. You are met with a few questions to determine how to run the algorithm. Default settings are fine, to see the game play to 2048 as fast as possible the number of rounds to skip iterative deepening can be set to around 750.

Once the selections are made the program opens up chrome browser and starts to play the game. You can inspect the game in browser and read the output that summarizes each round. Once the game is lost the browser is closed and the application exits. To stop the application mid-run use ctrl+c or close the controlled browser window.
