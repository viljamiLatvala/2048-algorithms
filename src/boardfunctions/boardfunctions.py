from typing import List


class Boardfunctions:
    """Object that provides various information about the game grid"""

    def get_grid_max_value(grid: List[List[int]]) -> int:
        """Returns the highest value present in the grid

        Args:
            grid (List[List[int]]): the games current state
        Returns:
            int: Highest value found in grid
        """
        maxvalue = 0
        for row in grid:
            for col in row:
                if col > maxvalue:
                    maxvalue = col

        return maxvalue

    def game_is_over(grid: List[List[int]]) -> bool:
        """Checks the game grid for game over scenario

        Args:
            grid (List[List[int]]): the games current state

        Returns:
            bool: True if game is over, otherwise false
        """
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                # Check if there is no tile in grid slot
                if grid[i][j] == 0:
                    return False

                # Check if there are available merges
                neighbors = []
                # Left
                if j > 0:
                    left = grid[i][j - 1] == grid[i][j]
                    neighbors.append(left)
                # Right
                if j < len(grid[i]) - 1:
                    right = grid[i][j + 1]
                    neighbors.append(right)
                # Above
                if i > 0:
                    above = grid[i - 1][j]
                    neighbors.append(above)
                # Below
                if i < len(grid) - 1:
                    below = grid[i + 1][j]
                    neighbors.append(below)

                if grid[i][j] in neighbors:
                    return False
        return True

    def copy_grid(item):
        item = (item, [])
        grid = [[], [], [], []]
        for i in range(4):
            grid[i].extend(item[0][i])

        empties = []
        for i in item[1]:
            empties.append(i)
        # return (grid, empties)
        return grid

    def get_available_merges(grid: List[List[int]]) -> int:
        """Counts and returns available merges in given state. Created for using to sort created child states to get more efficient A/B pruning but currently not used since not found performant.

        Args:
            grid (List[List[int]]): Game's state

        Returns:
            int: Count of available merges
        """
        merges = 0

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                # Check if there are available merges
                # Left
                if j > 0:
                    if grid[i][j] == grid[i][j - 1]:
                        merges += 1
                # Right
                if j < len(grid[i]) - 1:
                    if grid[i][j] == grid[i][j + 1]:
                        merges += 1
                # Above
                if i > 0:
                    if grid[i][j] == grid[i - 1][j]:
                        merges += 1
                # Below
                if i < len(grid) - 1:
                    if grid[i][j] == grid[i + 1][j]:
                        merges += 1

        return merges

    def move_left(state):
        newstate = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        empties = []
        for x in range(4):
            placed = -1
            can_merge = True
            for y in range(4):
                col = state[0][x][y]
                if col == 0:
                    continue
                if placed == -1:
                    newstate[x][0] = col
                    placed += 1
                elif newstate[x][placed] == col and can_merge:
                    newstate[x][placed] *= 2
                    can_merge = not can_merge
                else:
                    placed += 1
                    newstate[x][placed] = col
                    can_merge = not can_merge
            for i in range(placed + 1, 4):
                empties.append((x, i))
        return (newstate, empties)

    def move_right(state):
        newstate = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        empties = []
        for x in range(4):
            placed = -1
            can_merge = True
            for y in reversed(range(4)):
                col = state[0][x][y]
                if col == 0:
                    continue
                if placed == -1:
                    newstate[x][3] = col
                    placed = 3
                elif newstate[x][placed] == col and can_merge:
                    newstate[x][placed] *= 2
                    can_merge = not can_merge
                else:
                    placed -= 1
                    newstate[x][placed] = col
                    can_merge = not can_merge
            for i in range(0, placed):
                empties.append((x, i))
        return (newstate, empties)

    def move_up(state):
        newstate = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        empties = []
        for y in range(4):
            placed = -1
            can_merge = True
            for x in range(4):
                col = state[0][x][y]
                if col == 0:
                    continue
                if placed == -1:
                    newstate[0][y] = col
                    placed += 1
                elif newstate[placed][y] == col and can_merge:
                    newstate[placed][y] *= 2
                    can_merge = not can_merge
                else:
                    placed += 1
                    newstate[placed][y] = col
                    can_merge = not can_merge
            for i in range(placed + 1, 4):
                empties.append((i, y))
        return (newstate, empties)

    def move_down(state):
        newstate = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        empties = []
        for y in range(4):
            placed = -1
            can_merge = True
            for x in reversed(range(4)):
                col = state[0][x][y]
                if col == 0:
                    continue
                if placed == -1:
                    newstate[3][y] = col
                    placed = 3
                elif newstate[placed][y] == col and can_merge:
                    newstate[placed][y] *= 2
                    can_merge = not can_merge
                else:
                    placed -= 1
                    newstate[placed][y] = col
                    can_merge = not can_merge
            for i in range(0, placed):
                empties.append((i, y))
        return (newstate, empties)
