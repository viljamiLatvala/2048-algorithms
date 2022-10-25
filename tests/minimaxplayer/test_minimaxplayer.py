import pathlib
from tkinter import RIGHT
import unittest
import sys

PROJECT_SRC = str(pathlib.Path(__file__).parent.parent.parent / "src")
sys.path.append(PROJECT_SRC)
from players.minimaxplayer import MiniMaxPlayer


class TestMiniMaxPlayer(unittest.TestCase):
    def test_generate_spawn_tile(self):
        player = MiniMaxPlayer()
        grid = [[9, 0], [0, 9]]
        child_states = player.generate_spawn_tile(grid)
        self.assertEqual(len(child_states), 4)
        self.assertEqual(child_states.count([[9, 2], [0, 9]]), 1)
        self.assertEqual(child_states.count([[9, 4], [0, 9]]), 1)
        self.assertEqual(child_states.count([[9, 0], [2, 9]]), 1)
        self.assertEqual(child_states.count([[9, 0], [4, 9]]), 1)

    def test_generate_players_move_children(self):
        player = MiniMaxPlayer()
        grid = [[9, 0], [0, 9]]
        self.assertEqual(player.generate_direction(grid, "up"), [[9, 9], [0, 0]])
        self.assertEqual(player.generate_direction(grid, "down"), [[0, 0], [9, 9]])
        self.assertEqual(player.generate_direction(grid, "left"), [[9, 0], [9, 0]])
        self.assertEqual(player.generate_direction(grid, "right"), [[0, 9], [0, 9]])

    def test_rotate_grid_left(self):
        player = MiniMaxPlayer()
        grid = [[2, 0], [0, 4]]
        self.assertEqual(player.rotate_grid(grid, "left"), grid)

    def test_rotate_grid_right(self):
        player = MiniMaxPlayer()
        grid = [[2, 0], [0, 4]]
        self.assertEqual(player.rotate_grid(grid, "right"), [[0, 2], [4, 0]])

    def test_rotate_grid_up(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [0, 4, 0], [0, 0, 0]]
        self.assertEqual(player.rotate_grid(grid, "up"), [[2, 0, 0], [2, 4, 0], [8, 0, 0]])

    def test_rotate_grid_down(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 8, 8]]
        self.assertEqual(player.rotate_grid(grid, "down"), [[8, 0, 8], [8, 4, 2], [2, 2, 2]])

    def test_grid_similarity(self):
        player = MiniMaxPlayer()
        grid = [[0, 2, 0], [2, 0, 0], [0, 0, 0]]
        self.assertEqual(
            player.generate_direction(grid, "up"),
            player.generate_direction(grid, "down")[::-1],
        )
        self.assertEqual(
            player.generate_direction(grid, "left"),
            player.rotate_grid(player.generate_direction(grid, "right"), "right"),
        )

    def test_grid_similarity2(self):
        player = MiniMaxPlayer()
        grid = [[0, 2, 0], [2, 0, 0], [0, 0, 0]]
        left = player.rotate_grid(grid, "left")
        right = player.rotate_grid(grid, "right")
        up = player.rotate_grid(grid, "up")
        down = player.rotate_grid(grid, "down")
        print(f"LEFT: {left}")
        print(f"RIGHT: {right}")
        print(f"UP: {up}")
        print(f"DOWN: {down}")

    def test_generate_direction_left(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 8, 8]]
        self.assertEqual(
            player.generate_direction(grid, "left"),
            [[4, 8, 0], [2, 4, 0], [2, 16, 0]],
        )

    def test_generate_direction_right(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 8, 8]]
        self.assertEqual(player.generate_direction(grid, "right"), [[0, 4, 8], [0, 2, 4], [0, 2, 16]])

    def test_generate_direction_down(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 8, 8]]
        self.assertEqual(player.generate_direction(grid, "down"), [[0, 2, 0], [2, 4, 0], [4, 8, 16]])

    def test_generate_direction_up(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 8], [2, 4, 0], [2, 0, 8]]
        self.assertEqual(player.generate_direction(grid, "up"), [[4, 2, 16], [2, 4, 0], [0, 0, 0]])

    def test_generate_direction_consecutive_merge(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 4], [0, 0, 2]]
        child_state = player.generate_direction(grid, "left")
        self.assertEqual(child_state, [[4, 4, 0], [2, 0, 0]])

    def test_heuristic(self):
        player = MiniMaxPlayer()
        grid = [[2, 2, 4], [0, 0, 2]]
        self.assertEqual(player.heuristic(grid), 10 / 4)

    def test_minimize_reach_endstate(self):
        player = MiniMaxPlayer()
        grid = [[1, 0], [3, 4]]
        print(player.minimize(grid, 0, -9999999, 9999999))
        # 2.5

    def test_minimize_maxdepth(self):
        pass

    def test_maximize_reach_endstate(self):
        player = MiniMaxPlayer()
        grid = [[1, 10], [5, 5]]
        print(player.maximize(grid, 0, -9999999, 9999999))
        # 6.75

    def test_maximize_maxdepth(self):
        pass

    def test_play_round(self):
        player = MiniMaxPlayer()
        grid = [[1, 10], [5, 5]]
        print(player.play_round(grid))

    def test_problem_grid(self):
        player = MiniMaxPlayer()
        grid = [[4, 2, 8, 2], [8, 32, 16, 4], [2, 256, 16, 4], [4, 16, 4, 1024]]
        # grid = [[512, 2, 2, 4], [32, 128, 32, 16], [4, 4, 64, 16], [0, 16, 2, 4]]
        print(player.play_round(grid))


if __name__ == "__main__":
    # unittest.main()
    ut = TestMiniMaxPlayer()
    ut.test_problem_grid()
