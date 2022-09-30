from __future__ import annotations

import pygame

import Game
from Game.Scenes.Scene import Scene
from ..Shared import GameConstants, Slider, ColourTools


class OptionsScene(Scene):
    def __init__(self, game: Game.PyHue2) -> None:
        super(OptionsScene, self).__init__(game)
        self.sliders = []
        self.slider_values = [GameConstants.DEFAULT_WIDTH, GameConstants.DEFAULT_HEIGHT, GameConstants.DEFAULT_PASTEL,
                              GameConstants.DEFAULT_SPREAD, GameConstants.GRID_PINS_RANDOMISED]
        self.slider_draw = [0.3, 0.4, 0.5, 0.6, 0.75]
        self.width = GameConstants.WINDOW_SIZE[0]
        self.height = GameConstants.WINDOW_SIZE[1]
        self.zero_to_one = 0
        self.colour1 = None
        self.colour2 = None

        self.display_surface = pygame.display.get_surface()
        min_dimension = min(self.width, self.height)
        self.basic_font = self.create_font(int(min_dimension * 0.08))
        self.button_font = self.create_font(int(min_dimension * 0.045))
        self.score_font = self.create_font(int(min_dimension * 0.04))
        self.title_font = self.create_font(int(min_dimension * 0.18))

        self.slider_min = int(self.width * 0.45)
        self.slider_max = int(self.width * 0.9)
        self.slider_size = min_dimension * 0.08
        self.slider1 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[0], GameConstants.MIN_GRID_COLUMNS,
                              GameConstants.MAX_GRID_COLUMNS, 1, self.slider_values[0])
        self.slider2 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[1], GameConstants.MIN_GRID_ROWS,
                              GameConstants.MAX_GRID_ROWS, 1, self.slider_values[1])
        self.slider3 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[2], GameConstants.MIN_PASTEL, GameConstants.MAX_PASTEL, 1,
                              self.slider_values[2])
        self.slider4 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[3], GameConstants.MIN_SPREAD, GameConstants.MAX_SPREAD, 1,
                              self.slider_values[3])
        self.slider5 = Slider(self.slider_size, int(self.slider_min * 1.5), self.slider_max,
                              self.height * self.slider_draw[4],
                              GameConstants.GRID_PINS_CORNERS, GameConstants.GRID_PINS_RANDOMISED,
                              1, self.slider_values[4])
        self.sliders.append(self.slider1)
        self.sliders.append(self.slider2)
        self.sliders.append(self.slider3)
        self.sliders.append(self.slider4)
        self.sliders.append(self.slider5)
        self.offset_x = 0

    def setup(self) -> None:
        self.colour1 = self.get_game().colour1
        self.colour2 = self.get_game().colour2

    def back_to_title(self) -> None:
        self.get_game().change_scene(0)  # TitleScene

    def play_random(self) -> None:
        self.get_game().num_tiles_horizontally = self.slider1.value
        self.get_game().num_tiles_vertically = self.slider2.value
        self.get_game().set_level(self.slider1.value, self.slider2.value,
                                  self.slider3.value / 100, self.slider4.value / 100, self.slider5.value)
        self.get_game().load_level(0)
        self.get_game().shuffle_start = pygame.time.get_ticks()
        self.get_game().change_scene(2)  # ShuffleScene

    def play_levels(self) -> None:
        # TODO: Take user to the level picker scene
        self.get_game().change_scene(8)  # LevelPickerScene

    def edit_level(self) -> None:
        self.get_game().change_scene(9)  # LevelEditScene

    def draw_buttons(self) -> None:
        self.draw_button_group(self.button_font, ['Back', 'Play Levels', 'Play Random'],
                               [(0.2, 0.88), (0.5, 0.88), (0.8, 0.88)],
                               [pygame.Color('DarkRed'), pygame.Color('DarkGreen'), pygame.Color('DarkGreen')],
                               [pygame.Color('Red'), pygame.Color('Green'), pygame.Color('Green')],
                               [self.back_to_title, self.play_levels, self.play_random])
        # Test Level Edit Scene
        self.draw_button_group(self.button_font, ['E'], [(0.95, 0.88)], [pygame.Color('DarkGreen')],
                               [pygame.Color('Green')], [self.edit_level])

    def draw_sliders(self) -> None:
        pin_layouts = ["Corners", "Vert Edges", "Horiz Edges", "Border", "Alternating", "Diagonal", "Rnd Diagonal",
                       "Knights Tour", "Random", "Rnd Choice"]
        self.draw_right_aligned_text(self.basic_font, 'Width: ', pygame.Color('White'),
                                     self.width * 0.31, self.height * self.slider_draw[0])
        self.draw_right_aligned_text(self.basic_font, 'Height: ', pygame.Color('White'),
                                     self.width * 0.31, self.height * self.slider_draw[1])
        self.draw_right_aligned_text(self.basic_font, 'Pastel: ', pygame.Color('White'),
                                     self.width * 0.31, self.height * self.slider_draw[2])
        self.draw_right_aligned_text(self.basic_font, 'Spread: ', pygame.Color('White'),
                                     self.width * 0.31, self.height * self.slider_draw[3])
        self.draw_right_aligned_text(self.basic_font, 'Pins: ', pygame.Color('White'),
                                     self.width * 0.31, self.height * self.slider_draw[4])
        self.draw_left_aligned_text(self.basic_font, '{0}'.format(self.slider1.value), pygame.Color('White'),
                                    self.width * 0.31, self.height * self.slider_draw[0])
        self.draw_left_aligned_text(self.basic_font, '{0}'.format(self.slider2.value), pygame.Color('White'),
                                    self.width * 0.31, self.height * self.slider_draw[1])
        self.draw_left_aligned_text(self.basic_font, '{0}'.format(self.slider3.value), pygame.Color('White'),
                                    self.width * 0.31, self.height * self.slider_draw[2])
        self.draw_left_aligned_text(self.basic_font, '{0}'.format(self.slider4.value), pygame.Color('White'),
                                    self.width * 0.31, self.height * self.slider_draw[3])
        self.draw_left_aligned_text(self.basic_font, pin_layouts[self.slider5.value], pygame.Color('White'),
                                    self.width * 0.31, self.height * self.slider_draw[4])
        for slider in self.sliders:
            slider.draw(self.display_surface, pygame.Color('White'))

    def update(self, start_time: int = 0) -> None:
        self.zero_to_one = self.update_colours(1500.0, start_time)

    def render(self) -> None:
        # Draw TODO re-add following line
        ColourTools.fill_double_gradient(pygame.display.get_surface(), self.colour1, self.colour2, self.zero_to_one)
        self.draw_screen_centered_text("Options", self.title_font, pygame.Color('White'), 5)
        self.draw_sliders()
        self.draw_buttons()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(OptionsScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i, draggable in enumerate(self.sliders):
                        if draggable.rect.collidepoint(event.pos):
                            draggable.dragging = True
                            mouse_x, mouse_y = event.pos
                            self.offset_x = draggable.x_position - mouse_x

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for draggable in self.sliders:
                        draggable.dragging = False

            elif event.type == pygame.MOUSEMOTION:
                for i, draggable in enumerate(self.sliders):
                    if draggable.dragging:
                        mouse_x, mouse_y = event.pos
                        self.sliders[i].x_position = max(min(mouse_x + self.offset_x, draggable.x_max), draggable.x_min)
                        self.sliders[i].update()
                        self.slider_values[i] = self.sliders[i].value

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
