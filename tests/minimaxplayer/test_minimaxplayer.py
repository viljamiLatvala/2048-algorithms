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


class TestGenerateLeft(unittest.TestCase):
    def simple_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2], [0, 0]]
        child_state = player.generate_left(grid)
        self.assertEqual(child_state, [[4, 0], [0, 0]])

    def consecutive_merge_test(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 4], [0, 0, 2]]
        child_state = player.generate_left(grid)
        self.assertEqual(child_state, [[4, 4, 0], [2, 0, 0]])
