from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class BrowserGame:
    def __init__(self):
        self.url = "https://play2048.co/"
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )

    def start_game(self):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, "ez-accept-all").click()
        self.game = self.driver.find_element(By.TAG_NAME, "body")

    def move_up(self):
        self.game.send_keys(Keys.ARROW_UP)

    def move_down(self):
        self.game.send_keys(Keys.ARROW_DOWN)

    def move_left(self):
        self.game.send_keys(Keys.ARROW_LEFT)

    def move_right(self):
        self.game.send_keys(Keys.ARROW_RIGHT)

    def read_grid(self):
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
            tile_val = int(tile.text)
            print(f"col: {tile_col} - row {tile_row} - value: {tile_val}")
            grid[tile_row][tile_col] = tile_val

        return grid
