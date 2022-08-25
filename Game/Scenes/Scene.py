from __future__ import annotations

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

    def centre_window_on_screen(self, new_window_size: tuple[int, int] = None) -> None:
        window_size = new_window_size if new_window_size is not None else \
            (self.__game.num_tiles_horizontally * GameConstants.TILE_SIZE[0],
             self.__game.num_tiles_vertically * GameConstants.TILE_SIZE[1])
        self.__game.screen = pygame.display.set_mode(window_size, pygame.DOUBLEBUF, 32)
        self.__game.pg_window.position = ((self.__game.screen_width - window_size[0]) // 2,
                                          (self.__game.screen_height - window_size[1]) // 2)

    @staticmethod
    def draw_screen_centered_text(text: str, font: pygame.font.Font, colour: pygame.Color, y_position: int = 0) -> None:
        text_surface = font.render(text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.midtop = (GameConstants.SCREEN_SIZE[0] / 2, y_position)
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
