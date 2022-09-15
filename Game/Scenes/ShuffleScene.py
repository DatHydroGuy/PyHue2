from __future__ import annotations
import pygame

import Game
from Game.Scenes.Scene import Scene


class ShuffleScene(Scene):
    def __init__(self, game: Game.PyHue2) -> None:
        super(ShuffleScene, self).__init__(game)

    def setup(self) -> None:
        super(ShuffleScene, self).setup()
        self.get_game().get_grid().reset()
        self.centre_window_on_screen()

    def update(self) -> None:
        super(ShuffleScene, self).update()
        grid = self.get_game().get_grid()
        if grid.is_shuffled():
            self.get_game().change_scene(3)  # PlayingGameScene
        else:
            grid.update()

    def render(self) -> None:
        super(ShuffleScene, self).render()
        self.get_game().get_grid().render()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(ShuffleScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
