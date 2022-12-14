from __future__ import annotations

from random import randint

import Game
from Game.Grid import Grid
from Game.Shared import GameConstants, FileTools


class Level:
    def __init__(self, game: Game.PyHue2, columns: int, rows: int, pastel: float = 0.5, spread: float = 1.0,
                 pins: int = GameConstants.GRID_PINS_RANDOMISED, corner_colours: list[list[int]] = None) -> None:
        self.__file = FileTools()
        self.__game = game
        self.__pastel = pastel
        self.__spread = spread
        self.__pins = randint(GameConstants.GRID_PINS_CORNERS, GameConstants.GRID_PINS_RANDOMISED - 1) if \
            pins == GameConstants.GRID_PINS_RANDOMISED else pins
        self.__pin_spread = randint(3, min(columns, rows))
        self.__game_grid = Grid(game, columns, rows, pastel, spread, self.__pins, corner_colours)
        self.__current_level = 0

    def __str__(self) -> str:
        return str(self.__current_level)

    def get_game_grid(self) -> Game.Grid:
        return self.__game_grid

    def get_pastel(self) -> float:
        return self.__pastel

    def get_spread(self) -> float:
        return self.__spread

    def get_pins(self) -> int:
        return self.__pins

    def get_pin_spread(self) -> int:
        return self.__pin_spread

    def load_next_level(self) -> bool:
        self.__current_level += 1
        level_found = False
        if self.__file.check_for_levels_file():
            level_found = self.load_level(self.__current_level, True)
        else:
            self.load_random()
        return level_found

    def load_options_screen(self) -> None:
        self.__current_level = 0
        self.__game.change_scene(7)  # LevelsCompleteScene

    def load_random(self) -> None:
        self.__current_level = 0
        width = self.__game.num_tiles_horizontally
        height = self.__game.num_tiles_vertically
        self.__game.set_size(width, height)
        self.__game_grid = Grid(self.__game, width, height, self.__pastel, self.__spread, self.__pins)

    def load_level(self, level_number: int, is_from_preview: bool) -> bool:
        self.__current_level = level_number
        width, height, pins, corner_colours, pin_locations = self.__file.read_level(level_number)
        if width == -1 or height == -1 or pins == -1 or corner_colours is None:
            # No more levels left in the levels01.dat file, so send user back to options screen
            self.load_options_screen()
            return False
        # elif pins != GameConstants.GRID_PINS_CUSTOM and len(pin_locations) > 0:
        #     # Corrupt level data
        #     self.load_options_screen()
        #     return False
        else:
            self.__game.set_size(width, height)
            self.__game_grid = Grid(self.__game, width, height, self.__pastel, self.__spread, pins,
                                    corner_colours, not is_from_preview)
            self.__game_grid.set_cell_pins(pin_locations)
            return True

    def edit_level(self, columns: int, rows: int, pins: int = GameConstants.GRID_PINS_RANDOMISED,
                   corner_colours: list[list[int]] = None, from_preview: bool = True,
                   try_level: bool = False) -> None:
        self.__game.set_size(columns, rows)
        self.__game_grid = Grid(self.__game, columns, rows, self.__pastel, self.__spread, pins,
                                corner_colours, from_preview, try_level)
