from typing import List


class GameHandler:
    """Object that provides various information about the game grid"""

    def get_grid_max_value(self, grid: List[List[int]]) -> int:
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

    def game_is_over(self, grid: List[List[int]]) -> bool:
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

    def get_tiles(self, grid: List[List[int]]) -> List[str]:
        """Return list of strings representing each tile on grid

        Args:
            grid (List[List[int]]): the games current state

        Returns:
            List[str]: list of strings representing each tile on grid
        """
        tile_list = []
        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                if col > 0:
                    tile_list.append(f"col: {y} - row {x} - value {col}")

        return tile_list
