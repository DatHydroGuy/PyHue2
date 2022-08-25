from __future__ import annotations

import pygame

import Game
from Game.Scenes.Scene import Scene
from Game.Shared import GameConstants, FileTools


class HighScoreScene(Scene):
    def __init__(self, game: Game.PyHue2) -> None:
        super(HighScoreScene, self).__init__(game)
        self.grid_width = self.get_game().get_grid().get_grid_size()[0]
        self.grid_height = self.get_game().get_grid().get_grid_size()[1]
        self.screen_width = GameConstants.SCREEN_SIZE[0]
        self.screen_height = GameConstants.SCREEN_SIZE[1]
        min_dimension = min(GameConstants.SCREEN_SIZE[0], GameConstants.SCREEN_SIZE[1])
        self.title_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.12))
        self.basic_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.06))
        self.button_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.045))
        self.score_file = FileTools()
        self.__centred = False
        self.__moves = 99999999
        self.__time = 99999999
        self.__scores = None
        self.__pastel = None
        self.__spread = None
        self.__pins = None
        self.__level = None
        self.__pin_text = ["Corners", "Vert Edges", "Horiz Edges", "Border", "Alternating", "Diagonal", "Rnd Diagonal",
                           "Knights Tour", "Random", "Rnd Choice"]

    def setup(self) -> None:
        super(HighScoreScene, self).setup()
        self.__centred = False
        self.__level = self.get_game().get_level()
        self.__moves = self.get_game().get_moves()
        self.__time = self.get_game().get_time() / 1000
        self.__pastel = int(self.__level.get_pastel() * 100)
        self.__spread = int(self.__level.get_spread() * 100)
        self.__pins = self.__level.get_pins()
        self.grid_width = self.get_game().get_grid().get_grid_size()[0]
        self.grid_height = self.get_game().get_grid().get_grid_size()[1]
        self.centre_window_on_screen(GameConstants.SCREEN_SIZE)

    def draw_scores(self) -> None:
        self.draw_screen_centered_text('High Scores', self.title_font, pygame.Color('White'), self.screen_height * 0.05)
        if str(self.__level) == '0':
            self.draw_screen_centered_text(f'Width:{self.grid_width}, Height:{self.grid_height}', self.basic_font,
                                           pygame.Color('Grey'), self.screen_height * 0.20)
            self.draw_screen_centered_text(f'Pastel:{int(100 * self.__pastel)}%, Spread:{self.__spread}%,'
                                           f' Pins:{self.__pin_text[self.__pins]}', self.basic_font,
                                           pygame.Color('Grey'), self.screen_height * 0.28)
        else:
            self.draw_screen_centered_text(f'Level:{self.__level}', self.basic_font,
                                           pygame.Color('White'), self.screen_height * 0.25)
        self.draw_screen_centered_text(f'Your moves: {self.__moves}', self.basic_font, pygame.Color('White'),
                                       self.screen_height * 0.42)
        self.draw_screen_centered_text(f'Your time: {self.__time} seconds', self.basic_font,
                                       pygame.Color('White'), self.screen_height * 0.50)
        self.draw_screen_centered_text(f'Previous attempts: {self.__scores[0]}', self.basic_font,
                                       pygame.Color('Grey'), self.screen_height * 0.62)
        self.draw_screen_centered_text(f'Average moves: {self.__scores[1]:.0f}', self.basic_font,
                                       pygame.Color('Grey'), self.screen_height * 0.70)
        self.draw_screen_centered_text(f'Average time: {self.__scores[2]:.3f} seconds', self.basic_font,
                                       pygame.Color('Grey'), self.screen_height * 0.78)

    def draw_buttons(self) -> None:
        text_surface = self.button_font.render('Play XXXXXXXX', True, pygame.Color('Black'))
        text_rectangle = text_surface.get_rect()
        text_rectangle = text_rectangle.inflate(text_rectangle.width * 0.25, text_rectangle.height * 0.25)
        button_text = 'Play Random' if str(self.__level) == '0' else 'Next Level'
        self.button(button_text, self.button_font, pygame.Color('Black'),
                    self.screen_width * 0.25 - text_rectangle.width // 2, self.screen_height * 0.92,
                    text_rectangle.width, text_rectangle.height, pygame.Color('DarkGreen'),
                    pygame.Color('Green'), self.play_next)
        self.button('Back To Title', self.button_font, pygame.Color('Black'),
                    self.screen_width * 0.75 - text_rectangle.width // 2, self.screen_height * 0.92,
                    text_rectangle.width, text_rectangle.height, pygame.Color('DarkRed'),
                    pygame.Color('Red'), self.back_to_title)

    def back_to_title(self) -> None:
        self.save_score()
        self.get_game().change_scene(0)

    def play_next(self) -> None:
        self.save_score()
        if str(self.__level) == '0':
            self.get_game().change_scene(1)
        else:
            if self.__level.load_next_level():
                self.get_game().shuffle_start = pygame.time.get_ticks()
                self.get_game().change_scene(2)
            else:
                self.get_game().change_scene(7)

    def save_score(self) -> None:
        self.score_file.save_high_scores(self.__level, self.grid_width, self.grid_height,
                                         self.__pastel, self.__spread, self.__pins, self.__moves, self.__time)

    def update(self) -> None:
        super(HighScoreScene, self).update()
        if not self.__centred:
            self.centre_window_on_screen(GameConstants.SCREEN_SIZE)
            saved_scores = self.score_file.get_high_scores(self.__level, self.grid_width,
                                                           self.grid_height, self.__pastel, self.__spread, self.__pins)
            self.__scores = saved_scores[str(self.__level)][str(self.grid_width)][str(
                self.grid_height)][str(self.__pastel)][str(self.__spread)][str(self.__pins)]
            self.__centred = True

    def render(self) -> None:
        super(HighScoreScene, self).render()
        if self.__centred:
            self.draw_scores()
            self.draw_buttons()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(HighScoreScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                self.save_score()
                exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.save_score()
                    exit()
