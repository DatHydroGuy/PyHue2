class GameObject:
    def __init__(self, grid_position: tuple[int, int], draw_position: tuple[int, int], size: tuple[int, int]) -> None:
        self.__grid_position = grid_position
        self.__draw_position = draw_position
        self.__size = size

    def set_grid_position(self, position: tuple[int, int]) -> None:
        self.__grid_position = position

    def get_grid_position(self) -> tuple[int, int]:
        return self.__grid_position

    def set_draw_position(self, position: tuple[int, int]) -> None:
        self.__draw_position = position

    def get_draw_position(self) -> tuple[int, int]:
        return self.__draw_position

    def get_size(self) -> tuple[int, int]:
        return self.__size

    def set_size(self, new_size: tuple[int, int]) -> None:
        self.__size = new_size
