from __future__ import annotations

import os
from random import uniform

import pygame

import Game
from Game.Scenes.Scene import Scene
from Game.Shared import ColourTools, GameConstants


class TitleScene(Scene):
    def __init__(self, game: Game.PyHue2) -> None:
        super(TitleScene, self).__init__(game)
        colour1 = (uniform(0.0, 1.0), uniform(0.0, 1.0), uniform(0.0, 1.0))
        colour2 = ColourTools.generate_new_colour([colour1], 0.5, 1.0)
        colour3 = ColourTools.generate_new_colour([colour1, colour2], 0.0, 1.0)
        self.colour1 = pygame.Color(*[int(256 * x) for x in colour1])
        self.colour2 = pygame.Color(*[int(256 * x) for x in colour2])
        self.colour3 = pygame.Color(*[int(256 * x) for x in colour3])
        self.loop = True
        self.heart = '♥'  # Use Alt + Numeric pad 3 key
        self.width = GameConstants.WINDOW_SIZE[0]
        self.height = GameConstants.WINDOW_SIZE[1]
        self.zero_to_one1 = 0
        self.zero_to_one2 = 0

        min_dimension = min(self.width, self.height)
        self.basic_font = self.create_font(int(min_dimension * 0.06))
        self.title_font = self.create_font(int(min_dimension * 0.35))
        self.heart_font = pygame.font.Font(os.path.join(GameConstants.ASSET_DIR, GameConstants.SYM_FONT_FILE),
                                           int(min_dimension * 0.43))
        self.text_surface = self.title_font.render('I    Hue', True, pygame.Color('White'))
        self.heart_surface = self.heart_font.render('{0}'.format(self.heart), True, pygame.Color('White'))
        heart_rect = self.heart_surface.get_rect()
        heart_rect.center = (min_dimension * 0.29, min_dimension * 0.125)
        self.merged_surface = self.text_surface.copy()
        self.merged_surface.blit(self.heart_surface, heart_rect)

    def draw_instructions(self) -> None:
        self.draw_screen_centered_text('Press a key or click mouse to play.', font=self.basic_font,
                                       colour=self.colour3, y_position=int(self.height * 0.7))
        self.draw_screen_centered_text('Press Esc to exit.', font=self.basic_font,
                                       colour=self.colour3, y_position=int(self.height * 0.8))

    def create_gradient_text(self, start_colour: pygame.Color, end_colour: pygame.Color, zero_to_one: float) -> \
            pygame.Surface:
        text_rect = self.merged_surface.get_rect()
        text_gradient_surf = self.merged_surface.copy()
        ColourTools.fill_double_gradient(text_gradient_surf, start_colour, end_colour, zero_to_one, text_rect)
        text_gradient_surf.blit(self.merged_surface, text_rect, None, pygame.BLEND_RGBA_MULT)
        return text_gradient_surf

    def draw_gradient_text(self, display_surface: pygame.Surface, start_colour: pygame.Color, end_colour: pygame.Color,
                           zero_to_one: float) -> None:
        # inspired by https://stackoverflow.com/questions/29823190/fill-pygame-font-with-custom-pattern
        gradient_text_surface = self.create_gradient_text(start_colour, end_colour, zero_to_one)
        gradient_text_rectangle = gradient_text_surface.get_rect()
        gradient_text_rectangle.center = (self.width / 2, self.height / 3)
        display_surface.blit(gradient_text_surface, gradient_text_rectangle)

    def update(self, start_time: int = 0) -> None:
        self.zero_to_one1 = self.update_colours(1500.0, start_time)
        self.zero_to_one2 = self.update_colours(1000.0, start_time)

    def render(self) -> None:
        # TODO re-add following lines
        ColourTools.fill_double_gradient(pygame.display.get_surface(), self.colour1, self.colour2, self.zero_to_one1)
        self.draw_gradient_text(pygame.display.get_surface(), self.colour1, self.colour2, self.zero_to_one2)
        self.draw_instructions()

        self.get_game().colour1 = pygame.Color(self.colour1[0], self.colour1[1], self.colour1[2])
        self.get_game().colour2 = pygame.Color(self.colour2[0], self.colour2[1], self.colour2[2])

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(TitleScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.get_game().change_scene(1)  # OptionsScene

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
                else:
                    self.get_game().change_scene(1)  # OptionsScene
