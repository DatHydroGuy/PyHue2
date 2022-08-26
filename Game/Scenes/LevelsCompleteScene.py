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
        self.title_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.12))
        self.basic_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.06))
        self.button_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.045))
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
        text_surface = self.button_font.render('Create New Leve', True, pygame.Color('Black'))
        text_rectangle = text_surface.get_rect()
        text_rectangle = text_rectangle.inflate(text_rectangle.width * 0.25, text_rectangle.height * 0.25)
        self.button('Play Random', self.button_font, pygame.Color('Black'),
                    self.screen_width * 0.5 - text_rectangle.width // 2, self.screen_height * 0.6,
                    text_rectangle.width, text_rectangle.height, pygame.Color('DarkGreen'),
                    pygame.Color('Green'), self.play_next)
        # TODO: make the following button point to the level editor when it's done
        self.button('Create New Level', self.button_font, pygame.Color('Black'),
                    self.screen_width * 0.5 - text_rectangle.width // 2, self.screen_height * 0.75,
                    text_rectangle.width, text_rectangle.height, pygame.Color('DarkGreen'),
                    pygame.Color('Green'), self.play_next)
        self.button('Back To Title', self.button_font, pygame.Color('Black'),
                    self.screen_width * 0.5 - text_rectangle.width // 2, self.screen_height * 0.9,
                    text_rectangle.width, text_rectangle.height, pygame.Color('DarkRed'),
                    pygame.Color('Red'), self.back_to_title)

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
