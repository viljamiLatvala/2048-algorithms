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

    def can_move_left(self, grid):
        can_move = True
        for x in grid:
            zero_encountered = False
            for y in x:
                if y == 0:
                    zero_encountered = True
                if y != 0 and zero_encountered:
                    can_move = False
        return can_move
            