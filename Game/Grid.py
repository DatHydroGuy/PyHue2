from random import random, shuffle

from Game.Shared import *
from Game.Shared.GridPinSelector import GridPinSelector
from Game.Shared.TransitionCreator import TransitionCreator
from Game.Tiles import *


class Grid:
    def __init__(self, game, columns, rows, pastel=0.5, spread=1.0, corner_colours=None):
        self.__game = game
        self.__columns = columns
        self.__rows = rows
        self.__curr_selection = None
        self.__solved_time = 999999999
        self.__incorrect_tiles = None
        self.__current_level = 0
        self.__number_of_moves = 0
        self.__start_time = pygame.time.get_ticks()
        self.transition = TransitionCreator(global_start=1000, global_fade_out=2500, global_pause=500,
                                            global_fade_in=2500, local_fade_out=200, local_fade_in=200)
        self.__solved = False
        self.__shuffled = False
        self.transition_matrix = self.transition.choose_transition(columns,
                                                                   rows,
                                                                   GameConstants.TILE_SIZE[0],
                                                                   GameConstants.TILE_SIZE[1])
        self.fade_out_start = self.transition.global_start
        self.fade_out_end = self.fade_out_start + self.transition.global_fade_out
        self.fade_in_start = self.fade_out_end + self.transition.global_pause
        self.fade_in_end = self.fade_in_start + self.transition.global_fade_in
        self.__game_grid = [[TileHolder((x, y), [x * GameConstants.TILE_SIZE[0], y * GameConstants.TILE_SIZE[1]],
                                        (10, 10), False, self.__game, self.transition_matrix[y][x])
                             for x in range(columns)] for y in range(rows)]
        self.generate_corner_colours(corner_colours, pastel, spread)
        gps = GridPinSelector(self.__game_grid)
        gps.generate_grid_pins()
        self.generate_tile_array(GameConstants.TILE_SIZE)

    def get_grid_size(self):
        return self.__columns, self.__rows

    def get_solved_time(self):
        return self.__solved_time

    def is_solved(self):
        return self.__solved

    def is_shuffled(self):
        return self.__shuffled

    def reset(self):
        self.__shuffled = False
        self.__solved = False
        self.__start_time = pygame.time.get_ticks()
        self.fade_out_start = self.transition.global_start
        self.fade_out_end = self.fade_out_start + self.transition.global_fade_out
        self.fade_in_start = self.fade_out_end + self.transition.global_pause
        self.fade_in_end = self.fade_in_start + self.transition.global_fade_in

    def get_number_of_moves(self):
        return self.__number_of_moves

    def get_tile_holders(self):
        return self.__game_grid

    def get_tile_holder(self, row, column):
        return self.__game_grid[row][column]

    def get_number_of_incorrect_tiles(self):
        return self.__incorrect_tiles

    def generate_corner_colours(self, corner_colours, pastel_factor, colour_spread):
        colours = []
        if corner_colours is None:
            base_offset = random() * (1.0 - colour_spread)
            for _ in range(4):
                colours.append(ColourTools.generate_new_colour(colours, pastel_factor=pastel_factor,
                                                               colour_spread=colour_spread, base_offset=base_offset))

            colours = [[int(256 * x) for x in colour] for colour in colours]
        else:
            colours = corner_colours

        self.__game_grid[0][0].get_tile().set_colour(pygame.Color(colours[0][0], colours[0][1], colours[0][2]))
        self.__game_grid[0][self.__columns - 1].get_tile().set_colour(
            pygame.Color(colours[1][0], colours[1][1], colours[1][2]))
        self.__game_grid[self.__rows - 1][0].get_tile().set_colour(
            pygame.Color(colours[2][0], colours[2][1], colours[2][2]))
        self.__game_grid[self.__rows - 1][self.__columns - 1].get_tile().set_colour(
            pygame.Color(colours[3][0], colours[3][1], colours[3][2]))

    def generate_tile_array(self, cell_size):
        cell_width, cell_height = cell_size
        for row in range(self.__rows):
            row_step = row / float(self.__rows - 1)
            start_colour = ColourTools.generate_colour_components(
                self.__game_grid[0][0].get_tile().get_colour(),
                self.__game_grid[self.__rows - 1][0].get_tile().get_colour(), row_step)
            end_colour = ColourTools.generate_colour_components(
                self.__game_grid[0][self.__columns - 1].get_tile().get_colour(),
                self.__game_grid[self.__rows - 1][self.__columns - 1].get_tile().get_colour(), row_step)
            for column in range(self.__columns):
                col_step = column / float(self.__columns - 1)
                colour = ColourTools.generate_colour_components(start_colour, end_colour, col_step)
                tile_rect = pygame.Rect(column * cell_width, row * cell_height, cell_width, cell_height)
                tile = Tile((row, column), tile_rect.topleft, (cell_width, cell_height), self.__game)
                tile.set_colour(colour)
                self.__game_grid[row][column].set_tile(tile)

    def fade_out_tile_array(self):
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.get_tile_holders()[row][column].get_pinned() is False:
                    self.get_tile_holders()[row][column].fade_out(self.transition_matrix[row][column][:2],
                                                                  pygame.time.get_ticks() - self.__start_time)

    def fade_in_tile_array(self):
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.get_tile_holders()[row][column].get_pinned() is False:
                    self.get_tile_holders()[row][column].fade_in(self.transition_matrix[row][column][2:],
                                                                 pygame.time.get_ticks() - self.__start_time)

    def shuffle_tile_array(self):
        flat_array = [item for row in self.get_tile_holders() for item in row if item.get_pinned() is False]
        shuffle(flat_array)
        counter = 0
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.get_tile_holders()[row][column].get_pinned() is False:
                    self.get_tile_holders()[row][column].zero_size()
                    self.get_tile_holders()[row][column].swap_tiles(flat_array[counter])
                    counter += 1

    def ready_tile_array(self):
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.get_tile_holders()[row][column].get_pinned() is False:
                    self.get_tile_holders()[row][column].make_ready()

    def swap_tiles(self, row1, col1, row2, col2):
        self.__game_grid[row1][col1], self.__game_grid[row2][col2] = \
            self.__game_grid[row2][col2], self.__game_grid[row1][col1]

    def get_current_selection(self):
        return self.__curr_selection

    def set_current_selection(self, xy_of_selected_cell):
        if self.__game_grid[xy_of_selected_cell[1]][xy_of_selected_cell[0]].get_pinned() or not self.__shuffled:
            return

        # if nothing selected, select the clicked cell
        if self.__curr_selection is None:
            self.__game_grid[xy_of_selected_cell[1]][xy_of_selected_cell[0]].select()
            self.__curr_selection = xy_of_selected_cell
        else:
            # de-select the currently selected cell
            self.__game_grid[self.__curr_selection[1]][self.__curr_selection[0]].deselect()
            if self.__curr_selection != xy_of_selected_cell:
                # swap cells
                self.__game_grid[self.__curr_selection[1]][self.__curr_selection[0]].swap_tiles(
                    self.__game_grid[xy_of_selected_cell[1]][xy_of_selected_cell[0]]
                )
                self.__number_of_moves += 1
            self.__curr_selection = None

    def update(self):
        if not self.__shuffled:
            if self.fade_out_start <= pygame.time.get_ticks() - self.__start_time <= self.fade_out_end:
                self.fade_out_tile_array()
            elif self.fade_out_end < pygame.time.get_ticks() - self.__start_time < self.fade_in_start:
                self.shuffle_tile_array()
            elif self.fade_in_start <= pygame.time.get_ticks() - self.__start_time <= self.fade_in_end:
                self.fade_in_tile_array()
            elif self.fade_in_end < pygame.time.get_ticks() - self.__start_time:
                self.ready_tile_array()
                self.__shuffled = True

            for tile_holder_row in self.__game_grid:
                for tile_holder in tile_holder_row:
                    tile_holder.update()

        else:
            self.__incorrect_tiles = 0
            for tile_holder_row in self.__game_grid:
                for tile_holder in tile_holder_row:
                    tile_holder.update()
                    if not tile_holder.is_solved():
                        self.__incorrect_tiles += 1
            if self.__incorrect_tiles == 0 and not self.__solved:
                self.__solved_time = pygame.time.get_ticks() - self.__start_time - self.fade_in_end
                self.__solved = True

    def render(self):
        for row, tile_holder_row in enumerate(self.__game_grid):
            for col, tile_holder in enumerate(tile_holder_row):
                if self.__curr_selection != (col, row):
                    tile_holder.render()
        if self.__curr_selection is not None:
            self.__game_grid[self.__curr_selection[1]][self.__curr_selection[0]].render()
