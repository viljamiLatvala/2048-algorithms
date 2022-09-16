import os
import time
import csv

from browsergame.browsergame import BrowserGame
from gamehandler.gamehandler import GameHandler
from players.userinputplayer import UserInputPlayer


def clear():
    """Clears the terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def game_selection():
    games = [BrowserGame]

    print("Select which game implementation to play on:")
    print("\t[1] - BrowserGame (play2048.co -website)")
    print("\t[2] - HeadlessGame [TODO] (UI-less implementation)")
    selection = int(input("Selection: ")) - 1
    return games[selection]


def player_selection():
    players = [UserInputPlayer]
    print("\nSelect who plays the game(s)")
    print("\t[1] - UserInputPlayer (You choose the moves)")
    print("\t[2] - MinMaxAiPlayer [TODO]")
    selection = int(input("Selection: ")) - 1
    return players[selection]


def game_qty_selection():
    print("\nSelect how many games to play")
    selection = int(input("Selection: "))
    return selection


clear()
print("Welcome to 2048-algorithms!")
print("First, choose how you wish to run the application", end="\n\n")
print("Select which game implementation to play on:")

# [TODO] could also just use static classes?
game = game_selection()
player = player_selection()
games_to_play = game_qty_selection()
print("Thank you, onto the games then!")

game_handler = GameHandler()
game = game()
player = player()

logfile = open("logs.csv", "a", encoding="utf-8")
logwriter = csv.writer(logfile)
logheaders = [
    "event",
    "timestamp",
    "player",
    "game",
    "run_id",
    "run_id_custom",
    "highest_tile",
    "moves_count",
    "time_spent",
    "game_state",
]
logwriter.writerow(logheaders)

for game_no in range(games_to_play):

    max_score = 0
    turn_count = 0

    game.start_game()
    game_state = game.read_grid()
    while not game_handler.game_is_over(game_state):
        next_move = player.play_round(game_state)

        if next_move == "Up":
            game.move_up()
        elif next_move == "Down":
            game.move_down()
        elif next_move == "Left":
            game.move_left()
        elif next_move == "Right":
            game.move_right()

        turn_count += 1

        game_state = game.read_grid()
        gridmax = game_handler.get_grid_max_value(game_state)
        if gridmax > max_score:
            max_score = gridmax

    game.quit_game()
    print(
        f"Game {game_no + 1}/{games_to_play} over! Score: {max_score}, played_turns: {turn_count}"
    )

logfile.close()
