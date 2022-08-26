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
        self.screen_size = self.fake_screen.get_size()
        self.grid_size = (GameConstants.MIN_GRID_COLUMNS * GameConstants.TILE_SIZE[0],
                          GameConstants.MIN_GRID_ROWS * GameConstants.TILE_SIZE[1])
        self.x_scale = (GameConstants.WINDOW_SIZE[0] // 2) / self.grid_size[0]
        self.y_scale = (GameConstants.WINDOW_SIZE[1] // 2) / self.grid_size[1]

    def setup(self) -> None:
        super(LevelPickerScene, self).setup()
        self.centre_window_on_screen(GameConstants.WINDOW_SIZE)
        self.get_game().load_level(1)
        grid = self.get_game().get_grid()
        grid.reset(True)
        self.fake_screen = pygame.display.get_surface().copy()
        self.grid_size = (grid.get_grid_size()[0] * GameConstants.TILE_SIZE[0],
                          grid.get_grid_size()[1] * GameConstants.TILE_SIZE[1])
        self.x_scale = (GameConstants.WINDOW_SIZE[0] // 2) / self.grid_size[0]
        self.y_scale = (GameConstants.WINDOW_SIZE[1] // 2) / self.grid_size[1]

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
        grid_surface.blit(pygame.transform.scale(self.fake_screen, (grid_surface.get_size()[0] * self.x_scale,
                                                                    grid_surface.get_size()[1] * self.y_scale)),
                          (200, 50))

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(LevelPickerScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
