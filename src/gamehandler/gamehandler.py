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
        return False

    def get_tiles(self, grid: List[List[int]]) -> List[str]:
        tile_list = []
        for x, row in enumerate(grid):
            for y, col in enumerate(row):
                if col > 0:
                    tile_list.append(f"col: {y} - row {x} - value {col}")

        return tile_list
