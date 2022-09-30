import copy
from typing import List
from gamehandler.gamehandler import GameHandler
import time

HUGE_NUMBER = 999999999
# SEARCH_DEPTH = 6
SEARCH_DEPTH = 6

gamehandler = GameHandler()


class MiniMaxPlayer:
    def __init__(self):
        self.turn_count = 0
        self.generated_player_moves = 0
        self.generated_game_moves = 0
        self.visited_states = 0
        self.counted_prunes = 0
        self.recognized_dup_states = 0
        self.elapsed_times = {
            "generate_spawn_tile": 0,
            "generate_direction": 0,
            "maximize": 0,
            "minimize": 0,
        }

    def get_empty_slots(self, state):
        empty_slots = []
        for x in range(len(state)):
            for y in range(len(state[0])):
                if state[x][y] == 0:
                    empty_slots.append((x, y))
        return empty_slots

    def get_empty_uniques(self, grid):
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

        # print(f"topmost: {topmost}\nbottommost: {bottommost}\nleftmost: {leftmost}\nrightmost: {rightmost}")

        topleft_empty = (topmost - 1, leftmost - 1)
        bottomleft_empty = (bottommost + 1, leftmost - 1)
        topright_empty = (topmost - 1, rightmost + 1)
        bottomright_empty = (bottommost + 1, rightmost + 1)

        empty_slots = [topleft_empty, bottomleft_empty, topright_empty, bottomright_empty]

        # print(f"Going over vertical, rows from {topmost} to {bottommost}")
        # print(f"   Columns from 0 to {leftmost - 1}")
        for x in range(topmost, bottommost + 1):
            for y in range(0, leftmost):
                # print(f"{x},{y}")
                empty_slots.append((x, y))

        # print("Going over horizontal")
        for x in range(4):
            for y in range(leftmost, rightmost + 1):
                if grid[x][y] == 0:
                    # print(f"{x},{y}")
                    empty_slots.append((x, y))

        constrained_empty_slots = []

        for slot in empty_slots:
            if slot[0] < len(grid) and slot[1] < len(grid[0]):
                constrained_empty_slots.append(slot)

        return constrained_empty_slots

    def generate_spawn_child(self, state, slot, value):
        new_child = copy.deepcopy(state)
        new_child[slot[0]][slot[1]] = value
        return new_child

    def generate_spawn_tile(self, state: List[List[int]]) -> List[List[List[int]]]:
        """Generates list of child states on computers turn

        Args:
            state (List[List[int]]): Game state to generate children to

        Returns:
            List[List[List[int]]]: List of possible child states
        """
        starttime = time.perf_counter()
        children = []
        for x, row in enumerate(state):
            for y, col in enumerate(row):
                if col == 0:
                    new_child = copy.deepcopy(state)
                    new_child[x][y] = 2
                    children.append(new_child)

                    new_child = copy.deepcopy(state)
                    new_child[x][y] = 4
                    children.append(new_child)
        endtime = time.perf_counter()
        self.elapsed_times["generate_spawn_tile"] += endtime - starttime
        return children

    def generate_direction(self, state: List[List[int]], direction: str) -> List[List[int]]:
        """Generates the state of the grid after players move to given direction

        Args:
            state (List[List[int]]): Game state to move
            direction (str): Direction to move to ("left", "right", "up", "down")

        Returns:
            List[List[int]]: Game state after moving the tiles to given direction
        """
        starttime = time.perf_counter()

        new_state = []
        rotated_grid = self.rotate_grid(state, direction)
        for row in rotated_grid:
            # Create list of all present tiles
            tiles = []
            for col in row:
                if col != 0:
                    tiles.append(col)

            # Merge same values that are back to back
            merged_tiles = []
            if len(tiles) > 0:
                merged_tiles.append(tiles[0])

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
            while len(merged_tiles) < len(state[0]):
                merged_tiles.append(0)

            new_state.append(merged_tiles)

        endtime = time.perf_counter()
        self.elapsed_times["generate_direction"] += endtime - starttime
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
        starttime = time.perf_counter()
        self.turn_count += 1
        self.generated_player_moves = 0
        self.generated_game_moves = 0
        play_directions = ["up", "down", "left", "right"]
        lastchild = None
        lastchildname = None
        v = -HUGE_NUMBER
        winning_direction = None
        for direction in play_directions:
            child = self.generate_direction(state, direction)

            if child == state:
                continue

            if direction == "down" and lastchild == child[::-1]:
                self.recognized_dup_states += 1
                continue

            if direction == "right" and lastchildname == "left" and lastchild == self.rotate_grid(child, "right"):
                self.recognized_dup_states += 1
                continue

            lastchild = child
            lastchildname = direction

            candidate_v = self.minimize(child, 1, -HUGE_NUMBER, HUGE_NUMBER)
            if candidate_v > v:
                v = candidate_v
                winning_direction = direction

        print(f"Move no.{self.turn_count}: {winning_direction} {time.perf_counter() - starttime}")
        print(f"Generated player states: {self.generated_player_moves}, game states: {self.generated_game_moves}")
        return winning_direction.capitalize()

    def maximize(self, state: List[List[int]], depth: int, alpha, beta):
        """Maximizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to maximize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """
        starttime = time.perf_counter()
        self.visited_states += 1
        if gamehandler.game_is_over(state):
            endtime = time.perf_counter()
            self.elapsed_times["maximize"] += endtime - starttime
            return self.heuristic(state)
        if depth > SEARCH_DEPTH:
            endtime = time.perf_counter()
            self.elapsed_times["maximize"] += endtime - starttime
            return self.heuristic(state)
        v = -HUGE_NUMBER
        play_directions = ["up", "down", "left", "right"]
        lastchild = None
        lastchildname = None
        for direction in play_directions:
            child = self.generate_direction(state, direction)
            self.generated_player_moves += 1
            if child == state:
                continue

            if direction == "down" and lastchild == child[::-1]:
                self.recognized_dup_states += 1
                continue

            if direction == "right" and lastchildname == "left" and lastchild == self.rotate_grid(child, "right"):
                self.recognized_dup_states += 1
                continue

            lastchild = child
            lastchildname = direction

            v = max(v, self.minimize(child, depth + 1, alpha, beta))
            alpha = max(alpha, v)
            if alpha >= beta:
                self.counted_prunes += 1
                endtime = time.perf_counter()
                self.elapsed_times["maximize"] += endtime - starttime
                return v
        endtime = time.perf_counter()
        self.elapsed_times["maximize"] += endtime - starttime
        return v

    def minimize(self, state: List[List[int]], depth: int, alpha, beta):
        """Minimizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to minimize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """
        starttime = time.perf_counter()
        self.visited_states += 1
        if gamehandler.game_is_over(state):
            endtime = time.perf_counter()
            self.elapsed_times["minimize"] += endtime - starttime
            return self.heuristic(state)
        if depth > SEARCH_DEPTH:
            endtime = time.perf_counter()
            self.elapsed_times["minimize"] += endtime - starttime
            return self.heuristic(state)
        v = HUGE_NUMBER

        empty_slots = self.get_empty_uniques(state)

        for slot in empty_slots:
            child = self.generate_spawn_child(state, slot, 2)
            v = min(v, self.maximize(child, depth + 1, alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                endtime = time.perf_counter()
                self.elapsed_times["minimize"] += endtime - starttime
                return v

            child = self.generate_spawn_child(state, slot, 4)
            v = min(v, self.maximize(child, depth + 1, alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                endtime = time.perf_counter()
                self.elapsed_times["minimize"] += endtime - starttime
                return v

            self.generated_game_moves += 2

        if len(empty_slots) == 0:
            v = min(v, self.maximize(state, depth + 1, alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                self.counted_prunes += 1
                endtime = time.perf_counter()
                self.elapsed_times["minimize"] += endtime - starttime
                return v
        endtime = time.perf_counter()
        self.elapsed_times["minimize"] += endtime - starttime
        return v
