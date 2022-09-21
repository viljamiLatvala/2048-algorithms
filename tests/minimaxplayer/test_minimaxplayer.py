import pathlib
import unittest
import sys

PROJECT_SRC = str(pathlib.Path(__file__).parent.parent.parent / "src")
sys.path.append(PROJECT_SRC)

from players.minimaxplayer import MiniMaxPlayer


class TestGenerateSpawnTile(unittest.TestCase):
    def simple_test(self):
        player = MiniMaxPlayer()
        grid = [[9, 0], [0, 9]]
        child_states = player.generate_spawn_tile(grid)
        self.assertEqual(len(child_states), 4)
        self.assertEqual(child_states.count([[9, 2], [0, 9]]), 1)
        self.assertEqual(child_states.count([[9, 4], [0, 9]]), 1)
        self.assertEqual(child_states.count([[9, 0], [2, 9]]), 1)
        self.assertEqual(child_states.count([[9, 0], [4, 9]]), 1)


class TestGeneratePlayerMoveChildren(unittest.TestCase):
    def simple_test(self):
        player = MiniMaxPlayer()
        grid = [[9, 0], [0, 9]]
        child_states = player.generate_children(grid, True)
        self.assertEqual(len(child_states), 4)
        self.assertEqual(child_states.count([[9, 9], [0, 0]]), 1)
        self.assertEqual(child_states.count([[0, 0], [9, 9]]), 1)
        self.assertEqual(child_states.count([[9, 0], [9, 0]]), 1)
        self.assertEqual(child_states.count([[0, 9], [0, 9]]), 1)


class TestRotateGrid(unittest.TestCase):
    def left_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 0], [0, 4]]
        self.assertEqual(player.rotate_grid(grid, "left"), grid)

    def right_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 0], [0, 4]]
        self.assertEqual(player.rotate_grid(grid, "right"), [[0, 2], [4, 0]])

    def up_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [0, 4, 0], [0, 0, 0]]
        self.assertEqual(
            player.rotate_grid(grid, "up"), [[2, 0, 0], [2, 4, 0], [8, 0, 0]]
        )

    def down_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 8, 8]]
        self.assertEqual(
            player.rotate_grid(grid, "down"), [[8, 0, 8], [8, 4, 2], [2, 2, 2]]
        )


class TestGenerateDirection(unittest.TestCase):
    def left_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 8, 8]]
        self.assertEqual(
            player.generate_direction(grid, "left"),
            [[4, 8, 0], [2, 4, 0], [2, 16, 0]],
        )

    def right_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 8, 8]]
        self.assertEqual(
            player.generate_direction(grid, "right"), [[0, 4, 8], [0, 2, 4], [0, 2, 16]]
        )

    def down_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 8, 8]]
        self.assertEqual(
            player.generate_direction(grid, "down"), [[0, 2, 0], [2, 4, 0], [4, 8, 16]]
        )

    def up_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 0, 8]]
        self.assertEqual(
            player.generate_direction(grid, "up"), [[4, 2, 16], [2, 4, 0], [0, 0, 0]]
        )

    def consecutive_merge_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 4], [0, 0, 2]]
        child_state = player.generate_left(grid)
        self.assertEqual(child_state, [[4, 4, 0], [2, 0, 0]])


class TestHeuristicFunction(unittest.TestCase):
    def heuristic_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 4], [0, 0, 2]]
        self.assertEqual(player.heuristic(grid), 10 / 4)


if __name__ == "__main__":
    test = TestHeuristicFunction()
    test.heuristic_test()
