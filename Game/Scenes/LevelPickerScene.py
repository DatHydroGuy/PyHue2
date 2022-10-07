from __future__ import annotations

import pygame

import Game
from Game.Scenes.Scene import Scene
from Game.Shared import GameConstants, FileTools


class LevelPickerScene(Scene):
    # surface scaling source:
    # https://stackoverflow.com/questions/34910086/pygame-how-do-i-resize-a-surface-and-keep-all-objects-within-proportionate-to-t
    def __init__(self, game: Game.PyHue2, level_num: int = 1) -> None:
        super(LevelPickerScene, self).__init__(game)
        self.fake_screen = pygame.display.get_surface().copy()
        self.width = GameConstants.WINDOW_SIZE[0]
        self.height = GameConstants.WINDOW_SIZE[1]
        min_dimension = min(self.width, self.height)
        self.button_font = self.create_font(int(min_dimension * 0.045))
        self.__level_num = level_num
        self.__file = FileTools()
        self.__max_level = -1

    def setup(self) -> None:
        super(LevelPickerScene, self).setup()
        self.centre_window_on_screen(GameConstants.WINDOW_SIZE)
        self.set_grid_for_preview()
        # self.get_game().load_level(1)
        # grid = self.get_game().get_grid()
        # grid.reset()
        # self.fake_screen = pygame.display.get_surface().copy()
        self.__max_level = self.__file.count_levels_in_file()

    def set_grid_for_preview(self):
        self.get_game().load_level(self.__level_num)
        grid = self.get_game().get_grid()
        grid.reset()
        self.fake_screen = pygame.display.get_surface().copy()

    def draw_buttons(self) -> None:
        if self.__level_num == 1:
            self.draw_button_group(self.button_font, ['Play', 'Next >'], [(0.5, 0.72), (0.8, 0.72)],
                                   [pygame.Color('DarkGreen')] * 2, [pygame.Color('Green')] * 2,
                                   [self.play_level, self.next_level])
        elif self.__level_num == self.__max_level:
            self.draw_button_group(self.button_font, ['< Prev', 'Play'], [(0.2, 0.72), (0.5, 0.72)],
                                   [pygame.Color('DarkGreen')] * 2, [pygame.Color('Green')] * 2,
                                   [self.previous_level, self.play_level])
        else:
            self.draw_button_group(self.button_font, ['< Prev', 'Play', 'Next >'],
                                   [(0.2, 0.72), (0.5, 0.72), (0.8, 0.72)], [pygame.Color('DarkGreen')] * 3,
                                   [pygame.Color('Green')] * 3, [self.previous_level, self.play_level, self.next_level])
        self.draw_button_group(self.button_font, ['Create New Level'], [(0.5, 0.81)], [pygame.Color('DarkGreen')],
                               [pygame.Color('Green')], [self.edit_level])
        self.draw_button_group(self.button_font, ['Back to Options screen'], [(0.5, 0.9)], [pygame.Color('DarkRed')],
                               [pygame.Color('Red')], [self.options_screen])

    def previous_level(self) -> None:
        if self.check_button_click() and self.__level_num > 1:
            self.__level_num -= 1
            self.set_grid_for_preview()

    def play_level(self) -> None:
        self.get_game().get_level().load_level(self.__level_num, True)
        self.get_game().shuffle_start = pygame.time.get_ticks()
        self.get_game().change_scene(2)  # ShuffleScene

    def next_level(self) -> None:
        if self.check_button_click() and self.__level_num < self.__max_level:
            self.__level_num += 1
            self.set_grid_for_preview()

    def edit_level(self):
        self.get_game().change_scene(9)  # LevelEditScene

    def options_screen(self) -> None:
        self.get_game().change_scene(1)  # OptionsScene

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
        self.draw_buttons()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(LevelPickerScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
