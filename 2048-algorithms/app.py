from browser_game.browser_game import BrowserGame
from game_handler.game_handler import GameHandler

game = BrowserGame()
game_handler = GameHandler()

game.start_game()
max = game_handler.get_grid_max_value(game.read_grid())
print(max)