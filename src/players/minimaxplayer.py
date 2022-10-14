from typing import List, Tuple
from boardfunctions.boardfunctions import *
from boardfunctions.boardfunctions import Boardfunctions
import time

from players.minimaxplayer2 import maximize

INFINITY = float("inf")
SEARCH_DEPTH = 7


class MiniMaxPlayer:
    def __init__(self) -> None:
        self.round_count = 0
        self.known_paths = {}

    def get_empties(self, state: List[List[int]]) -> List[tuple]:
        """Returns a list of empty slots. Used when generating possible moves on game's turn.
        Currently not using this function but get_empty_uniques instead.

        Args:
            state (List[List[int]]): Game's state

        Returns:
            List[tuple]: List of X,Y coordinates representing empty slots on the game grid.
        """
        empties = []
        for x in range(len(state)):
            for y in range(len(state[0])):
                if state[x][y] == 0:
                    empties.append((x, y))
        return empties

    def generate_spawn_child(self, state: List[List[int]], slot: Tuple, value: int) -> List[List[int]]:
        """Generates a child state for given state, representing a possible state created on game's turn

        Args:
            state (List[List[int]]): Game's state
            slot (Tuple): X and Y coordinates of the slot to add tile to
            value (int): value of the new tile

        Returns:
            _type_: List[List[int]]
        """
        new_child = Boardfunctions.copy_grid(state)
        new_child[slot[0]][slot[1]] = value
        return new_child

    def generate_direction(self, state: List[List[int]], direction: str) -> List[List[int]]:
        """Generates the state of the grid after players move to given direction

        Args:
            state (List[List[int]]): Game state to move
            direction (str): Direction to move to ("left", "right", "up", "down")

        Returns:
            List[List[int]]: Game state after moving the tiles to given direction
        """
        functions = {
            "up": Boardfunctions.move_up,
            "down": Boardfunctions.move_down,
            "left": Boardfunctions.move_left,
            "right": Boardfunctions.move_right,
        }

        return functions[direction]((state, None))[0]

    def heuristic(self, state: List[List[int]]) -> float:
        """Heuristic function to evaluate the value of a state that is not an end state

        Args:
            state (List[List[int]]): _description_

        Returns:
            float: _description_
        """
        tile_sum = 0
        tiles = 0
        for row in state:
            for col in row:
                if col != 0:
                    tile_sum += col
                    tiles += 1

        return tile_sum / tiles

    def play_round(self, state: List[List[int]]):
        """Calculates the next move for given games state

        Args:
            grid (List[List[int]]): State of the game grid

        Returns:
            str: Direction to play ("left", "right", "up", "down")
        """
        starttime = time.time()
        self.round_count += 1
        maximized = self.maximize(state, 0, -INFINITY, INFINITY, ["root"])
        print(f"{self.round_count}; {len(self.get_empties(state))}; {time.time() - starttime} ")
        return maximized["path"][1]

    def maximize(self, state: List[List[int]], depth: int, alpha, beta, path):
        """Maximizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to maximize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """

        if Boardfunctions.game_is_over(state) or depth > SEARCH_DEPTH:
            return {"value": self.heuristic(state), "path": path}

        maximized = {"value": -INFINITY, "path": path}

        play_directions = ["up", "down", "left", "right"]
        for direction in play_directions:
            child = self.generate_direction(state, direction)

            if child == state:
                continue

            candidate = self.minimize(child, depth + 1, alpha, beta, [*path, direction])

            if candidate["value"] > maximized["value"]:
                maximized = candidate

            alpha = max(alpha, maximized["value"])
            if alpha >= beta:
                return maximized

        return maximized

    def minimize(self, state: List[List[int]], depth: int, alpha, beta, path):
        """Minimizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to minimize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """
        if Boardfunctions.game_is_over(state) or depth > SEARCH_DEPTH:
            return {"value": self.heuristic(state), "path": path}

        minimized = {"value": INFINITY, "path": path}
        empties = self.get_empties(state)

        # As long as there are empty slots
        for slot in empties:
            for i in range(2):
                child = self.generate_spawn_child(state, slot, (i + 1) * 2)
                candidate = self.maximize(child, depth + 1, alpha, beta, [*path, f"{slot} -> {(i + 1) * 2}"])

                if candidate["value"] < minimized["value"]:
                    minimized = candidate

                beta = min(beta, minimized["value"])
                if alpha >= beta:
                    return minimized

        # If the board is full but still playable
        if len(empties) == 0:
            candidate = self.maximize(state, depth + 1, alpha, beta, path)

            if candidate["value"] < minimized["value"]:
                minimized = candidate

            beta = min(beta, minimized["value"])
            if alpha >= beta:
                return minimized

        return minimized
