import copy
from typing import List
from gamehandler.gamehandler import GameHandler

HUGE_NUMBER = 999999999
SEARCH_DEPTH = 4

gamehandler = GameHandler()


class MiniMaxPlayer:
    def play_round(self, grid: List[List[int]]) -> str:
        """Calculates the next move for given games state

        Args:
            grid (List[List[int]]): State of the game grid

        Returns:
            str: Direction to play ("left", "right", "up", "down")
        """

    def generate_children(self, state: List[List[int]], is_player_turn: bool) -> List[List[List[int]]]:
        """Generates list of possible next states of the game given a state

        Args:
            state (List[List[int]]): Game state to generate child states to
            is_player_turn (bool): Indicates if it is the player or the games turn to play

        Returns:
            List[List[List[int]]]: List of possible child states
        """

        if not is_player_turn:
            return self.generate_spawn_tile(state)

        return [
            [*self.generate_direction(state, "up")],
            [*self.generate_direction(state, "down")],
            [*self.generate_direction(state, "left")],
            [*self.generate_direction(state, "right")],
        ]

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
                    new_child = copy.deepcopy(state)
                    new_child[x][y] = 2
                    children.append(new_child)

                    new_child = copy.deepcopy(state)
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
                for j, col in enumerate(row):
                    newrow.append(state[j][i])
                rotated_state.append(newrow)

            return rotated_state

        elif direction == "down":
            rotated_state = []

            for i, row in enumerate(state):
                newrow = []
                for j, col in enumerate(row):
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

    def maximize(self, state: List[List[int]], depth: int):
        """Maximizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to maximize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """
        if gamehandler.game_is_over(state):
            return gamehandler.get_grid_max_value(state)
        if depth > SEARCH_DEPTH:
            return self.heuristic(state)
        v = -HUGE_NUMBER
        for child in self.generate_children(state, True):
            v = max(v, self.minimize(child, depth))
        return v

    def minimize(self, state: List[List[int]], depth: int):
        """Minimizer functionf or the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to minimize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """
        if gamehandler.game_is_over(state):
            return gamehandler.get_grid_max_value(state)
        if depth > SEARCH_DEPTH:
            return self.heuristic(state)
        v = HUGE_NUMBER
        for child in self.generate_children(state, False):
            v = max(v, self.maximize(child, depth + 1))
        return v
