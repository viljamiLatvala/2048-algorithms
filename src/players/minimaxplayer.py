import copy
from typing import List
from gamehandler.gamehandler import GameHandler

HUGE_NUMBER = 999999999
# SEARCH_DEPTH = 6
SEARCH_DEPTH = 6

gamehandler = GameHandler()


class MiniMaxPlayer:
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

        player_moves = [
            {"direction": "up", "state": [*self.generate_direction(state, "up")]},
            {"direction": "down", "state": [*self.generate_direction(state, "down")]},
            {"direction": "left", "state": [*self.generate_direction(state, "left")]},
            {"direction": "right", "state": [*self.generate_direction(state, "right")]},
        ]

        allowed_moves = []
        for move in player_moves:
            if move["state"] != state:
                allowed_moves.append(move["state"])

        return allowed_moves

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

    def play_round(self, state: List[List[int]]):
        """Calculates the next move for given games state

        Args:
            grid (List[List[int]]): State of the game grid

        Returns:
            str: Direction to play ("left", "right", "up", "down")
        """
        play_directions = ["up", "down", "left", "right"]
        lastchild = None
        v = -HUGE_NUMBER
        winning_direction = "Up"
        for direction in play_directions:
            child = self.generate_direction(state, direction)

            if direction == "down":
                if lastchild == child[::-1]:
                    continue

            if direction == "right":
                if lastchild == self.rotate_grid(child, "right"):
                    continue

            lastchild = child

            if child == state:
                continue
            candidate_v = self.minimize(child, 1, -HUGE_NUMBER, HUGE_NUMBER)
            if candidate_v > v:
                v = candidate_v
                winning_direction = direction

        return winning_direction.capitalize()

    def maximize(self, state: List[List[int]], depth: int, alpha, beta):
        """Maximizer function for the minmax -algorithm

        Args:
            state (List[List[int]]): Game state to maximize
            depth (int): Current depth of search

        Returns:
            _type_: _description_
        """
        if gamehandler.game_is_over(state):
            return self.heuristic(state)
        if depth > SEARCH_DEPTH:
            return self.heuristic(state)
        v = -HUGE_NUMBER
        play_directions = ["up", "down", "left", "right"]
        lastchild = None
        for direction in play_directions:
            child = self.generate_direction(state, direction)

            if direction == "down":
                if lastchild == child[::-1]:
                    continue

            if direction == "right":
                if lastchild == self.rotate_grid(child, "right"):
                    continue

            lastchild = child

            if child == state:
                continue

            v = max(v, self.minimize(child, depth + 1, alpha, beta))
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
        if gamehandler.game_is_over(state):
            return self.heuristic(state)
        if depth > SEARCH_DEPTH:
            return self.heuristic(state)
        v = HUGE_NUMBER
        children = self.generate_children(state, False)
        for child in children:
            v = min(v, self.maximize(child, depth + 1, alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                return v
        if len(children) == 0:
            v = min(v, self.maximize(state, depth + 1, alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                return v
        return v
