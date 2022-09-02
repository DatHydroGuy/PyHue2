from __future__ import annotations

import pygame

import Game
from Game.Scenes.Scene import Scene
from Game.Shared import GameConstants


class LevelPickerScene(Scene):
    # surface scaling source:
    # https://stackoverflow.com/questions/34910086/pygame-how-do-i-resize-a-surface-and-keep-all-objects-within-proportionate-to-t
    def __init__(self, game: Game.PyHue2) -> None:
        super(LevelPickerScene, self).__init__(game)
        self.fake_screen = pygame.display.get_surface().copy()

    def setup(self) -> None:
        super(LevelPickerScene, self).setup()
        self.centre_window_on_screen(GameConstants.WINDOW_SIZE)
        self.get_game().load_level(1)
        grid = self.get_game().get_grid()
        grid.reset()
        self.fake_screen = pygame.display.get_surface().copy()

    def update(self) -> None:
        super(LevelPickerScene, self).update()
        self.get_game().get_grid().update()

    def render(self) -> None:
        super(LevelPickerScene, self).render()
        self.get_game().get_grid().render()
        grid_surface = pygame.display.get_surface()
        self.fake_screen.fill('grey')
        self.fake_screen.blit(grid_surface, (0, 0))
        grid_surface.fill('black')
        grid_surface.blit(pygame.transform.scale(self.fake_screen, GameConstants.PREVIEW_SIZE),
                          (GameConstants.PREVIEW_X_OFFSET, GameConstants.PREVIEW_Y_OFFSET))

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(LevelPickerScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
