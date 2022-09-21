import copy
from typing import List

from gamehandler.gamehandler import GameHandler

HUGE_NUMBER = 999999999
SEARCH_DEPTH = 4

gamehandler = GameHandler()


class MiniMaxPlayer:
    def play_round(self, grid: List[List[int]]) -> str:
        self.maximize(grid)

    def generate_children(self, state, is_player_turn):
        if not is_player_turn:
            return self.generate_spawn_tile(state)

        return [
            [*self.generate_direction(state, "up")],
            [*self.generate_direction(state, "down")],
            [*self.generate_direction(state, "left")],
            [*self.generate_direction(state, "right")],
        ]

    def generate_spawn_tile(self, state):
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

    def generate_direction(self, state, direction):
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

    def rotate_grid(self, state, direction):
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

    def heuristic(self, state):
        tile_sum = 0
        tiles = 0
        for row in state:
            for col in row:
                if col != 0:
                    tile_sum += col
                    tiles += 1

        return tile_sum / tiles

    def maximize(self, state, depth):
        if gamehandler.game_is_over(state):
            return gamehandler.get_grid_max_value(state)
        v = -HUGE_NUMBER
        for child in self.generate_children(state, True):
            v = max(v, self.minimize(child, depth))
        return v

    def minimize(self, state, depth):
        if gamehandler.game_is_over(state):
            return gamehandler.get_grid_max_value(state)
        if depth > SEARCH_DEPTH:
            return self.heuristic(state)
        v = HUGE_NUMBER
        for child in self.generate_children(state, False):
            v = max(v, self.maximize(child, depth + 1))
        return v
