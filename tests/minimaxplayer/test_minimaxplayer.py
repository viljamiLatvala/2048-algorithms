from http.client import ImproperConnectionState
import pathlib
from tkinter import RIGHT
import unittest
import sys
from io import StringIO

PROJECT_SRC = str(pathlib.Path(__file__).parent.parent.parent / "src")
sys.path.append(PROJECT_SRC)
from players.minimaxplayer import MiniMaxPlayer


class TestGenerateSpawnChild(unittest.TestCase):
    def setUp(self):
        self.player = MiniMaxPlayer()
        self.player.filename = "unittests.txt"

    def test_generation(self):
        state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        newstate = self.player.generate_spawn_child(state, (0, 0), 2)
        self.assertEqual(newstate, [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

        self.assertEqual(
            self.player.generate_spawn_child(newstate, (3, 3), 4),
            [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 4]],
        )


class TestHeuristic(unittest.TestCase):
    def setUp(self) -> None:
        self.player = MiniMaxPlayer()
        self.player.filename = "unittests.txt"

    def test_empty(self):
        state = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(self.player.heuristic(state), 0)

    def test_filled(self):
        state = [[2, 2, 2, 2], [2, 4, 6, 2], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.assertEqual(self.player.heuristic(state), -(14 * 8))

    def test_game_over(self):
        state = [[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2048, 4096], [8192, 16384, 32768, 65536]]
        self.assertEqual(self.player.heuristic(state), -999999)


class TestLogWrite(unittest.TestCase):
    def setUp(self) -> None:
        self.player = MiniMaxPlayer()
        self.player.filename = "unittests.txt"

    def test_logwrite(self):
        string = "Hello from unittest"
        self.player.logwrite(string)
        string = "A second hello"
        self.player.logwrite(string)
        file = open(pathlib.Path(__file__).parents[2] / "logs" / self.player.filename, "r")
        self.assertEqual(string, file.readlines()[-1].strip())


class TestPlayRound(unittest.TestCase):
    def setUp(self) -> None:
        self.player = MiniMaxPlayer()
        self.player.filename = "unittests.txt"

    def test_play_round(self):
        state = [[0, 8, 2, 0], [32, 64, 128, 4], [256, 512, 1024, 8], [32, 64, 128, 256]]
        self.assertEqual(self.player.play_round(state), "left")

    def test_no_deepening(self):
        output = sys.stdout = StringIO()
        state = [[0, 8, 2, 0], [32, 8, 128, 4], [256, 16, 1024, 8], [32, 64, 128, 256]]
        self.player.play_round(state, iterative_deepening=False, id_timelimit=2), "left"
        sys.stdout = sys.__stdout__
        outstring = output.getvalue().split(" | ")
        self.assertEqual(outstring[-1].strip(), "Reached depth: 3")

    def test_deepening(self):
        output = sys.stdout = StringIO()
        state = [[0, 8, 2, 0], [32, 8, 128, 4], [16, 16, 32, 32], [32, 64, 128, 256]]
        self.player.play_round(state, id_timelimit=2), "left"
        sys.stdout = sys.__stdout__
        depth = int(output.getvalue().split(" | Reached depth: ")[-1])
        self.assertGreater(depth, 3)


class TestMaximize(unittest.TestCase):
    def setUp(self) -> None:
        self.player = MiniMaxPlayer()
        self.player.filename = "unittests.txt"
        self.INFINITY = float("inf")

    def test_game_over(self):
        state = [[8, 16, 8, 16], [16, 8, 16, 8], [8, 16, 8, 16], [16, 8, 16, 8]]
        maximized = self.player.maximize(state, 0, 2, -self.INFINITY, self.INFINITY, ["root"])
        self.assertEqual(maximized["value"], -999999)

    def test_game_over_in_one(self):
        state = [[4, 2, 4, 32], [2, 8, 16, 64], [8, 16, 32, 16], [4, 8, 4, 0]]
        maximized = self.player.maximize(state, 0, 2, -self.INFINITY, self.INFINITY, ["root"])
        self.assertEqual(maximized["value"], -999999)

    def test_move_to_merge(self):
        # can move right or left but left leads to merge possibilities
        state = [[0, 8, 2, 0], [32, 64, 128, 4], [256, 512, 1024, 8], [32, 64, 128, 256]]
        maximized = self.player.maximize(state, 0, 2, -self.INFINITY, self.INFINITY, ["root"])
        self.assertEqual(maximized["path"][1], "left")


class TestMinimize(unittest.TestCase):
    def setUp(self) -> None:
        self.player = MiniMaxPlayer()
        self.player.filename = "unittests.txt"
        self.INFINITY = float("inf")

    def test_game_over(self):
        # spawns a 4 to end the game
        state = [[0, 2, 8, 16], [2, 8, 16, 8], [8, 16, 8, 16], [16, 8, 16, 8]]
        minimized = self.player.minimize(state, [(0, 0)], 0, 2, -self.INFINITY, self.INFINITY, ["root"])
        self.assertEqual(minimized["value"], -999999)
        self.assertEqual(minimized["path"][1], "(0, 0) -> 4")

    def test_game_over_in_two(self):
        # Can end game in two: has to deny merge in top first, then fill bottom
        state = [[0, 2, 4, 32], [2, 8, 16, 64], [8, 16, 32, 16], [4, 8, 4, 0]]
        minimized = self.player.minimize(state, [(0, 0)], 0, 4, -self.INFINITY, self.INFINITY, ["root"])
        self.assertEqual(minimized["value"], -999999)
        self.assertEqual(minimized["path"][1], "(0, 0) -> 4")
        self.assertEqual(minimized["path"][-1], "(0, 3) -> 2")


if __name__ == "__main__":
    unittest.main()
