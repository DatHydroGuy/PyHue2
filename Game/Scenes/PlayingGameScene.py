from __future__ import annotations
import pygame

import Game
from Game.Scenes.Scene import Scene
from Game.Shared import GameConstants


class PlayingGameScene(Scene):
    def __init__(self, game: Game.PyHue2) -> None:
        super(PlayingGameScene, self).__init__(game)

    def setup(self):
        pass

    def update(self) -> None:
        super(PlayingGameScene, self).update()
        grid = self.get_game().get_grid()
        grid.update()
        if grid.is_solved():
            if grid.get_number_of_moves() == 0:
                # Reshuffle
                self.get_game().change_scene(2)
            else:
                self.get_game().set_moves(grid.get_number_of_moves())
                self.get_game().set_time(grid.get_solved_time() - self.get_game().get_paused_time())
                self.get_game().reset_paused_time()
                self.get_game().change_scene(4)

    def render(self) -> None:
        super(PlayingGameScene, self).render()
        grid = self.get_game().get_grid()
        grid.render()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(PlayingGameScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    print(self.get_game().get_grid().get_number_of_incorrect_tiles())
                else:
                    clicked_tile_x = int(event.pos[0] / GameConstants.TILE_SIZE[0])
                    clicked_tile_y = int(event.pos[1] / GameConstants.TILE_SIZE[1])
                    self.get_game().get_grid().set_current_selection((clicked_tile_x, clicked_tile_y))

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()

            # If window loses focus, store the paused time so that we can subtract it from the game time at the end.
            if event.type == pygame.ACTIVEEVENT:
                if event.state == 1:
                    if event.gain == 0:
                        self.get_game().pause_start()
                        self.get_game().change_scene(6)
                    else:
                        pass
