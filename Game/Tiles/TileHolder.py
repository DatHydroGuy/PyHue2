import pygame

from Game.Shared import GameObject
from Game.Tiles import Tile


class TileHolder(GameObject):
    def __init__(self, grid_position, draw_position, size, is_pinned, game, transition_times):
        super(TileHolder, self).__init__(grid_position, draw_position, size)
        self.__game = game
        self.__tile = Tile(grid_position, draw_position, size, game)
        self.__is_pinned = is_pinned
        self.__correct_tile = self.__tile.get_grid_position()[::-1]
        self.__transition_times = transition_times

    def set_pinned(self, pin_value):
        self.__is_pinned = pin_value

    def get_pinned(self):
        return self.__is_pinned

    def get_tile(self):
        return self.__tile

    def set_tile(self, new_tile):
        self.__tile = new_tile

    def is_solved(self):
        return self.get_tile().get_grid_position() == self.__correct_tile

    def select(self):
        if self.__is_pinned is False:
            self.get_tile().select()

    def deselect(self):
        self.get_tile().deselect()

    def fade_out(self, timings, ticks):
        ticks = min(ticks, timings[1])
        if timings[0] <= ticks <= timings[1]:
            self.get_tile().fade_out((ticks - timings[0]) / (timings[1] - timings[0]))

    def zero_size(self):
        self.get_tile().zero_size()

    def fade_in(self, timings, ticks):
        ticks = min(ticks, timings[1])
        if timings[0] <= ticks <= timings[1]:
            self.get_tile().fade_in((ticks - timings[0]) / (timings[1] - timings[0]))

    def make_ready(self):
        self.get_tile().make_ready()

    def swap_tiles(self, other):
        if self.__is_pinned is False and other.__is_pinned is False:
            self.__tile, other.__tile = other.__tile, self.__tile
            temp_draw_position = self.get_tile().get_draw_position()
            self.get_tile().set_draw_position(other.get_tile().get_draw_position())
            other.get_tile().set_draw_position(temp_draw_position)

    def update(self):
        self.get_tile().update()

    def render(self):
        rect = self.get_tile().render()
        if self.__is_pinned:
            pygame.draw.circle(self.__game.screen, pygame.Color('black'), rect.center,
                               min(rect.width, rect.height) // 20, 0)
