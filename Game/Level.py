from Game.Grid import Grid
from Game.Shared import GameConstants
from Game.Shared.FileTools import FileTools


class Level:
    def __init__(self, game, columns, rows, pastel=0.5, spread=1.0, pins=GameConstants.GRID_PINS_RANDOMISED,
                 corner_colours=None):
        self.__file = FileTools()
        self.__game = game
        self.__pastel = pastel
        self.__spread = spread
        self.__pins = pins
        self.__game_grid = Grid(game, columns, rows, pastel, spread, pins, corner_colours)
        self.__current_level = 0

    def __str__(self):
        return str(self.__current_level)

    def get_game_grid(self):
        return self.__game_grid

    def get_pastel(self):
        return self.__pastel

    def get_spread(self):
        return self.__spread

    def get_pins(self):
        return self.__pins

    def load_next_level(self):
        self.__current_level += 1
        level_found = False
        if self.__file.check_for_levels_file():
            level_found = self.load(self.__current_level)
        else:
            self.load_random()
        return level_found

    def load_options_screen(self):
        self.__current_level = 0
        self.__game.change_scene(0)

    def load_random(self):
        self.__current_level = 0
        width = self.__game.num_tiles_horizontally
        height = self.__game.num_tiles_vertically
        self.__game.set_size(width, height)
        self.__game_grid = Grid(self.__game, width, height, self.__pastel, self.__spread, self.__pins)

    def load(self, level_number):
        self.__current_level = level_number
        width, height, corner_colours = self.__file.read_level(level_number)
        if width == -1 or height == -1 or corner_colours is None:
            # No more levels left in the levels01.dat file, so send user back to options screen
            self.load_options_screen()
            return False
        else:
            self.__game.set_size(width, height)
            self.__game_grid = Grid(self.__game, width, height, self.__pastel, self.__spread, self.__pins,
                                    corner_colours)
            return True
