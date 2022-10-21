from __future__ import annotations

from random import random, shuffle

from Game.Shared import *
from Game.Tiles import *


class Grid:
    def __init__(self, game: Game.PyHue2, columns: int, rows: int, pastel: float = 0.5, spread: float = 1.0,
                 pins: int = GameConstants.GRID_PINS_RANDOMISED, corner_colours: list[pygame.Color] = None,
                 preview: bool = False, try_level: bool = False) -> None:
        self.__game = game
        self.__columns = columns
        self.__rows = rows
        self.__curr_selection = None
        self.__solved_time = 999999999
        self.__incorrect_tiles = None
        self.__current_level = 0
        self.__number_of_moves = 0
        self.__start_time = pygame.time.get_ticks()
        self.__solved = False
        self.__shuffled = False
        self.__preview = preview
        self.__try = try_level
        pixels_per_tile = int(min(GameConstants.WINDOW_SIZE[0] / columns, GameConstants.WINDOW_SIZE[1] / rows, 30))
        self.scaled_tile_size = (pixels_per_tile, pixels_per_tile)
        self.__preview_x_offset = (GameConstants.WINDOW_SIZE[0] - self.scaled_tile_size[
            0] * columns) // 2 if preview else 0
        self.__tile_size = self.scaled_tile_size if preview else GameConstants.TILE_SIZE
        self.transition = TransitionCreator(global_start=GameConstants.FADE_OUT_START,
                                            global_fade_out=GameConstants.FADE_OUT_DURATION,
                                            global_pause=GameConstants.FADE_PAUSE,
                                            global_fade_in=GameConstants.FADE_IN_DURATION,
                                            local_fade_out=GameConstants.TILE_FADE_OUT_DURATION,
                                            local_fade_in=GameConstants.TILE_FADE_IN_DURATION)
        self.transition_matrix = self.transition.choose_transition(columns, rows)
        self.fade_out_start = GameConstants.FADE_OUT_START
        self.fade_out_end = self.fade_out_start + GameConstants.FADE_OUT_DURATION
        self.fade_in_start = self.fade_out_end + GameConstants.FADE_PAUSE
        self.fade_in_end = self.fade_in_start + GameConstants.FADE_IN_DURATION
        self.__game_grid = [
            [TileHolder((x, y), (self.__preview_x_offset + x * self.__tile_size[0], y * self.__tile_size[1]),
                        self.__tile_size, (x, y) in self.__game.custom_pins, self.__game, preview)
             for x in range(columns)] for y in range(rows)]
        self.generate_corner_colours(corner_colours, pastel, spread)
        gps = GridPinSelector(self.__game_grid)
        gps.generate_grid_pins(pins)
        self.generate_tile_array(self.__tile_size)

    def get_grid_size(self) -> tuple[int, int]:
        return self.__columns, self.__rows

    def toggle_cell_pin(self, cell_x: int, cell_y: int) -> None:
        self.__game_grid[cell_y][cell_x].toggle_pinned()

    def set_cell_pins(self, pin_locations: list[tuple[int, int]]) -> None:
        for pin_location in pin_locations:
            self.__game_grid[pin_location[1]][pin_location[0]].set_pinned(True)

    def get_cell_pins(self) -> list[tuple[int, int]]:
        pin_locations = []
        for r_index, row in enumerate(self.__game_grid):
            for c_index, col in enumerate(row):
                if self.__game_grid[r_index][c_index].get_pinned():
                    pin_locations.append((c_index, r_index))
        return pin_locations

    def get_solved_time(self) -> int:
        return self.__solved_time

    def is_solved(self) -> bool:
        return self.__solved

    def is_in_try_mode(self) -> bool:
        return self.__try

    def is_shuffled(self) -> bool:
        return self.__shuffled

    def reset(self) -> None:
        self.__shuffled = self.__preview
        self.__solved = False
        self.__start_time = pygame.time.get_ticks()
        self.fade_out_start = GameConstants.FADE_OUT_START
        self.fade_out_end = self.fade_out_start + GameConstants.FADE_OUT_DURATION
        self.fade_in_start = self.fade_out_end + GameConstants.FADE_PAUSE
        self.fade_in_end = self.fade_in_start + GameConstants.FADE_IN_DURATION

    def get_number_of_moves(self) -> int:
        return self.__number_of_moves

    def get_tile_holders(self) -> list[list[Game.Tiles.TileHolder]]:
        return self.__game_grid

    def get_number_of_incorrect_tiles(self) -> int:
        return self.__incorrect_tiles

    def generate_corner_colours(self, corner_colours: list[pygame.Color], pastel_factor: float,
                                colour_spread: float) -> None:
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

    def generate_tile_array(self, cell_size: tuple[int, int]) -> None:
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
                tile_rect = pygame.Rect(self.__preview_x_offset + column * cell_width, row * cell_height, cell_width,
                                        cell_height)
                tile = Tile((row, column), tile_rect.topleft, (cell_width, cell_height), self.__game, self.__preview)
                tile.set_colour(colour)
                self.__game_grid[row][column].set_tile(tile)

    def fade_out_tile_array(self) -> None:
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.get_tile_holders()[row][column].get_pinned() is False:
                    self.get_tile_holders()[row][column].fade_out(self.transition_matrix[row][column][:2],
                                                                  pygame.time.get_ticks() - self.__start_time)

    def fade_in_tile_array(self) -> None:
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.get_tile_holders()[row][column].get_pinned() is False:
                    self.get_tile_holders()[row][column].fade_in(self.transition_matrix[row][column][2:],
                                                                 pygame.time.get_ticks() - self.__start_time)

    def shuffle_tile_array(self) -> None:
        flat_array = [item for row in self.get_tile_holders() for item in row if item.get_pinned() is False]
        shuffle(flat_array)
        counter = 0
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.get_tile_holders()[row][column].get_pinned() is False:
                    self.get_tile_holders()[row][column].zero_size()
                    self.get_tile_holders()[row][column].swap_tiles(flat_array[counter])
                    counter += 1

    def ready_tile_array(self) -> None:
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.get_tile_holders()[row][column].get_pinned() is False:
                    self.get_tile_holders()[row][column].make_ready()

    def set_current_selection(self, xy_of_selected_cell: tuple[int, int]) -> None:
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

    def update(self) -> None:
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

    def render(self) -> None:
        for row, tile_holder_row in enumerate(self.__game_grid):
            for col, tile_holder in enumerate(tile_holder_row):
                if self.__curr_selection != (col, row):
                    tile_holder.render()
        if self.__curr_selection is not None:
            self.__game_grid[self.__curr_selection[1]][self.__curr_selection[0]].render()
