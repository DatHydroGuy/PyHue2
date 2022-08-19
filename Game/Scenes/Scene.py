import pygame.display

from Game.Shared import GameConstants


class Scene:
    def __init__(self, game):
        self.__game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def get_game(self):
        return self.__game

    def setup(self):
        pass

    def centre_window_on_screen(self, new_window_size=None):
        window_size = new_window_size if new_window_size is not None else \
            (self.__game.num_tiles_horizontally * GameConstants.TILE_SIZE[0],
             self.__game.num_tiles_vertically * GameConstants.TILE_SIZE[1])
        self.__game.screen = pygame.display.set_mode(window_size, pygame.DOUBLEBUF, 32)
        self.__game.pg_window.position = ((self.__game.screen_width - window_size[0]) // 2,
                                          (self.__game.screen_height - window_size[1]) // 2)

    @staticmethod
    def draw_screen_centered_text(text, font, colour, y_position=0):
        text_surface = font.render(text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.midtop = (GameConstants.SCREEN_SIZE[0] / 2, y_position)
        pygame.display.get_surface().blit(text_surface, text_rectangle)

    @staticmethod
    def draw_left_aligned_text(font, text, colour, x_position, y_position):
        text_surface = font.render(text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.midleft = (x_position, y_position)
        pygame.display.get_surface().blit(text_surface, text_rectangle)

    @staticmethod
    def draw_center_aligned_text(font, text, colour, x_position, y_position):
        text_surface = font.render(text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = (x_position, y_position)
        pygame.display.get_surface().blit(text_surface, text_rectangle)

    @staticmethod
    def draw_right_aligned_text(font, text, colour, x_position, y_position):
        text_surface = font.render(text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.midright = (x_position, y_position)
        pygame.display.get_surface().blit(text_surface, text_rectangle)
