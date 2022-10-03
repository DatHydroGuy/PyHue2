import pygame


class Slider:
    def __init__(self, size: float, x_min: int, x_max: int, y_position: int, min_value: int, max_value: int, step: int,
                 value: int) -> None:
        self.size = size
        self.x_min = x_min
        self.x_max = x_max
        self.y_position = y_position
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value
        self.dragging = False
        x_diff = x_max - x_min
        value_ratio = (value - min_value) / float(max_value - min_value)
        self.x_position = x_min + int(value_ratio * x_diff)
        self.rect = pygame.rect.Rect(self.x_position, y_position - size // 2, size, size)

    def set_value(self, new_value: int) -> None:
        x_diff = self.x_max - self.x_min
        value_ratio = (new_value - self.min_value) / float(self.max_value - self.min_value)
        self.x_position = self.x_min + int(value_ratio * x_diff)
        self.rect.left = self.x_position
        self.value = new_value

    def normalise_slider_value(self) -> int:
        pixel_range = self.x_max - self.x_min
        pixels_per_step = pixel_range / float((self.max_value - self.min_value) / self.step)
        number_of_steps = int((self.x_position - self.x_min) / pixels_per_step)

        return number_of_steps * self.step + self.min_value

    def update(self) -> None:
        self.rect.left = self.x_position
        self.value = self.normalise_slider_value()

    def draw(self, display_surface: pygame.Surface, colour: pygame.Color) -> None:
        pygame.draw.line(display_surface, colour, (self.x_min, self.y_position), (self.x_max + self.size - 1, self.y_position))
        pygame.draw.rect(display_surface, colour, self.rect)
