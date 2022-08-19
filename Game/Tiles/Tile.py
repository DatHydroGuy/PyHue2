import math

import pygame

from Game.Shared import GameObject, GameConstants


class Tile(GameObject):
    state = {"None": 0, "Selected": 1, "FadeOut": 2, "FadeIn": 3}

    def __init__(self, grid_position, draw_position, size, game):
        super(Tile, self).__init__(grid_position, draw_position, size)
        self.__game = game
        self.__colour = [100, 100, 100]
        self.__state = self.state["None"]
        self.__grid_position = grid_position
        self.__start_time = pygame.time.get_ticks()
        self.__inflate = 0

    def get_game(self):
        return self.__game

    def get_colour(self):
        return self.__colour

    def set_colour(self, new_colour):
        self.__colour = new_colour

    def deselect(self):
        self.__state = self.state["None"]

    def select(self):
        if self.__state == self.state["None"]:
            self.__state = self.state["Selected"]
            self.__start_time = pygame.time.get_ticks()
        elif self.__state == self.state["Selected"]:
            self.__state = self.state["None"]
        else:
            pass

    def is_selected(self):
        return self.__state == self.state["Selected"]

    def get_hit_sound(self):
        pass

    def get_image(self):
        return pygame.Surface(self.get_size())

    def get_rectangle(self):
        return self.get_image().get_rect(topleft=self.get_draw_position()).inflate(self.__inflate, self.__inflate)

    def fade_out(self, progress):
        self.__inflate = -GameConstants.TILE_SIZE[0] * progress
        self.__state = self.state["FadeOut"]

    def zero_size(self):
        self.set_size((0, 0))

    def fade_in(self, progress):
        self.__inflate = GameConstants.TILE_SIZE[0] * (progress - 1)
        self.__state = self.state["FadeIn"]

    def make_ready(self):
        self.__inflate = 0
        self.set_size(GameConstants.TILE_SIZE)
        self.__state = self.state["None"]

    def update(self):
        if self.__state == self.state["Selected"]:
            # Need to pulse the tile by expanding and shrinking
            duration = (pygame.time.get_ticks() - self.__start_time) / 250
            self.__inflate = int(10 * math.sin(duration))
        elif self.__state == self.state["None"]:
            self.__inflate = 0
        elif self.__state == self.state["FadeOut"]:
            if self.get_size()[0] <= 0:
                self.__inflate = -GameConstants.TILE_SIZE[0]
        elif self.__state == self.state["FadeIn"]:
            if self.get_size()[0] >= GameConstants.TILE_SIZE[0]:
                self.__inflate = 0
                self.__state = self.state["None"]
        self.set_size((GameConstants.TILE_SIZE[0] + self.__inflate, GameConstants.TILE_SIZE[1] + self.__inflate))

    def render(self):
        tile_image = self.get_image()
        tile_image.fill(self.get_colour())
        tile_rect = self.get_rectangle()

        self.__game.screen.blit(tile_image, tile_rect)
        return tile_rect
