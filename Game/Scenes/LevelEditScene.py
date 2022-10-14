from __future__ import annotations

import pygame

import Game
from Game.Scenes.Scene import Scene
from Game.Shared import GameConstants, FileTools, Slider


class LevelEditScene(Scene):
    # surface scaling source:
    # https://stackoverflow.com/questions/34910086/pygame-how-do-i-resize-a-surface-and-keep-all-objects-within-proportionate-to-t
    def __init__(self, game: Game.PyHue2, level_num: int = 1) -> None:
        super(LevelEditScene, self).__init__(game)
        self.fake_screen = pygame.display.get_surface().copy()
        self.width = GameConstants.WINDOW_SIZE[0]
        self.height = GameConstants.WINDOW_SIZE[1]
        min_dimension = min(self.width, self.height)
        self.basic_font = self.create_font(int(min_dimension * 0.04))
        self.button_font = self.create_font(int(min_dimension * 0.045))
        self.__file = FileTools()
        self.__max_level = self.__file.count_levels_in_file()
        self.sliders = []
        self.slider_values = [11, 21, 0, 0, 0, GameConstants.GRID_PINS_CORNERS, 0]
        self.slider_draw = [0.81, 0.81, 0.85, 0.89, 0.93, 0.97, 0.97]
        self.slider_min = int(self.width * 0.2)
        self.slider_max = int(self.width * 0.75)
        self.slider_size = min_dimension * 0.03
        self.slider1 = Slider(self.slider_size, self.slider_min, int(self.width * 0.41),
                              self.height * self.slider_draw[0], 5, 63, 1, self.slider_values[0])
        self.slider2 = Slider(self.slider_size, int(self.width * 0.62), self.slider_max,
                              self.height * self.slider_draw[1], 5, 37, 1, self.slider_values[1])
        self.slider3 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[2], 0, 255, 1, self.slider_values[2])
        self.slider4 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[3], 0, 255, 1, self.slider_values[3])
        self.slider5 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[4], 0, 255, 1, self.slider_values[4])
        self.slider6 = Slider(self.slider_size, int(self.slider_min * 1.5), int(self.width * 0.4),
                              self.height * self.slider_draw[5],
                              GameConstants.GRID_PINS_CORNERS, GameConstants.GRID_PINS_CUSTOM,
                              1, self.slider_values[5])
        self.slider7 = Slider(self.slider_size, int(self.width * 0.7), self.slider_max,
                              self.height * self.slider_draw[6], 0, 3, 1, self.slider_values[6])
        self.sliders.append(self.slider1)
        self.sliders.append(self.slider2)
        self.sliders.append(self.slider3)
        self.sliders.append(self.slider4)
        self.sliders.append(self.slider5)
        self.sliders.append(self.slider6)
        self.sliders.append(self.slider7)
        self.offset_x = 0
        self.top_left_colour = [255, 0, 0]
        self.top_right_colour = [0, 0, 255]
        self.bottom_left_colour = [255, 255, 0]
        self.bottom_right_colour = [0, 255, 0]
        self.old_corner = -1
        self.display_surface = pygame.display.get_surface()
        self.changed = False
        self.saved = False

    def setup(self) -> None:
        super(LevelEditScene, self).setup()
        self.centre_window_on_screen(GameConstants.WINDOW_SIZE)
        self.set_grid_for_preview()
        # self.get_game().load_level(1)
        # grid = self.get_game().get_grid()
        # grid.reset()
        # self.fake_screen = pygame.display.get_surface().copy()
        self.__max_level = self.__file.count_levels_in_file()
        self.changed = False
        self.saved = False

    def set_grid_for_preview(self):
        self.get_game().edit_level(self.slider1.value, self.slider2.value, self.slider6.value,
                                   [self.top_left_colour, self.top_right_colour,
                                    self.bottom_left_colour, self.bottom_right_colour])
        grid = self.get_game().get_grid()
        grid.reset()
        self.fake_screen = pygame.display.get_surface().copy()

    def draw_buttons(self) -> None:
        self.draw_button_group(self.button_font, ['Try', 'Save', 'Options'],
                               [(0.9, 0.80), (0.9, 0.86), (0.9, 0.92)],
                               [pygame.Color('DarkGreen')] * 2 + [pygame.Color('DarkRed')],
                               [pygame.Color('Green')] * 2 + [pygame.Color('Red')],
                               [self.try_level, self.save_level, self.options_screen])

    def draw_sliders(self) -> None:
        corners = ["Top Left", "Top Right", "Bottom Left", "Bottom Right"]
        pin_layouts = ["Corners", "Vert Edges", "Horiz Edges", "Border", "Alternating", "Diagonal", "Rnd Diagonal",
                       "Knights Tour", "Random", "Rnd Choice", "Custom"]
        align_x = self.width * 0.15
        self.draw_right_aligned_text(self.basic_font, 'Width: ', pygame.Color('White'),
                                     align_x, self.height * self.slider_draw[0])
        self.draw_right_aligned_text(self.basic_font, 'Height: ', pygame.Color('White'),
                                     self.width * 0.58, self.height * self.slider_draw[1])
        self.draw_right_aligned_text(self.basic_font, 'Red: ', pygame.Color('White'),
                                     align_x, self.height * self.slider_draw[2])
        self.draw_right_aligned_text(self.basic_font, 'Green: ', pygame.Color('White'),
                                     align_x, self.height * self.slider_draw[3])
        self.draw_right_aligned_text(self.basic_font, 'Blue: ', pygame.Color('White'),
                                     align_x, self.height * self.slider_draw[4])
        self.draw_right_aligned_text(self.basic_font, 'Pins: ', pygame.Color('White'),
                                     align_x, self.height * self.slider_draw[5])
        self.draw_right_aligned_text(self.basic_font, 'Corner: ', pygame.Color('White'),
                                     self.width * 0.55, self.height * self.slider_draw[6])
        self.draw_left_aligned_text(self.basic_font, '{0}'.format(self.slider1.value), pygame.Color('White'),
                                    align_x, self.height * self.slider_draw[0])
        self.draw_left_aligned_text(self.basic_font, '{0}'.format(self.slider2.value), pygame.Color('White'),
                                    self.width * 0.58, self.height * self.slider_draw[1])
        self.draw_left_aligned_text(self.basic_font, '{0}'.format(self.slider3.value), pygame.Color('White'),
                                    align_x, self.height * self.slider_draw[2])
        self.draw_left_aligned_text(self.basic_font, '{0}'.format(self.slider4.value), pygame.Color('White'),
                                    align_x, self.height * self.slider_draw[3])
        self.draw_left_aligned_text(self.basic_font, '{0}'.format(self.slider5.value), pygame.Color('White'),
                                    align_x, self.height * self.slider_draw[4])
        self.draw_left_aligned_text(self.basic_font, pin_layouts[self.slider6.value], pygame.Color('White'),
                                    align_x, self.height * self.slider_draw[5])
        self.draw_left_aligned_text(self.basic_font, corners[self.slider7.value], pygame.Color('White'),
                                    self.width * 0.55, self.height * self.slider_draw[6])
        for slider in self.sliders:
            slider.draw(self.display_surface, pygame.Color('White'))

    def try_level(self) -> None:
        corner_colours = [self.top_left_colour, self.top_right_colour, self.bottom_left_colour,
                          self.bottom_right_colour]
        self.get_game().try_level(self.slider1.value, self.slider2.value, self.slider6.value,
                                  corner_colours)
        self.get_game().shuffle_start = pygame.time.get_ticks()
        self.get_game().change_scene(2)  # ShuffleScene

    def save_level(self) -> None:
        if self.changed and not self.saved:
            file_tools = FileTools()
            corner_colours = [self.top_left_colour, self.top_right_colour, self.bottom_left_colour,
                              self.bottom_right_colour]
            file_tools.save_level(self.sliders, corner_colours, self.get_game().get_grid().get_cell_pins())
            self.saved = True

    def options_screen(self) -> None:
        self.get_game().change_scene(1)  # OptionsScene

    def calculate_clicked_preview_cell(self, event_pos):
        # Calculate which cell was clicked (the preview thinks it is drawn at WINDOW_SIZE, so scale values)
        preview_cell_size = self.get_game().get_grid().scaled_tile_size
        scaled_tile_x = GameConstants.WINDOW_SIZE[0] / GameConstants.TILE_SIZE[0]
        scaled_tile_y = GameConstants.WINDOW_SIZE[1] / GameConstants.TILE_SIZE[1]
        border_is_left_and_right = abs(preview_cell_size[0] * 0.75 - scaled_tile_x) > abs(
            preview_cell_size[1] * 0.75 - scaled_tile_y)
        if border_is_left_and_right:
            y_offset = 0
            x_offset = (GameConstants.WINDOW_SIZE[0] - (preview_cell_size[0] * self.slider1.value)) * 0.375
        else:
            x_offset = 0
            y_offset = (GameConstants.WINDOW_SIZE[1] - (preview_cell_size[1] * self.slider2.value)) * 0.375
        x_offset = int(x_offset) + GameConstants.PREVIEW_X_OFFSET
        y_offset = int(y_offset) + GameConstants.PREVIEW_Y_OFFSET // 5
        preview_cell_size = (int(preview_cell_size[0] * 0.75), int(preview_cell_size[1] * 0.75))
        clicked_tile_x = (event_pos[0] - x_offset) // preview_cell_size[0]
        clicked_tile_y = (event_pos[1] - y_offset) // preview_cell_size[1]
        return clicked_tile_x, clicked_tile_y

    def update(self) -> None:
        super(LevelEditScene, self).update()

        if self.slider7.value != self.old_corner:
            if self.slider7.value == 0:
                colour = self.top_left_colour
            elif self.slider7.value == 1:
                colour = self.top_right_colour
            elif self.slider7.value == 2:
                colour = self.bottom_left_colour
            else:
                colour = self.bottom_right_colour
            self.slider3.set_value(colour[0])
            self.slider4.set_value(colour[1])
            self.slider5.set_value(colour[2])
            self.old_corner = self.slider7.value
        else:
            colour = [self.slider3.value, self.slider4.value, self.slider5.value]
            if self.slider7.value == 0:
                self.top_left_colour = colour
            elif self.slider7.value == 1:
                self.top_right_colour = colour
            elif self.slider7.value == 2:
                self.bottom_left_colour = colour
            else:
                self.bottom_right_colour = colour

        self.set_grid_for_preview()
        self.get_game().get_grid().update()

    def render(self) -> None:
        super(LevelEditScene, self).render()
        self.get_game().get_grid().render()
        grid_surface = pygame.display.get_surface()
        self.fake_screen.fill('grey')
        self.fake_screen.blit(grid_surface, (0, 0))
        grid_surface.fill('black')
        grid_surface.blit(pygame.transform.scale(self.fake_screen, GameConstants.PREVIEW_SIZE),
                          (GameConstants.PREVIEW_X_OFFSET, GameConstants.PREVIEW_Y_OFFSET // 5))
        self.draw_buttons()
        self.draw_sliders()

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        super(LevelEditScene, self).handle_events(events)

        for event in events:
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_tile_x, clicked_tile_y = self.calculate_clicked_preview_cell(event.pos)
                    # If click is outside the grid, ignore. Otherwise toggle pin and set pins to CUSTOM
                    if 0 <= clicked_tile_x < self.slider1.value and 0 <= clicked_tile_y < self.slider2.value:
                        self.get_game().get_grid().toggle_cell_pin(clicked_tile_x, clicked_tile_y)
                        if self.slider6.value != GameConstants.GRID_PINS_CUSTOM:
                            # TODO Save list of pinned cells here
                            self.slider6.set_value(GameConstants.GRID_PINS_CUSTOM)
                        else:
                            # TODO Save list of pinned cells here
                            pass

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
                        self.changed = True
                        self.saved = False
                        mouse_x, mouse_y = event.pos
                        self.sliders[i].x_position = max(min(mouse_x + self.offset_x, draggable.x_max), draggable.x_min)
                        self.sliders[i].update()
                        self.slider_values[i] = self.sliders[i].value

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    exit()
