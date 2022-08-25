import pygame


class Slider:
    value = 0
    dragging = False

    def __init__(self, size, x_min, x_max, y_position, min_value, max_value, step, value):
        self.size = size
        self.x_min = x_min
        self.x_max = x_max
        self.y_position = y_position
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value
        x_diff = x_max - x_min
        value_ratio = (value - min_value) / float(max_value - min_value)
        self.x_position = x_min + int(value_ratio * x_diff)
        self.rect = pygame.rect.Rect(self.x_position, y_position - size // 2, size, size)

    def normalise_slider_value(self):
        pixel_range = self.x_max - self.x_min
        pixels_per_step = pixel_range / float((self.max_value - self.min_value) / self.step)
        number_of_steps = int((self.x_position - self.x_min) / pixels_per_step)

        return number_of_steps * self.step + self.min_value

    def update(self):
        self.rect.left = self.x_position
        self.value = self.normalise_slider_value()

    def draw(self, display_surface, colour):
        pygame.draw.rect(display_surface, colour, self.rect)
