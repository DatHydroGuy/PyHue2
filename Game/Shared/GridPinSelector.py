from random import randint

from Game.Shared import GameConstants


class GridPinSelector:
    def __init__(self, grid):
        self.grid = grid
        self.__rows = len(grid)
        self.__columns = len(grid[0])

    def generate_grid_pins(self, pins=GameConstants.GRID_PINS_RANDOMISED):
        grid_pin_type = randint(0, 6) if pins == GameConstants.GRID_PINS_RANDOMISED else pins
        if grid_pin_type == GameConstants.GRID_PINS_CORNERS:
            self.generate_corners_grid_pins()
        elif grid_pin_type == GameConstants.GRID_PINS_VERTICAL:
            self.generate_vertical_grid_pins()
        elif grid_pin_type == GameConstants.GRID_PINS_HORIZONTAL:
            self.generate_horizontal_grid_pins()
        elif grid_pin_type == GameConstants.GRID_PINS_BORDERS:
            self.generate_borders_grid_pins()
        elif grid_pin_type == GameConstants.GRID_PINS_ALTERNATING:
            self.generate_alternating_grid_pins()
        elif grid_pin_type == GameConstants.GRID_PINS_DIAGONAL:
            self.generate_diagonal_grid_pins()
        elif grid_pin_type == GameConstants.GRID_PINS_RANDOM_DIAGONAL:
            self.generate_random_diagonal_grid_pins()
        else:  # 7
            self.generate_random_grid_pins()

    def generate_corners_grid_pins(self):
        self.grid[0][0].set_pinned(True)
        self.grid[0][self.__columns - 1].set_pinned(True)
        self.grid[self.__rows - 1][0].set_pinned(True)
        self.grid[self.__rows - 1][self.__columns - 1].set_pinned(True)

    def generate_vertical_grid_pins(self):
        for i in range(self.__rows):
            self.grid[i][0].set_pinned(True)
            self.grid[i][self.__columns - 1].set_pinned(True)

    def generate_horizontal_grid_pins(self):
        for i in range(self.__columns):
            self.grid[0][i].set_pinned(True)
            self.grid[self.__rows - 1][i].set_pinned(True)

    def generate_borders_grid_pins(self):
        self.generate_vertical_grid_pins()
        self.generate_horizontal_grid_pins()

    def generate_alternating_grid_pins(self):
        for row in range(self.__rows):
            for col in range(self.__columns):
                if row % 2 == 0 and col % 2 == 0:
                    self.grid[row][col].set_pinned(True)

    def generate_diagonal_grid_pins(self):
        for row in range(self.__rows):
            for col in range(self.__columns):
                if (row + col) % 2 == 0:
                    self.grid[row][col].set_pinned(True)

    def generate_random_diagonal_grid_pins(self):
        gap = randint(3, min(self.__rows, self.__columns))
        for row in range(self.__rows):
            for col in range(self.__columns):
                if (row + col) % gap == 0:
                    self.grid[row][col].set_pinned(True)

    def generate_random_grid_pins(self):
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
