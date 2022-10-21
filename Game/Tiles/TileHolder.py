from __future__ import annotations

import pygame

import Game
from Game.Shared import GameObject
from Game.Tiles import Tile


class TileHolder(GameObject):
    def __init__(self, grid_position: tuple[int, int], draw_position: tuple[int, int], size: tuple[int, int],
                 is_pinned: bool, game: Game.PyHue2, preview: bool = False) -> None:
        super(TileHolder, self).__init__(grid_position, draw_position, size)
        self.__game = game
        self.__tile = Tile(grid_position, draw_position, size, game)
        self.__is_pinned = is_pinned
        self.__correct_tile = self.__tile.get_grid_position()[::-1]

    def set_pinned(self, pin_value: bool) -> None:
        self.__is_pinned = pin_value

    def get_pinned(self) -> bool:
        return self.__is_pinned

    def toggle_pinned(self) -> None:
        self.__is_pinned = not self.__is_pinned

    def get_tile(self) -> Tile:
        return self.__tile

    def set_tile(self, new_tile: Tile) -> None:
        self.__tile = new_tile

    def is_solved(self) -> bool:
        return self.get_tile().get_grid_position() == self.__correct_tile

    def select(self) -> None:
        if self.__is_pinned is False:
            self.get_tile().select()

    def deselect(self) -> None:
        self.get_tile().deselect()

    def fade_out(self, timings: tuple[int, int, int, int], ticks: int) -> None:
        ticks = min(ticks, timings[1])
        if timings[0] <= ticks <= timings[1]:
            self.get_tile().fade_out((ticks - timings[0]) / (timings[1] - timings[0]))

    def zero_size(self) -> None:
        self.get_tile().zero_size()

    def fade_in(self, timings: tuple[int, int, int, int], ticks: int) -> None:
        ticks = min(ticks, timings[1])
        if timings[0] <= ticks <= timings[1]:
            self.get_tile().fade_in((ticks - timings[0]) / (timings[1] - timings[0]))

    def make_ready(self) -> None:
        self.get_tile().make_ready()

    def swap_tiles(self, other: TileHolder) -> None:
        if self.__is_pinned is False and other.__is_pinned is False:
            self.__tile, other.__tile = other.__tile, self.__tile
            temp_draw_position = self.get_tile().get_draw_position()
            self.get_tile().set_draw_position(other.get_tile().get_draw_position())
            other.get_tile().set_draw_position(temp_draw_position)

    def update(self) -> None:
        self.get_tile().update()

    def render(self) -> None:
        rect = self.get_tile().render()
        if self.__is_pinned:
            pygame.draw.circle(self.__game.screen, pygame.Color('black'), rect.center, 3, 0)
            pygame.draw.circle(self.__game.screen, pygame.Color('white'), rect.center, 1, 0)
