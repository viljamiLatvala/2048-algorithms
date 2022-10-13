import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

# <a class="keep-playing-button">Keep going</a>
class BrowserGame:
    """
    A class for representing the browser version of the game 2048,
    and having methods for controlling it
    """

    def __init__(self):
        self.url = "https://play2048.co/"
        self.driver = None
        self.game = None

    def start_game(self):
        """Open browser an navigate to games url. Accept cookie consent"""

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(self.url)
        try:
            cookie_prompt = self.driver.find_element(By.ID, "ez-accept-all")
            cookie_prompt.click()
        except NoSuchElementException:
            pass

        self.game = self.driver.find_element(By.TAG_NAME, "body")

    def quit_game(self):
        """Closes the controlled web browser and reassigns a new webdriver to be ready for possible new games"""
        self.driver.close()

    def move_up(self):
        """Commands the game to move up"""
        self.game = self.driver.find_element(By.TAG_NAME, "body")
        self.game.send_keys(Keys.ARROW_UP)

    def move_down(self):
        """Commands the game to move down"""
        self.game = self.driver.find_element(By.TAG_NAME, "body")
        self.game.send_keys(Keys.ARROW_DOWN)

    def move_left(self):
        """Commands the game to move left"""
        self.game = self.driver.find_element(By.TAG_NAME, "body")
        self.game.send_keys(Keys.ARROW_LEFT)

    def move_right(self):
        """Commands the game to move right"""
        self.game = self.driver.find_element(By.TAG_NAME, "body")
        self.game.send_keys(Keys.ARROW_RIGHT)

    def read_grid(self):
        """Parses the HTML representing the game grid, returns a 2-dimensional array representation"""
        time.sleep(0.08)
        grid = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        tile_container = self.driver.find_element(By.CLASS_NAME, "tile-container")
        tiles = tile_container.find_elements(By.CLASS_NAME, "tile")
        for tile in tiles:
            tile_classes = tile.get_attribute("class")
            position_prefix = "tile-position-"
            tile_pos = tile_classes.find(position_prefix)
            pos_str_start = tile_pos + len(position_prefix)
            pos_str_end = pos_str_start + 3
            pos_str = tile_classes[pos_str_start:pos_str_end]
            tile_col = int(pos_str[0]) - 1
            tile_row = int(pos_str[2]) - 1
            tile_val = int(tile_classes.split(" ")[1].split("-")[1])
            grid[tile_row][tile_col] = tile_val

        return grid
