import pathlib
import unittest
import sys
import random

PROJECT_SRC = str(pathlib.Path(__file__).parent.parent.parent / "src")
sys.path.append(PROJECT_SRC)
from boardfunctions.boardfunctions import Boardfunctions as board


class TestGameIsOver(unittest.TestCase):
    def test_not_over_empty(self):
        state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertFalse(board.game_is_over(state))

    def test_not_over_not_full(self):
        state = [[0, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [1024, 512, 256, 128]]
        self.assertFalse(board.game_is_over(state))

    def test_not_over_full_but_merges(self):
        state = [[1, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 1024], [1024, 512, 256, 128]]
        self.assertFalse(board.game_is_over(state))

    def test_over(self):
        state = [[4, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [16, 32, 64, 128]]
        self.assertTrue(board.game_is_over(state))


class TestGetGridMaxValue(unittest.TestCase):
    def test_one_highest_value(self):
        state = [[0, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 2048], [1024, 512, 256, 128]]
        self.assertEqual(board.get_grid_max_value(state), 2048)

    def test_multiple_highest_values(self):
        state = [[0, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 1024], [1024, 512, 256, 128]]
        self.assertEqual(board.get_grid_max_value(state), 1024)


class TestCopyGrid(unittest.TestCase):
    def test_empty_grid(self):
        state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(board.copy_grid(state), state)

    def test_sample_grid(self):
        state = [[0, 2, 4, 8], [16, 32, 64, 128], [256, 512, 1024, 1024], [1024, 512, 256, 128]]
        self.assertEqual(board.copy_grid(state), state)

    def test_multiple(self):
        for _ in range(100):
            state = []
            for x in range(4):
                state.append([0, 0, 0, 0])
                for y in range(4):
                    state[x][y] = 2 ** random.randint(1, 11)

            self.assertEqual(board.copy_grid(state), state)


class TestMovement(unittest.TestCase):
    def test_no_merges_left(self):
        state = [[0, 0, 0, 0], [0, 2, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        newstate, empties = board.move_left((state, None))
        self.assertEqual(newstate, [[0, 0, 0, 0], [2, 4, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertEqual(
            empties,
            [
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 2),
                (1, 3),
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (3, 0),
                (3, 1),
                (3, 2),
                (3, 3),
            ],
        )

    def test_no_merges_right(self):
        state = [[0, 0, 0, 0], [0, 2, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        newstate, empties = board.move_right((state, None))
        self.assertEqual(newstate, [[0, 0, 0, 0], [0, 0, 2, 4], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertEqual(
            empties,
            [
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 0),
                (1, 1),
                (2, 0),
                (2, 1),
                (2, 2),
                (2, 3),
                (3, 0),
                (3, 1),
                (3, 2),
                (3, 3),
            ],
        )

    def test_no_merges_up(self):
        state = [[0, 0, 0, 0], [0, 2, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        newstate, empties = board.move_up((state, None))
        self.assertEqual(newstate, [[0, 2, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertEqual(
            empties,
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (1, 1),
                (2, 1),
                (3, 1),
                (1, 2),
                (2, 2),
                (3, 2),
                (0, 3),
                (1, 3),
                (2, 3),
                (3, 3),
            ],
        )

    def test_no_merges_down(self):
        state = [[0, 0, 0, 0], [0, 2, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        newstate, empties = board.move_down((state, None))
        self.assertEqual(newstate, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 2, 4, 0]])
        self.assertEqual(
            empties,
            [
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (0, 1),
                (1, 1),
                (2, 1),
                (0, 2),
                (1, 2),
                (2, 2),
                (0, 3),
                (1, 3),
                (2, 3),
                (3, 3),
            ],
        )

    def test_merge_horizontal(self):
        state = [[0, 0, 0, 0], [0, 2, 2, 0], [0, 4, 4, 0], [0, 2, 2, 0]]
        # Left
        state_l, empties_l = board.move_left((state, None))
        self.assertEqual(state_l, [[0, 0, 0, 0], [4, 0, 0, 0], [8, 0, 0, 0], [4, 0, 0, 0]])
        self.assertEqual(
            empties_l,
            [
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
                (1, 1),
                (1, 2),
                (1, 3),
                (2, 1),
                (2, 2),
                (2, 3),
                (3, 1),
                (3, 2),
                (3, 3),
            ],
        )

        # Right
        state_r, empties_r = board.move_right((state, None))
        self.assertEqual(state_r, [[0, 0, 0, 0], [0, 0, 0, 4], [0, 0, 0, 8], [0, 0, 0, 4]])
        self.assertEqual(
            empties_r,
            [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)],
        )

    def test_merge_vertical(self):
        state = [[0, 0, 0, 4], [0, 2, 2, 0], [0, 2, 2, 4], [0, 0, 0, 0]]
        # Up
        state_u, empties_u = board.move_up((state, None))
        self.assertEqual(state_u, [[0, 4, 4, 8], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.assertEqual(
            empties_u,
            [(0, 0), (1, 0), (2, 0), (3, 0), (1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)],
        )
        # Down
        state_d, empties_d = board.move_down((state, None))
        self.assertEqual(state_d, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 4, 4, 8]])
        self.assertEqual(
            empties_d,
            [(0, 0), (1, 0), (2, 0), (3, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (0, 3), (1, 3), (2, 3)],
        )

    def test_multiple_merges_horizontal(self):
        state = [[0, 0, 0, 0], [2, 2, 2, 2], [2, 2, 2, 2], [0, 0, 0, 0]]
        # Left
        state_l, empties_l = board.move_left((state, None))
        self.assertEqual(state_l, [[0, 0, 0, 0], [4, 4, 0, 0], [4, 4, 0, 0], [0, 0, 0, 0]])
        # Right
        state_r, empties_r = board.move_right((state, None))
        self.assertEqual(state_r, [[0, 0, 0, 0], [0, 0, 4, 4], [0, 0, 4, 4], [0, 0, 0, 0]])

    def test_multiple_merges_vertical(self):
        state = [[0, 2, 2, 0], [0, 2, 2, 0], [0, 2, 2, 0], [0, 2, 2, 0]]
        # Up
        state_u, empties_u = board.move_up((state, None))
        self.assertEqual(state_u, [[0, 4, 4, 0], [0, 4, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        # Down
        state_d, empties_d = board.move_down((state, None))
        self.assertEqual(state_d, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 4, 4, 0], [0, 4, 4, 0]])


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
    unittest.main()
