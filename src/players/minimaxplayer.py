import math
import copy
from multiprocessing.spawn import old_main_modules
from typing import List, Tuple
from boardfunctions.boardfunctions import *
from boardfunctions.boardfunctions import Boardfunctions
import time

HUGE_NUMBER = 10e10
SEARCH_DEPTH = 5


class MiniMaxPlayer:
    def __init__(self) -> None:
        self.round_count = 0
        self.known_paths = {}

    def get_empty_slots(self, state: List[List[int]]) -> List[tuple]:
        """Returns a list of empty slots. Used when generating possible moves on game's turn.
        Currently not using this function but get_empty_uniques instead.

        Args:
            state (List[List[int]]): Game's state

        Returns:
            List[tuple]: List of X,Y coordinates representing empty slots on the game grid.
        """
        empty_slots = []
        for x in range(len(state)):
            for y in range(len(state[0])):
                if state[x][y] == 0:
                    empty_slots.append((x, y))
        return empty_slots

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
        play_directions = ["up", "down", "left", "right"]
        path = ["root"]
        v = -HUGE_NUMBER
        winning_direction = None
        for direction in play_directions:
            child = self.generate_direction(state, direction)
            if child == state:
                continue

            candidate_v = self.minimize(child, 1, -HUGE_NUMBER, HUGE_NUMBER, [*path, direction])
            if candidate_v["value"] > v:
                v = candidate_v["value"]
                winning_direction = candidate_v["path"][1]

        self.round_count += 1
        print(f"{self.round_count}; {len(self.get_empty_slots(state))}; {time.time() - starttime} ")

        return winning_direction

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

        v = -HUGE_NUMBER
        play_directions = ["up", "down", "left", "right"]
        for direction in play_directions:
            child = self.generate_direction(state, direction)

            if child == state:
                continue

            minimized_candidate = self.minimize(child, depth + 1, alpha, beta, [*path, direction])["value"]
            v = max(v, minimized_candidate)
            alpha = max(alpha, v)
            if alpha >= beta:
                {"value": v, "path": path}
        return {"value": v, "path": path}

    def minimize(self, state: List[List[int]], depth: int, alpha, beta, path):
        """Minimizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to minimize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """
        # print(f"{path}")

        if Boardfunctions.game_is_over(state) or depth > SEARCH_DEPTH:
            return {"value": self.heuristic(state), "path": path}

        v = HUGE_NUMBER
        empty_slots = self.get_empty_slots(state)

        for slot in empty_slots:
            for i in range(2):
                child = self.generate_spawn_child(state, slot, (i + 1) * 2)
                maximized_candidate = self.maximize(child, depth + 1, alpha, beta, [*path, f"{slot} -> {(i + 1) * 2}"])[
                    "value"
                ]
                v = min(v, maximized_candidate)
                beta = min(beta, v)
                if alpha >= beta:
                    return {"value": v, "path": path}

        if len(empty_slots) == 0:
            v = min(v, self.maximize(state, depth + 1, alpha, beta))["value"]
            beta = min(beta, v)
            if alpha >= beta:
                return {"value": v, "path": path}
        return {"value": v, "path": path}
