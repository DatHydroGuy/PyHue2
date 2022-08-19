class GameObject:
    def __init__(self, grid_position, draw_position, size):
        self.__grid_position = grid_position
        self.__draw_position = draw_position
        self.__size = size

    def set_grid_position(self, position):
        self.__grid_position = position

    def get_grid_position(self):
        return self.__grid_position

    def set_draw_position(self, position):
        self.__draw_position = position

    def get_draw_position(self):
        return self.__draw_position

    def get_size(self):
        return self.__size

    def set_size(self, new_size):
        self.__size = new_size
