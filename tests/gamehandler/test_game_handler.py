import pathlib
import unittest
import sys

PROJECT_SRC = str(pathlib.Path(__file__).parent.parent.parent / "src")
sys.path.append(PROJECT_SRC)
from boardfunctions.boardfunctions import Boardfunctions as board


class TestBoardfuntions(unittest.TestCase):
    def test_simple_highest_value(self):
        grid = [[0, 0, 0, 0], [0, 0, 2048, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(board.get_grid_max_value(grid), 2048)

    def test_duplicate_highest_values(self):
        grid = [[31, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 32, 32, 32]]
        self.assertEqual(board.get_grid_max_value(grid), 32)

    def test_zeroes_present_in_grid(self):
        grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertFalse(board.game_is_over(grid))

    def test_merge_possible_in_grid(self):
        grid = [[1, 2, 3, 4], [1, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        self.assertFalse(board.game_is_over(grid))

    def test_game_is_over(self):
        grid = [[1, 2, 3, 4], [2, 3, 4, 1], [1, 2, 3, 4], [2, 3, 4, 1]]
        self.assertTrue(board.game_is_over(grid))


if __name__ == "__main__":
    # unittest.main()
    grid = [[4, 2, 8, 2], [8, 32, 16, 4], [2, 256, 16, 4], [4, 16, 4, 1024]]
    print(board.move_up([grid, None]))
    print(board.move_down([grid, None]))
