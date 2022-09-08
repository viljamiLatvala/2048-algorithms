class GameHandler:

    def get_grid_max_value(self, grid):
        max = 0
        for x in grid:
            for y in x:
                if y > max:
                    max = y
        
        return max

    def get_possible_mvmnt_directions():
        possibilities = []

    def is_possible_mvmnt_direction(direction):
        pass