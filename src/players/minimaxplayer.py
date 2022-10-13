import math
import copy
from multiprocessing.spawn import old_main_modules
from typing import List, Tuple
from boardfunctions.boardfunctions import *
from boardfunctions.boardfunctions import Boardfunctions
import time

HUGE_NUMBER = 999999999
SEARCH_DEPTH = 6
# SEARCH_DEPTH = 5


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

    def rotate_grid(self, state: List[List[int]], direction: str) -> List[List[int]]:
        """Rotates the game state grid to normalize it for generating directions

        Args:
            state (List[List[int]]): Game state to rotate
            direction (str): Direction that will be generated out of the rotated state

        Returns:
            List[List[int]]: Rotated game state grid
        """
        if direction == "left":
            return state

        elif direction == "right":
            return [list(reversed(row)) for row in state]

        elif direction == "up":
            rotated_state = []

            for i, row in enumerate(state):
                newrow = []
                for j in range(len(row)):
                    newrow.append(state[j][i])
                rotated_state.append(newrow)

            return rotated_state

        elif direction == "down":
            rotated_state = []

            for i, row in enumerate(state):
                newrow = []
                for j in range(len(row)):
                    newrow.insert(0, state[j][i])
                rotated_state.insert(0, newrow)

            return rotated_state

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
        lastchild = None
        lastchildname = None
        v = -HUGE_NUMBER
        winning_direction = None
        for direction in play_directions:
            child = self.generate_direction(state, direction)

            if self.invalid_state(state, child, direction, lastchild, lastchildname):
                continue

            lastchild = child
            lastchildname = direction

            candidate_v = self.minimize(child, 1, -HUGE_NUMBER, HUGE_NUMBER)
            if candidate_v > v:
                v = candidate_v
                winning_direction = direction

        self.round_count += 1
        print(f"{self.round_count}; {len(self.get_empty_slots(state))}; {time.time() - starttime} ")

        return winning_direction.capitalize()

    def invalid_state(
        self,
        state: List[List[int]],
        child: List[List[int]],
        direction: str,
        lastchild: List[List[int]],
        lastchildname: str,
    ) -> bool:
        """Checks if the given state is relevant for minimizing. States that are identical to current state or previously minimized states are irrelevant.

        Args:
            state (List[List[int]]): Current state of the game
            child (List[List[int]]): Generated child state, possibly to be minimized next
            direction (str): Which direction from the current state does the child represent
            lastchild (List[List[int]]): Previously minimized child
            lastchildname (str): previously minimized child's direction

        Returns:
            bool: _description_
        """
        if child == state:
            return True

        if direction == "down" and lastchild == child[::-1]:
            return True

        if direction == "right" and lastchildname == "left" and lastchild == self.rotate_grid(child, "right"):
            return True

        return False

    def maximize(self, state: List[List[int]], depth: int, alpha, beta):
        """Maximizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to maximize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """
        if Boardfunctions.game_is_over(state) or depth > SEARCH_DEPTH:
            return self.heuristic(state)

        v = -HUGE_NUMBER
        play_directions = ["up", "down", "left", "right"]
        lastchild = None
        lastchildname = None
        for direction in play_directions:
            child = self.generate_direction(state, direction)
            if self.invalid_state(state, child, direction, lastchild, lastchildname):
                continue

            lastchild = child
            lastchildname = direction
            minimized_candidate = self.minimize(child, depth + 1, alpha, beta)
            v = max(v, minimized_candidate)
            alpha = max(alpha, v)
            if alpha >= beta:
                return v
        return v

    def minimize(self, state: List[List[int]], depth: int, alpha, beta):
        """Minimizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to minimize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """
        if Boardfunctions.game_is_over(state) or depth > SEARCH_DEPTH:
            return self.heuristic(state)

        v = HUGE_NUMBER
        empty_slots = self.get_empty_slots(state)

        for slot in empty_slots:
            for i in range(2):
                child = self.generate_spawn_child(state, slot, (i + 1) * 2)
                maximized_candidate = self.maximize(child, depth + 1, alpha, beta)
                v = min(v, maximized_candidate)
                beta = min(beta, v)
                if alpha >= beta:
                    return v

        if len(empty_slots) == 0:
            v = min(v, self.maximize(state, depth + 1, alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                return v
        return v
