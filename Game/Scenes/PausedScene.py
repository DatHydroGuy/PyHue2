from math import sin

import pygame

from Game.Scenes.Scene import Scene
from ..Shared import GameConstants, ColourTools


class PausedScene(Scene):
    def __init__(self, game):
        super(PausedScene, self).__init__(game)
        self.width = GameConstants.SCREEN_SIZE[0]
        self.height = GameConstants.SCREEN_SIZE[1]
        self.zero_to_one = 0
        self.colour1 = None
        self.colour2 = None
        self.zero_to_one1 = 0
        self.zero_to_one2 = 0
        self.display_surface = None
        self.title_font = None
        self.text_surface = None
        self.merged_surface = None
        self.__pause_start = 0

    def setup(self):
        self.colour1 = self.get_game().colour1
        self.colour2 = self.get_game().colour2
        self.display_surface = pygame.display.get_surface()
        self.width, self.height = self.display_surface.get_size()
        min_dimension = min(self.width, self.height)
        self.title_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.23))
        self.text_surface = self.title_font.render('PAUSED', True, pygame.Color('White'))
        self.merged_surface = self.text_surface.copy()
        self.__pause_start = pygame.time.get_ticks()

    def create_gradient_text(self, start_colour, end_colour, zero_to_one):
        text_rect = self.merged_surface.get_rect()
        text_gradient_surf = self.merged_surface.copy()
        ColourTools.fill_double_gradient(text_gradient_surf, start_colour, end_colour, zero_to_one, text_rect)
        text_gradient_surf.blit(self.merged_surface, text_rect, None, pygame.BLEND_RGBA_MULT)
        return text_gradient_surf

    def draw_gradient_text(self, display_surface, start_colour, end_colour, zero_to_one):
        # inspired by https://stackoverflow.com/questions/29823190/fill-pygame-font-with-custom-pattern
        gradient_text_surface = self.create_gradient_text(start_colour, end_colour, zero_to_one)
        gradient_text_rectangle = gradient_text_surface.get_rect()
        gradient_text_rectangle.center = (self.width / 2, self.height / 2)
        display_surface.blit(gradient_text_surface, gradient_text_rectangle)

    def update(self, start_time=0):
        elapsed1 = (pygame.time.get_ticks() - start_time) / 1500.0
        elapsed2 = (pygame.time.get_ticks() - start_time) / 1000.0
        self.zero_to_one1 = ((sin(elapsed1) * 0.99) + 1.0) * 0.5
        self.zero_to_one2 = ((sin(elapsed2) * 0.99) + 1.0) * 0.5

    def render(self):
        ColourTools.fill_double_gradient(pygame.display.get_surface(), self.colour1, self.colour2, self.zero_to_one1)
        self.draw_gradient_text(pygame.display.get_surface(), self.colour1, self.colour2, self.zero_to_one2)

    def handle_events(self, events):
        super(PausedScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            # If window loses focus, store the paused time so that we can subtract it from the game time at the end.
            if event.type == pygame.ACTIVEEVENT:
                if event.state == 1:
                    if event.gain == 0:
                        pass
                        # self.pause_start = pygame.time.get_ticks()
                    else:
                        # self.paused_time += (pygame.time.get_ticks() - self.pause_start)
                        # self.pause_start = 0
                        self.get_game().pause_end()
                        self.get_game().change_scene(3)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()