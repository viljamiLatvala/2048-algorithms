from browsergame.browsergame import BrowserGame
from gamehandler.gamehandler import GameHandler
from players.userinputplayer import UserInputPlayer

game = BrowserGame()
game_handler = GameHandler()
player = UserInputPlayer()
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

    game_state = game.read_grid()
    gridmax = game_handler.get_grid_max_value(game_state)
    print(f"max value: {gridmax}\n")
    print("\n".join(game_handler.get_tiles(game_state)))
