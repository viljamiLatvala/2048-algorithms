import os
from browsergame.browsergame import BrowserGame
from boardfunctions.boardfunctions import Boardfunctions
from players.userinputplayer import UserInputPlayer
from players.minimaxplayer import MiniMaxPlayer
from selenium.common.exceptions import NoSuchWindowException


def clear():
    """Clears the terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def game_selection() -> object:
    """Prompts user to select what version of 2048 -game to play on

    Returns:
        object: Game -class representing the selected game
    """
    games = [BrowserGame]

    print("Select which game implementation to play on:")
    print("\t[1] - play2048.co -website (requires Chrome)")
    selection = int(input("Selection: ")) - 1
    return games[selection]


def player_selection() -> object:
    """Prompts user to select the player (algorithm) to play the game

    Returns:
        object: Player -class representing the selected player
    """
    players = [MiniMaxPlayer, UserInputPlayer]
    print("\nSelect who plays the game(s)")
    print("\t[1] - MinMaxAiPlayer")
    print("\t[2] - UserInputPlayer (You choose the moves)")
    selection = False
    while not selection:
        selection = input("Selection (1): ")
        if selection == "":
            selection = players[0]
        else:
            try:
                selection = int(selection) - 1
                selection = players[selection]
            except Exception:
                selection = False
    return selection


def game_qty_selection() -> int:
    """Prompts user to enter the quantity of consecutive rounds of 2048 to play

    Returns:
        int: Number of games to play
    """
    print("\nSelect how many games to play")
    selection = False
    while not selection:
        selection = input("Selection (1): ")
        if selection == "":
            selection = 1
        else:
            try:
                selection = int(selection)
            except Exception:
                selection = False

    return selection


def ask_iterative():
    iterative_deepening = input("Use iterative deepening? y/n (y): ")
    choice = False
    if len(iterative_deepening) == 0:
        choice = True
    elif iterative_deepening.lower() == "y":
        choice = True
    elif iterative_deepening.lower() == "n":
        choice = False
    else:
        ask_iterative()

    id_timelimit = False
    skippedturns = False

    if choice:
        while not id_timelimit:
            try:
                id_timelimit = input(
                    "Give maximum accumulated time (as float) to trigger deepening to +1 depth (0.3): "
                )
                if len(id_timelimit) == 0:
                    id_timelimit = 0.3
                else:
                    id_timelimit = float(id_timelimit)
            except Exception:
                pass

        while not skippedturns:
            try:
                skippedturns = input(
                    "Give number (as int) of rounds to not apply iterative deepening to at the start of the game (200): "
                )
                if len(skippedturns) == 0:
                    skippedturns = 200
                else:
                    skippedturns = int(skippedturns)

            except Exception:
                pass

    return {"iterative_deepening": choice, "id_timelimit": id_timelimit, "skippedturns": skippedturns}


def algorithm_settings():
    return {"deepening": ask_iterative()}


if __name__ == "__main__":
    clear()
    print("Welcome to 2048-algorithms!")
    print("First, choose how you wish to run the application", end="\n\n")

    player = player_selection()
    games_to_play = game_qty_selection()
    settings = {}
    if player.__dict__["__module__"] == "players.minimaxplayer":
        settings = ask_iterative()
    print("Thank you, onto the games then!")
    print("\n\n\n\n\n")

    game = BrowserGame()
    player = player()

    game_no = 1
    while game_no <= games_to_play:
        print("starting up the loop")
        max_score = 0
        turn_count = 0
        player.round_count = 0

        game.start_game()
        game_state = game.read_grid()
        while not Boardfunctions.game_is_over(game_state):
            try:
                if player.__class__.__name__ == "MiniMaxPlayer":
                    next_move = player.play_round(
                        game_state, settings["iterative_deepening"], settings["id_timelimit"], settings["skippedturns"]
                    )
                else:
                    next_move = player.play_round(game_state)

                if next_move == "up":
                    game.move_up()
                elif next_move == "down":
                    game.move_down()
                elif next_move == "left":
                    game.move_left()
                elif next_move == "right":
                    game.move_right()

                turn_count += 1

                game_state = game.read_grid()
                gridmax = Boardfunctions.get_grid_max_value(game_state)
                if gridmax > max_score:
                    max_score = gridmax
            except NoSuchWindowException:
                print("The browser window has been closed")
                break

        game.quit_game()
        print(f"Game {game_no}/{games_to_play} over! Score: {max_score}, played_turns: {turn_count}")
        game_no += 1
