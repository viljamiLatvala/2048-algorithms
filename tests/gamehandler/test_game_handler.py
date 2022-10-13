import pathlib
import unittest
import sys

PROJECT_SRC = str(pathlib.Path(__file__).parent.parent.parent / "src")
sys.path.append(PROJECT_SRC)
from gamehandler.boardfunctions import GameHandler


class TestGameHandler(unittest.TestCase):
    def test_simple_highest_value(self):
        game_handler = GameHandler()
        grid = [[0, 0, 0, 0], [0, 0, 2048, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(game_handler.get_grid_max_value(grid), 2048)

    def test_duplicate_highest_values(self):
        game_handler = GameHandler()
        grid = [[31, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 32, 32, 32]]
        self.assertEqual(game_handler.get_grid_max_value(grid), 32)

    def test_zeroes_present_in_grid(self):
        game_handler = GameHandler()
        grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertFalse(game_handler.game_is_over(grid))

    def test_merge_possible_in_grid(self):
        game_handler = GameHandler()
        grid = [[1, 2, 3, 4], [1, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        self.assertFalse(game_handler.game_is_over(grid))

    def test_game_is_over(self):
        game_handler = GameHandler()
        grid = [[1, 2, 3, 4], [2, 3, 4, 1], [1, 2, 3, 4], [2, 3, 4, 1]]
        self.assertTrue(game_handler.game_is_over(grid))


if __name__ == "__main__":
    unittest.main()
