from typing import List, Tuple
from boardfunctions.boardfunctions import Boardfunctions as board
from boardfunctions.boardtree import *
import time

INFINITY = float("inf")
SEARCH_DEPTH = 4


class MiniMaxPlayer:
    def __init__(self) -> None:
        self.round_count = 0
        self.known_paths = {}

    def generate_spawn_child(self, state: List[List[int]], slot: Tuple, value: int) -> List[List[int]]:
        """Generates a child state for given state, representing a possible state created on game's turn

        Args:
            state (List[List[int]]): Game's state
            slot (Tuple): X and Y coordinates of the slot to add tile to
            value (int): value of the new tile

        Returns:
            _type_: List[List[int]]
        """
        new_child = board.copy_grid(state)
        new_child[slot[0]][slot[1]] = value
        return new_child

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
        elapsed = 0
        maxdepth = 2
        while elapsed < 1:
            maximized = self.maximize(state, 0, maxdepth, -INFINITY, INFINITY, ["root"])
            maxdepth += 1
            elapsed += time.time() - starttime

        # Write html
        # states = list(self.known_paths.values())
        # write_html(form_graph(states), f"turn_{self.round_count}")

        self.round_count += 1
        elapsed = "%.2f" % elapsed
        decision = maximized["path"][1]
        print(
            f"Round: {self.round_count} | Move: {decision.ljust(5,' ')} | Time spent: {elapsed}s | Reached depth: {maxdepth}"
        )
        return decision

    def maximize(self, state: List[List[int]], depth: int, maxdepth, alpha, beta, path):
        """Maximizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to maximize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """

        self.known_paths[f"{path}"] = {"board": state, "path": path}

        if board.game_is_over(state) or depth > maxdepth:
            return {"value": self.heuristic(state), "path": path}

        maximized = {"value": -INFINITY, "path": path}
        directions = {"up": board.move_up, "down": board.move_down, "left": board.move_left, "right": board.move_right}

        for direction, move in directions.items():
            child, empties = move((state, None))

            if child == state:
                continue

            candidate = self.minimize(child, empties, depth + 1, maxdepth, alpha, beta, [*path, direction])

            if candidate["value"] > maximized["value"]:
                maximized = candidate

            alpha = max(alpha, maximized["value"])
            if alpha >= beta:
                return maximized

        return maximized

    def minimize(self, state: List[List[int]], empties, depth: int, maxdepth, alpha, beta, path):
        """Minimizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to minimize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """

        self.known_paths[f"{path}"] = {"board": state, "path": path}

        if board.game_is_over(state) or depth > maxdepth:
            return {"value": self.heuristic(state), "path": path}

        minimized = {"value": INFINITY, "path": path}

        # As long as there are empty slots
        for slot in empties:
            for i in range(2):
                child = self.generate_spawn_child(state, slot, (i + 1) * 2)
                candidate = self.maximize(child, depth + 1, maxdepth, alpha, beta, [*path, f"{slot} -> {(i + 1) * 2}"])

                if candidate["value"] < minimized["value"]:
                    minimized = candidate

                beta = min(beta, minimized["value"])
                if alpha >= beta:
                    return minimized

        # If the board is full but still playable
        if len(empties) == 0:
            candidate = self.maximize(state, depth + 1, maxdepth, alpha, beta, path)

            if candidate["value"] < minimized["value"]:
                minimized = candidate

            beta = min(beta, minimized["value"])
            if alpha >= beta:
                return minimized

        return minimized
