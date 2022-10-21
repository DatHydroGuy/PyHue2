from random import randint

import Game.Tiles
from Game.Shared import GameConstants


class GridPinSelector:
    def __init__(self, grid: list[list[Game.Tiles.TileHolder]]) -> None:
        self.grid = grid
        self.__rows = len(grid)
        self.__columns = len(grid[0])
        self.pin_lookup = {
            GameConstants.GRID_PINS_CORNERS: self.generate_corners_grid_pins,
            GameConstants.GRID_PINS_VERTICAL: self.generate_vertical_grid_pins,
            GameConstants.GRID_PINS_HORIZONTAL: self.generate_horizontal_grid_pins,
            GameConstants.GRID_PINS_BORDERS: self.generate_borders_grid_pins,
            GameConstants.GRID_PINS_ALTERNATING: self.generate_alternating_grid_pins,
            GameConstants.GRID_PINS_DIAGONAL: self.generate_diagonal_grid_pins,
            GameConstants.GRID_PINS_RANDOM_DIAGONAL: self.generate_random_diagonal_grid_pins,
            GameConstants.GRID_PINS_RANDOM: self.generate_random_grid_pins,
            GameConstants.GRID_PINS_KNIGHTS_TOUR: self.generate_knights_tour_grid_pins,
            GameConstants.GRID_PINS_RANDOMISED: self.generate_grid_pins,
            GameConstants.GRID_PINS_CUSTOM: self.generate_custom_grid_pins
        }

    def generate_grid_pins(self, pins: int = GameConstants.GRID_PINS_RANDOMISED) -> None:
        grid_pin_type = randint(GameConstants.GRID_PINS_CORNERS, GameConstants.GRID_PINS_CUSTOM - 1) if \
            pins == GameConstants.GRID_PINS_RANDOMISED else pins
        # print(f'{grid_pin_type}')
        self.pin_lookup[grid_pin_type]()

    def generate_corners_grid_pins(self) -> None:
        self.grid[0][0].set_pinned(True)
        self.grid[0][self.__columns - 1].set_pinned(True)
        self.grid[self.__rows - 1][0].set_pinned(True)
        self.grid[self.__rows - 1][self.__columns - 1].set_pinned(True)

    def generate_vertical_grid_pins(self) -> None:
        for i in range(self.__rows):
            self.grid[i][0].set_pinned(True)
            self.grid[i][self.__columns - 1].set_pinned(True)

    def generate_horizontal_grid_pins(self) -> None:
        for i in range(self.__columns):
            self.grid[0][i].set_pinned(True)
            self.grid[self.__rows - 1][i].set_pinned(True)

    def generate_borders_grid_pins(self) -> None:
        self.generate_vertical_grid_pins()
        self.generate_horizontal_grid_pins()

    def generate_alternating_grid_pins(self) -> None:
        for row in range(self.__rows):
            for col in range(self.__columns):
                if row % 2 == 0 and col % 2 == 0:
                    self.grid[row][col].set_pinned(True)

    def generate_diagonal_grid_pins(self) -> None:
        for row in range(self.__rows):
            for col in range(self.__columns):
                if (row + col) % 2 == 0:
                    self.grid[row][col].set_pinned(True)

    def generate_random_diagonal_grid_pins(self) -> None:
        gap = randint(3, min(self.__rows, self.__columns))
        for row in range(self.__rows):
            for col in range(self.__columns):
                if (row + col) % gap == 0:
                    self.grid[row][col].set_pinned(True)

    def generate_knights_tour_grid_pins(self) -> None:
        for row in range(self.__rows):
            for col in range(self.__columns):
                if row % 2 == 0 and col % 4 == 0 or row % 2 == 1 and col % 4 == 2:
                    self.grid[row][col].set_pinned(True)

    def generate_random_grid_pins(self) -> None:
        pins = []
        min_pins = int(self.__rows * self.__columns * 0.05)
        max_pins = int(self.__rows * self.__columns * 0.1)
        num_random_pins = randint(min_pins, max_pins)
        while len(pins) < num_random_pins:
            row = randint(0, self.__rows - 1)
            col = randint(0, self.__columns - 1)
            if (row, col) not in pins:
                self.grid[row][col].set_pinned(True)
                pins.append((row, col))

    def generate_custom_grid_pins(self) -> None:
        pass
