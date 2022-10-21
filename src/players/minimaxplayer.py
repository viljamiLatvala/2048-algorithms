from typing import List, Tuple
from boardfunctions.boardfunctions import Boardfunctions as board
from boardfunctions.boardtree import *
import time

INFINITY = float("inf")


class MiniMaxPlayer:
    def __init__(self) -> None:
        self.round_count = 0
        self.known_paths = {}
        self.last_best = "up"

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
        if board.game_is_over(state):
            return -INFINITY

        tile_sum = 0
        tile_diff = 0
        tiles = 0

        for row in state:
            last_tile = None
            for col in row:
                if col != 0:
                    tiles += 1
                    tile_diff += 0 if last_tile is None else abs(col - last_tile)
                    last_tile = col

        for y in range(4):
            last_tile = None
            for x in range(4):
                if state[x][y] != 0:
                    tile_diff += 0 if last_tile is None else abs(state[x][y] - last_tile)
                    last_tile = state[x][y]

        return -tile_diff * tiles

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
        while elapsed < 0.2:
            maximized = self.maximize(state, 0, maxdepth, -INFINITY, INFINITY, ["root"])
            maxdepth += 1
            print(maximized["path"])
            self.last_best = maximized["path"][1]
            elapsed += time.time() - starttime

        # Write html
        # states = list(self.known_paths.values())
        # write_html(form_graph(states), f"turn_{self.round_count}")

        self.round_count += 1
        decision = maximized["path"][1]
        print(
            f"Round: {self.round_count} | Move: {decision.ljust(5,' ')} | Time spent: {'%.2f' % elapsed}s | Reached depth: {maxdepth}"
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
            if board.game_is_over(state):
                print("GAME IS OVER")
            return {"value": self.heuristic(state), "path": path}

        maximized = {"value": -INFINITY, "path": path}
        directions = {"up": board.move_up, "down": board.move_down, "left": board.move_left, "right": board.move_right}
        last_best_function = directions.pop(self.last_best)
        for direction, move in [(self.last_best, last_best_function), *directions.items()]:
            child, empties = move((state, None))

            if child == state:
                continue

            candidate = self.minimize(child, empties, depth, maxdepth, alpha, beta, [*path, direction])

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
            print("BOARD FULL")
            candidate = self.maximize(state, depth + 1, maxdepth, alpha, beta, path)

            if candidate["value"] < minimized["value"]:
                minimized = candidate

            beta = min(beta, minimized["value"])
            if alpha >= beta:
                return minimized

        return minimized
