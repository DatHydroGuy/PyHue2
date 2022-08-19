import pygame
import colorsys
from random import uniform


class ColourTools:
    @staticmethod
    def fill_gradient(surface, start_colour, end_colour, rect=None, vertical=True, forward=True):
        """
        Fill a surface with a gradient pattern.
        Inspired by: https://www.pygame.org/wiki/GradientCode
        :param surface: Surface to fill.
        :param start_colour: Starting colour.
        :param end_colour: Final colour.
        :param rect: Area to fill.  Default is surface's bounding rectangle.
        :param vertical: True=vertical; False=horizontal.
        :param forward:  True=forward; False=reverse.
        :return: None.
        """
        if rect is None:
            rect = surface.get_rect()

        x1, x2 = rect.left, rect.right
        y1, y2 = rect.top, rect.bottom

        if vertical:
            h = y2 - y1
        else:
            h = x2 - x1

        if forward:
            a, b = start_colour, end_colour
        else:
            b, a = start_colour, end_colour

        rate = (
            float(b[0] - a[0]) / h,
            float(b[1] - a[1]) / h,
            float(b[2] - a[2]) / h
        )

        if vertical:
            colours = ColourTools.fill_range(y1, y2, a, rate)
            for row in range(y1, y2):
                pygame.draw.line(surface, colours[row - y1], (x1, row), (x2, row))
        else:
            colours = ColourTools.fill_range(x1, x2, a, rate)
            for col in range(x1, x2):
                pygame.draw.line(surface, colours[col - x1], (col, y1), (col, y2))

    @staticmethod
    def fill_range(range_start, range_end, start_colour, colour_delta):
        colours = []
        for row in range(range_start, range_end):
            colours.append((
                min(max(start_colour[0] + (colour_delta[0] * (row - range_start)), 0), 255),
                min(max(start_colour[1] + (colour_delta[1] * (row - range_start)), 0), 255),
                min(max(start_colour[2] + (colour_delta[2] * (row - range_start)), 0), 255)
            ))
        return colours

    @staticmethod
    def fill_double_gradient(surface, start_colour, end_colour, mirror_position=0.5,
                             rect=None, vertical=True, forward=True):
        """
        Fill a surface with a gradient pattern.
        :param surface: Surface to fill.
        :param start_colour: Starting colour.
        :param end_colour: Final colour.
        :param mirror_position: Fraction of surface at which we reflect the gradient. Ranges from 0.0 to 1.0
        :param rect: Area to fill.  Default is surface's bounding rectangle.
        :param vertical: True=vertical; False=horizontal.
        :param forward:  True=forward; False=reverse.
        :return: None.
        """
        if rect is None:
            rect = surface.get_rect()

        x1, x2 = rect.left, rect.right
        y1, y2 = rect.top, rect.bottom

        if vertical:
            h = y2 - y1
            rect1 = pygame.Rect(x1, y1, x2 - x1, h * mirror_position)
            rect2 = pygame.Rect(x1, y1 + h * mirror_position, x2 - x1, h * (1 - mirror_position))
        else:
            h = x2 - x1
            rect1 = pygame.Rect(x1, y1, h * mirror_position, y2 - y1)
            rect2 = pygame.Rect(x1 + h * mirror_position, y1, h * (1 - mirror_position), y2 - y1)

        if rect1.height == 0:
            rect1 = rect1.inflate(0, 1)

        if rect2.height == 0:
            rect2 = rect2.inflate(0, 1)

        ColourTools.fill_gradient(surface, start_colour, end_colour, rect1, vertical, forward)
        ColourTools.fill_gradient(surface, start_colour, end_colour, rect2, vertical, not forward)

    @staticmethod
    def get_random_colour(pastel_factor=0.5):
        return [(x + pastel_factor) / (1.0 + pastel_factor) for x in [uniform(0, 1.0) for _ in [1, 2, 3]]]

    @staticmethod
    def colour_distance(c1, c2):
        return sum([abs(x[0] - x[1]) for x in zip(c1, c2)])

    @staticmethod
    def generate_new_colour(existing_colours, pastel_factor=0.5, colour_spread=1.0, base_offset=0.0):
        max_distance = None
        best_colour = None
        for _ in range(0, 100):
            colour = ColourTools.get_random_colour(pastel_factor=pastel_factor)
            hsv = colorsys.rgb_to_hsv(colour[0], colour[1], colour[2])
            hsv = [base_offset + hsv[0] * colour_spread, hsv[1], hsv[2]]
            colour = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
            if not existing_colours:
                return colour
            best_distance = min([ColourTools.colour_distance(colour, c) for c in existing_colours])
            if not max_distance or best_distance > max_distance:
                max_distance = best_distance
                best_colour = colour
        return best_colour

    # noinspection PyArgumentList
    @staticmethod
    def generate_colour_components(start_colour: pygame.Color, end_colour: pygame.Color, step: float):
        red = start_colour.r + int(step * (end_colour.r - start_colour.r))
        green = start_colour.g + int(step * (end_colour.g - start_colour.g))
        blue = start_colour.b + int(step * (end_colour.b - start_colour.b))
        alpha = start_colour.a + int(step * (end_colour.a - start_colour.a))
        return pygame.Color(red, green, blue, alpha)

    @staticmethod
    def blended_text(font, text, colour, background_colour):
        surface = font.render(text, True, colour, background_colour)
        surface.set_colorkey(background_colour)
        return surface
