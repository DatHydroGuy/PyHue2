from __future__ import annotations
from math import sin
from typing import Callable

import pygame

import Game
from Game.Scenes.Scene import Scene
from ..Shared import GameConstants, Slider, ColourTools


class OptionsScene(Scene):
    def __init__(self, game: Game.PyHue2) -> None:
        super(OptionsScene, self).__init__(game)
        self.sliders = []
        self.slider_values = [5, 5, 0, 100, GameConstants.GRID_PINS_RANDOMISED]
        self.slider_draw = [0.3, 0.4, 0.5, 0.6, 0.75]
        self.width = GameConstants.SCREEN_SIZE[0]
        self.height = GameConstants.SCREEN_SIZE[1]
        self.zero_to_one = 0
        self.colour1 = None
        self.colour2 = None

        self.display_surface = pygame.display.get_surface()
        min_dimension = min(self.width, self.height)
        self.basic_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.08))
        self.button_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.045))
        self.score_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.04))
        self.title_font = pygame.font.Font('freesansbold.ttf', int(min_dimension * 0.18))

        self.slider_min = int(self.width * 0.45)
        self.slider_max = int(self.width * 0.9)
        self.slider_size = min_dimension * 0.08
        self.slider1 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[0], 5, 63, 1, self.slider_values[0])
        self.slider2 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[1], 5, 37, 1, self.slider_values[1])
        self.slider3 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[2], 0, 100, 1, self.slider_values[2])
        self.slider4 = Slider(self.slider_size, self.slider_min, self.slider_max,
                              self.height * self.slider_draw[3], 10, 100, 1, self.slider_values[3])
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

    def button(self, button_text: str, font: pygame.font, colour: pygame.Color, top_left_x: int, top_left_y: int,
               width: int, height: int, inactive_colour: pygame.Color, active_colour: pygame.Color,
               callback: Callable[[], None] = None) -> None:
        # Taken from https://pythonprogramming.net/pygame-button-function-events/?completed=/pygame-button-function/
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if top_left_x + width > mouse[0] > top_left_x and top_left_y + height > mouse[1] > top_left_y:
            pygame.draw.rect(self.display_surface, active_colour, (top_left_x, top_left_y, width, height))

            if click[0] == 1 and callback is not None:
                callback()
        else:
            pygame.draw.rect(self.display_surface, inactive_colour, (top_left_x, top_left_y, width, height))

        text_surface = font.render(button_text, True, colour)
        text_rectangle = text_surface.get_rect()
        text_rectangle.center = ((top_left_x + (width / 2)), (top_left_y + (height / 2)))
        self.display_surface.blit(text_surface, text_rectangle)

    def back_to_title(self) -> None:
        self.get_game().change_scene(0)

    def play_random(self) -> None:
        self.get_game().num_tiles_horizontally = self.slider1.value
        self.get_game().num_tiles_vertically = self.slider2.value
        self.get_game().set_level(self.slider1.value, self.slider2.value,
                                  self.slider3.value / 100, self.slider4.value / 100, self.slider5.value)
        self.get_game().load_level(0)
        self.get_game().shuffle_start = pygame.time.get_ticks()
        self.get_game().change_scene(2)

    def play_levels(self) -> None:
        self.get_game().load_level(1)
        self.get_game().shuffle_start = pygame.time.get_ticks()
        self.get_game().change_scene(2)

    def draw_buttons(self) -> None:
        text_surface = self.button_font.render('Play XXXXX', True, pygame.Color('Black'))
        text_rectangle = text_surface.get_rect()
        text_rectangle = text_rectangle.inflate(text_rectangle.width * 0.25, text_rectangle.height * 0.25)
        self.button('Back', self.button_font, pygame.Color('Black'),
                    self.width * 0.2 - text_rectangle.width // 2, self.height * 0.88,
                    text_rectangle.width, text_rectangle.height, pygame.Color('DarkRed'),
                    pygame.Color('Red'), self.back_to_title)
        self.button('Play Levels', self.button_font, pygame.Color('Black'),
                    self.width * 0.5 - text_rectangle.width // 2, self.height * 0.88,
                    text_rectangle.width, text_rectangle.height, pygame.Color('DarkGreen'),
                    pygame.Color('Green'), self.play_levels)
        self.button('Play Random', self.button_font, pygame.Color('Black'),
                    self.width * 0.8 - text_rectangle.width // 2, self.height * 0.88,
                    text_rectangle.width, text_rectangle.height, pygame.Color('DarkGreen'),
                    pygame.Color('Green'), self.play_random)

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
        self.slider1.draw(self.display_surface, pygame.Color('White'))
        self.slider2.draw(self.display_surface, pygame.Color('White'))
        self.slider3.draw(self.display_surface, pygame.Color('White'))
        self.slider4.draw(self.display_surface, pygame.Color('White'))
        self.slider5.draw(self.display_surface, pygame.Color('White'))

    def update(self, start_time: int = 0) -> None:
        elapsed = (pygame.time.get_ticks() - start_time) / 1500.0
        self.zero_to_one = ((sin(elapsed) * 0.99) + 1.0) * 0.5

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
