from __future__ import annotations

import pygame

import Game
from Game.Scenes.Scene import Scene
from Game.Shared import GameConstants


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

    def setup(self) -> None:
        super(LevelPickerScene, self).setup()
        self.centre_window_on_screen(GameConstants.WINDOW_SIZE)
        self.get_game().load_level(1)
        grid = self.get_game().get_grid()
        grid.reset()
        self.fake_screen = pygame.display.get_surface().copy()

    def draw_buttons(self) -> None:
        self.draw_button_group(['< Prev', 'Play', 'Next >'], [(0.2, 0.72), (0.5, 0.72), (0.8, 0.72)],
                               [pygame.Color('DarkGreen')] * 3, [pygame.Color('Green')] * 3)
        self.draw_button_group(['Back to Options screen'], [(0.5, 0.88)], [pygame.Color('DarkRed')],
                               [pygame.Color('Red')])

    def draw_button_group(self, text: list[str], coords: list[tuple[float, float]], colour: list[pygame.Color],
                          hover_colour: list[pygame.Color]) -> None:
        max_text = max(text, key=len)
        text_surface = self.button_font.render(max_text, True, pygame.Color('Black'))
        text_rectangle = text_surface.get_rect()
        text_rectangle = text_rectangle.inflate(text_rectangle.width * 0.25, text_rectangle.height * 0.25)
        for i, button_text in enumerate(text):
            self.button(button_text, self.button_font, pygame.Color('Black'),
                        self.width * coords[i][0] - text_rectangle.width // 2, self.height * coords[i][1],
                        text_rectangle.width, text_rectangle.height, colour[i], hover_colour[i], self.options_screen)

    def previous_level(self) -> None:
        pass

    def play_level(self) -> None:
        pass

    def next_level(self) -> None:
        pass

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
