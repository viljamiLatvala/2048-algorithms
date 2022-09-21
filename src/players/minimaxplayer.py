import copy


class MiniMaxPlayer:
    def play_round(self):
        pass

    def generate_children(self, state, is_player_turn):
        children = []
        if not is_player_turn:
            return children + self.generate_spawn_tile(state)

    def generate_spawn_tile(self, state):
        children = []
        print(state)
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

    def generate_left(self, state):
        new_state = []

        for row in state:
            # Create list of all present tiles
            tiles = []
            for col in row:
                if col != 0:
                    tiles.append(col)

            print(f"Tiles: {tiles}")
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

            print(f"Merged tiles: {merged_tiles}")

            new_state.append(merged_tiles)

        return new_state

    def minimize(self):
        pass

    def maximize(self):
        pass
