import pathlib
import unittest
import sys

PROJECT_SRC = str(pathlib.Path(__file__).parent.parent.parent / "src")
sys.path.append(PROJECT_SRC)

from game_handler.game_handler import GameHandler


class TestGameHandler(unittest.TestCase):
    def test_get_grid_max_value(self):
        game_handler = GameHandler()
        grid = [[0, 0, 0, 0], [0, 0, 2048, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        self.assertEqual(game_handler.get_grid_max_value(grid), 2048)


if __name__ == "__main__":
    unittest.main()
