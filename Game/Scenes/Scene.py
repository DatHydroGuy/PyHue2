from __future__ import annotations

from math import sin
from typing import Callable

import pygame.display

import Game
from Game.Shared import GameConstants


class Scene:
    def __init__(self, game: Game.PyHue2) -> None:
        self.__game = game

    def handle_events(self, events: list[pygame.event.Event]):
        pass

    def update(self) -> None:
        pass

    def render(self) -> None:
        pass

    def get_game(self) -> Game.PyHue2:
        return self.__game

    def setup(self) -> None:
        pass

    @staticmethod
    def update_colours(divisor: float, start_time: int = 0) -> float:
        elapsed = (pygame.time.get_ticks() - start_time) / divisor
        return ((sin(elapsed) * 0.99) + 1.0) * 0.5

    def centre_window_on_screen(self, new_window_size: tuple[int, int] = None) -> None:
        window_size = new_window_size if new_window_size is not None else \
            (self.__game.num_tiles_horizontally * GameConstants.TILE_SIZE[0],
             self.__game.num_tiles_vertically * GameConstants.TILE_SIZE[1])
        self.__game.screen = pygame.display.set_mode(window_size, pygame.DOUBLEBUF, 32)
        self.__game.pg_window.position = ((self.__game.screen_width - window_size[0]) // 2,
                                          (self.__game.screen_height - window_size[1]) // 2)

    @staticmethod
    def button(button_text: str, font: pygame.font, colour: pygame.Color, top_left_x: int, top_left_y: int,
               width: int, height: int, inactive_colour: pygame.Color, active_colour: pygame.Color,
               callback: Callable[[], None] = None) -> None:
        # Taken from https://pythonprogramming.net/pygame-button-function-events/?completed=/pygame-button-function/
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if top_left_x + width > mouse[0] > top_left_x and top_left_y + height > mouse[1] > top_left_y:
            pygame.draw.rect(pygame.display.get_surface(), active_colour, (top_left_x, top_left_y, width, height))

            if click[0] == 1 and callback is not None:
                callback()
        else:
            pygame.draw.rect(pygame.display.get_surface(), inactive_colour, (top_left_x, top_left_y, width, height))

        text_surface = font.render(button_text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = ((top_left_x + (width / 2)), (top_left_y + (height / 2)))
        pygame.display.get_surface().blit(text_surface, text_rectangle)

    @staticmethod
    def draw_screen_centered_text(text: str, font: pygame.font.Font, colour: pygame.Color, y_position: int = 0) -> None:
        text_surface = font.render(text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.midtop = (GameConstants.WINDOW_SIZE[0] / 2, y_position)
        pygame.display.get_surface().blit(text_surface, text_rectangle)

    @staticmethod
    def draw_left_aligned_text(font: pygame.font.Font, text: str, colour: pygame.Color, x_position: int,
                               y_position: int) -> None:
        text_surface = font.render(text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.midleft = (x_position, y_position)
        pygame.display.get_surface().blit(text_surface, text_rectangle)

    @staticmethod
    def draw_center_aligned_text(font: pygame.font.Font, text: str, colour: pygame.Color, x_position: int,
                                 y_position: int) -> None:
        text_surface = font.render(text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (x_position, y_position)
        pygame.display.get_surface().blit(text_surface, text_rectangle)

    @staticmethod
    def draw_right_aligned_text(font: pygame.font.Font, text: str, colour: pygame.Color, x_position: int,
                                y_position: int) -> None:
        text_surface = font.render(text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.midright = (x_position, y_position)
        pygame.display.get_surface().blit(text_surface, text_rectangle)
