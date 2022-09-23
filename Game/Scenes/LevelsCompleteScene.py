from __future__ import annotations

import pygame

import Game
from Game.Scenes.Scene import Scene
from Game.Shared import GameConstants


class LevelsCompleteScene(Scene):
    def __init__(self, game: Game.PyHue2) -> None:
        super(LevelsCompleteScene, self).__init__(game)
        self.screen_width = GameConstants.WINDOW_SIZE[0]
        self.screen_height = GameConstants.WINDOW_SIZE[1]
        min_dimension = min(GameConstants.WINDOW_SIZE[0], GameConstants.WINDOW_SIZE[1])
        self.title_font = self.create_font(int(min_dimension * 0.12))
        self.basic_font = self.create_font(int(min_dimension * 0.06))
        self.button_font = self.create_font(int(min_dimension * 0.045))
        self.__centred = False

    def setup(self) -> None:
        super(LevelsCompleteScene, self).setup()
        self.__centred = False
        self.centre_window_on_screen(GameConstants.WINDOW_SIZE)

    def draw_scores(self) -> None:
        self.draw_screen_centered_text('Congratulations!', self.title_font, pygame.Color('White'),
                                       self.screen_height * 0.05)
        self.draw_screen_centered_text(f'You have completed all the levels!', self.basic_font,
                                       pygame.Color('White'), self.screen_height * 0.25)
        self.draw_screen_centered_text(f'Please choose one of the following options:', self.basic_font,
                                       pygame.Color('White'), self.screen_height * 0.37)

    def draw_buttons(self) -> None:
        # TODO: make the middle button point to the level editor when it's done
        self.draw_button_group(self.button_font, ['Play Random', 'Create New Level', 'Back To Title'],
                               [(0.5, 0.6), (0.5, 0.75), (0.5, 0.9)],
                               [pygame.Color('DarkGreen'), pygame.Color('DarkGreen'), pygame.Color('DarkRed')],
                               [pygame.Color('Green'), pygame.Color('Green'), pygame.Color('Red')],
                               [self.play_next, self.play_next, self.back_to_title])

    def back_to_title(self) -> None:
        self.get_game().change_scene(0)  # TitleScene

    def play_next(self) -> None:
        self.get_game().change_scene(1)  # OptionsScene

    def update(self) -> None:
        super(LevelsCompleteScene, self).update()
        if not self.__centred:
            self.centre_window_on_screen(GameConstants.WINDOW_SIZE)
            self.__centred = True

    def render(self) -> None:
        super(LevelsCompleteScene, self).render()
        if self.__centred:
            self.draw_scores()
            self.draw_buttons()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(LevelsCompleteScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
