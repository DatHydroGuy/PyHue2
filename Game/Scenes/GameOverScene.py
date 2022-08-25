from __future__ import annotations
import os.path

import pygame

import Game
from Game.Scenes.Scene import Scene
from Game.Shared import ColourTools, GameConstants


class GameOverScene(Scene):
    def __init__(self, game: Game.PyHue2) -> None:
        super(GameOverScene, self).__init__(game)
        self.begin = False
        self.start_time = None
        self.display_surface = None
        self.surface = None
        self.rect = None
        self.fade_out_start = GameConstants.SOLVED_FADE_IN + GameConstants.SOLVED_PAUSE
        self.fade_out_end = self.fade_out_start + GameConstants.SOLVED_FADE_OUT
        self.fade_end = self.fade_out_end + GameConstants.SOLVED_PAUSE

    def create_fading_heart_surface(self) -> tuple[pygame.Surface, pygame.Rect]:
        heart = '♥'  # Use Alt + Numeric pad 3 key
        window_width = self.get_game().get_grid().get_grid_size()[0] * GameConstants.TILE_SIZE[0]
        window_height = self.get_game().get_grid().get_grid_size()[1] * GameConstants.TILE_SIZE[1]
        min_dimension = min(window_width, window_height)
        heart_font = pygame.font.Font(os.path.join(GameConstants.ASSET_DIR, GameConstants.SYM_FONT_FILE),
                                      int(min_dimension * 1.0))
        heart_surface = ColourTools.blended_text(heart_font, heart, pygame.Color('White'),
                                                 pygame.Color(255, 255, 255, 0))
        heart_rect = heart_surface.get_rect()
        self.display_surface = pygame.display.get_surface()
        display_rect = self.display_surface.get_rect()
        heart_rect.center = display_rect.center
        return heart_surface, heart_rect

    def fade_heart_surface(self, surface: pygame.Surface, rect: pygame.Rect, start_alpha: int, end_alpha: int,
                           curr_time: int, max_time: int = 1000) -> None:
        alpha_increment = (end_alpha - start_alpha) / float(max_time)
        alpha = start_alpha + int(alpha_increment * curr_time)
        surface.set_alpha(alpha)
        self.display_surface.blit(surface, rect)

    def update(self) -> None:
        super(GameOverScene, self).update()
        if not self.begin:
            self.surface, self.rect = self.create_fading_heart_surface()
            self.start_time = pygame.time.get_ticks()
            self.begin = True

        game = self.get_game()
        grid = game.get_grid()
        grid.update()

    def render(self) -> None:
        super(GameOverScene, self).render()
        game = self.get_game()
        grid = game.get_grid()
        grid.render()

        curr_time = pygame.time.get_ticks() - self.start_time
        if curr_time <= GameConstants.SOLVED_FADE_IN:
            self.fade_heart_surface(self.surface, self.rect, 0, 255, curr_time, GameConstants.SOLVED_FADE_IN)
        elif GameConstants.SOLVED_FADE_IN < curr_time <= self.fade_out_start:
            self.fade_heart_surface(self.surface, self.rect, 255, 255, curr_time - GameConstants.SOLVED_FADE_IN,
                                    GameConstants.SOLVED_PAUSE)
        elif self.fade_out_start < curr_time <= self.fade_out_end:
            self.fade_heart_surface(self.surface, self.rect, 255, 0, curr_time - self.fade_out_start,
                                    GameConstants.SOLVED_FADE_OUT)
        elif self.fade_out_end < curr_time <= self.fade_end:
            self.fade_heart_surface(self.surface, self.rect, 0, 0, curr_time - self.fade_out_end,
                                    GameConstants.SOLVED_PAUSE)
        else:
            self.get_game().change_scene(5)
            self.begin = False

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(GameOverScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
