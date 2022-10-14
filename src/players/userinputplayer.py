from typing import List
from cmath import sqrt
import copy


class UserInputPlayer:
    """Class representing a player that acts based on user input.
    Used for manually testing the program,"""

    def play_round(self, grid: List[List[int]]) -> str:
        """Prompts user to give a direction to play the next move in the game

        Args:
            grid (List[List[int]]): The games current state

        Returns:
            str: Direction to play as a string
        """
        direction = input("Please provide direction to play: [U]p, [D]own, [L]eft, [R]igt")

        if direction.casefold() == "u":
            return "Up"
        elif direction.casefold() == "d":
            return "Down"
        elif direction.casefold() == "l":
            return "Left"
        elif direction.casefold() == "r":
            return "Right"
        else:
            self.play_round(grid)
