import math
import copy
from multiprocessing.spawn import old_main_modules
from typing import List, Tuple
from unittest.mock import mock_open
from gamehandler.gamehandler import GameHandler
import time

HUGE_NUMBER = 999999999
# SEARCH_DEPTH = 6
SEARCH_DEPTH = 5

gamehandler = GameHandler()


class MiniMaxPlayer:
    def __init__(self) -> None:
        self.round_count = 0
        self.generated_states = 0
        self.rotation_times = {"up": 0, "down": 0, "left": 0, "right": 0}
        self.time_generate_direction = 0
        self.time_get_empty_uniques = 0
        self.time_game_over_check = 0
        self.time_maximize = 0
        self.time_minimize = 0

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

    def get_empty_uniques(self, grid: List[List[int]]) -> List[tuple]:
        """Returns a list of empty slots in the game grid.
        Used when generating possible moves on game's turn.
        Disqualifies a slot if effectively identical slot has already been found,
        meaning that the difference in position would not lead to new possible game states.

        Args:
            grid (List[List[int]]): Game's state

        Returns:
            List[tuple]: List of X,Y coordinates representing empty slots on the game grid.
        """
        topmost = len(grid) - 1
        bottommost = 0
        leftmost = len(grid[0]) - 1
        rightmost = 0

        for x in range(len(grid)):
            for y in range(len(grid[0])):
                if grid[x][y] != 0:
                    if x < topmost:
                        topmost = x
                    if x > bottommost:
                        bottommost = x
                    if y < leftmost:
                        leftmost = y
                    if y > rightmost:
                        rightmost = y

        topleft_empty = (topmost - 1, leftmost - 1)
        bottomleft_empty = (bottommost + 1, leftmost - 1)
        topright_empty = (topmost - 1, rightmost + 1)
        bottomright_empty = (bottommost + 1, rightmost + 1)

        empty_slots = [topleft_empty, bottomleft_empty, topright_empty, bottomright_empty]

        for x in range(topmost, bottommost + 1):
            for y in range(0, leftmost):
                empty_slots.append((x, y))

        for x in range(len(grid)):
            for y in range(leftmost, rightmost + 1):
                if grid[x][y] == 0:
                    empty_slots.append((x, y))

        constrained_empty_slots = []

        for slot in empty_slots:
            if slot[0] < len(grid) and slot[1] < len(grid[0]):
                constrained_empty_slots.append(slot)

        return constrained_empty_slots

    def copy_grid(self, item):
        grid = [[], [], [], []]
        for i in range(4):
            grid[i].extend(item[i])
        return grid

    def generate_spawn_child(self, state: List[List[int]], slot: Tuple, value: int) -> List[List[int]]:
        """Generates a child state for given state, representing a possible state created on game's turn

        Args:
            state (List[List[int]]): Game's state
            slot (Tuple): X and Y coordinates of the slot to add tile to
            value (int): value of the new tile

        Returns:
            _type_: List[List[int]]
        """
        new_child = self.copy_grid(state)
        new_child[slot[0]][slot[1]] = value
        return new_child

    def generate_spawn_tile(self, state: List[List[int]]) -> List[List[List[int]]]:
        """Generates list of child states on computers turn

        Args:
            state (List[List[int]]): Game state to generate children to

        Returns:
            List[List[List[int]]]: List of possible child states
        """
        children = []
        for x, row in enumerate(state):
            for y, col in enumerate(row):
                if col == 0:
                    new_child = self.copy_grid(state)
                    new_child[x][y] = 2
                    children.append(new_child)

                    new_child = self.copy_grid(state)
                    new_child[x][y] = 4
                    children.append(new_child)
        return children

    def generate_direction(self, state: List[List[int]], direction: str) -> List[List[int]]:
        """Generates the state of the grid after players move to given direction

        Args:
            state (List[List[int]]): Game state to move
            direction (str): Direction to move to ("left", "right", "up", "down")

        Returns:
            List[List[int]]: Game state after moving the tiles to given direction
        """
        new_state = []
        rotated_grid = self.rotate_grid(state, direction)
        for row in rotated_grid:

            # Create list of all present tiles
            tiles = [col for col in row if col != 0]

            # Merge same values that are back to back
            merged_tiles = [] if len(tiles) == 0 else [tiles[0]]

            # Flag to prevent merging tiles that have been already merged once
            allow_merge = True
            for tile in tiles[1:]:
                if tile == merged_tiles[len(merged_tiles) - 1] and allow_merge:
                    merged_tiles[len(merged_tiles) - 1] *= 2
                    allow_merge = False
                else:
                    merged_tiles.append(tile)
                    allow_merge = True

            # Fill up rest of the row with zeroes
            merged_tiles.extend((4 - len(merged_tiles)) * [0])

            new_state.append(merged_tiles)

        return self.rotate_grid(new_state, direction)

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

    def greedy_heuristic(self, state):
        return gamehandler.get_grid_max_value(state)

    def empty_heuristic(self, state):
        zeroes = 0
        for row in state:
            for col in row:
                if col == 0:
                    zeroes += 1
        return zeroes

    def uniform_heuristic(self, state):
        different_tile_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for row in state:
            for col in row:
                if col == 0:
                    continue
                if col == 2:
                    different_tile_values[0] += 1
                else:
                    if len(different_tile_values) < math.log(col, 2):
                        for _ in range(math.log(col, 2) - len(different_tile_values)):
                            different_tile_values.append(0)

                    different_tile_values[int(math.log(col, 2)) - 1] += 1
        return sum([x**3 for x in different_tile_values])

    def monotonicity_heuristic(self, state):
        best = -1
        ted_state = copy.deepcopy(state)
        for _ in range(4):  # Board is evaluated from all 4 directions
            current = 0
            for row_no in range(4):
                for col_no in range(3):
                    if ted_state[row_no][col_no] == 0:
                        continue
                    if ted_state[row_no][col_no] >= ted_state[row_no][col_no + 1]:
                        current += 1
            for col_no in range(4):
                for row_no in range(3):
                    if ted_state[row_no][col_no] == 0:
                        continue
                    if ted_state[row_no][col_no] >= ted_state[row_no + 1][col_no]:
                        current += 1

            best = best if best >= current else current

            ted_state = list(zip(*ted_state[::-1]))
        return best

    def old_heuristic(self, state):
        tile_sum = 0
        tiles = 0
        for row in state:
            for col in row:
                if col != 0:
                    tile_sum += col
                    tiles += 1

        return tile_sum / tiles

    def heuristic(self, state: List[List[int]]) -> float:
        """Heuristic function to evaluate the value of a state that is not an end state

        Args:
            state (List[List[int]]): _description_

        Returns:
            float: _description_
        """
        """
        endstate_minus = 500 if gamehandler.game_is_over(state) else 0
        return (
            (self.monotonicity_heuristic(state)) / 2
            + (math.log(self.greedy_heuristic(state), 2) * 2)
            + self.empty_heuristic(state)
            - endstate_minus
        )
        """
        return self.old_heuristic(state)

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
            self.generated_states += 1

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
        if gamehandler.game_is_over(state) or depth > SEARCH_DEPTH:
            return self.heuristic(state)

        v = -HUGE_NUMBER
        play_directions = ["up", "down", "left", "right"]
        lastchild = None
        lastchildname = None
        for direction in play_directions:
            child = self.generate_direction(state, direction)
            self.generated_states += 1
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
        if gamehandler.game_is_over(state) or depth > SEARCH_DEPTH:
            return self.heuristic(state)

        v = HUGE_NUMBER
        empty_slots = self.get_empty_uniques(state)

        for slot in empty_slots:
            for i in range(2):
                child = self.generate_spawn_child(state, slot, (i + 1) * 2)
                maximized_candidate = self.maximize(child, depth + 1, alpha, beta)
                v = min(v, maximized_candidate)
                beta = min(beta, v)
                if alpha >= beta:
                    return v

                self.generated_states += 1

        if len(empty_slots) == 0:
            v = min(v, self.maximize(state, depth + 1, alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                return v
        return v
