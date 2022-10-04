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
        print(f"Uniformity heuristic: {self.uniform_heuristic(grid)}")
        print(f"Monotonicity heuristic: {self.monotonicity_heuristic(grid)}")
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

    def greedy_heuristic(self, state):
        pass

    def empty_heuristic(self, state):
        pass

    def uniform_heuristic(self, state):
        different_tile_values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for row in state:
            for col in row:
                if col == 0:
                    continue
                if col == 2:
                    different_tile_values[0] += 1
                else:
                    if len(different_tile_values) < sqrt(col).real:
                        for _ in range(sqrt(col) - len(different_tile_values)):
                            different_tile_values.append(0)

                    different_tile_values[int(sqrt(col).real) - 1] += 1
        return sum([x**3 for x in different_tile_values])

    def monotonicity_heuristic(self, state):
        best = -1
        ted_state = copy.deepcopy(state)
        for _ in range(4):  # Board is evaluated from all 4 directions
            current = 0
            for row_no in range(4):
                for col_no in range(3):
                    if ted_state[row_no][col_no] == 0:
                        continue
                    if ted_state[row_no][col_no] >= ted_state[row_no][col_no + 1]:
                        current += 1
            for col_no in range(4):
                for row_no in range(3):
                    if ted_state[row_no][col_no] == 0:
                        continue
                    if ted_state[row_no][col_no] >= ted_state[row_no + 1][col_no]:
                        current += 1

            if best >= current:
                print("NEW BEST")
            best = best if best >= current else current
            print(ted_state)

            ted_state = list(zip(*ted_state[::-1]))
        return best

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
                for j in range(len(row)):
                    newrow.append(state[j][i])
                rotated_state.append(newrow)

            return rotated_state

        elif direction == "down":
            rotated_state = []

            for i, row in enumerate(state):
                newrow = []
                for j in range(len(row)):
                    newrow.insert(0, state[j][i])
                rotated_state.insert(0, newrow)

            return rotated_state
