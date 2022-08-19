from math import pi, atan2
from random import choice


class TransitionCreator:
    def __init__(self, global_start, global_fade_out, global_pause, global_fade_in, local_fade_out, local_fade_in):
        self.global_start = global_start
        self.global_fade_in = global_fade_in
        self.global_pause = global_pause
        self.global_fade_out = global_fade_out
        self.local_fade_in = local_fade_in
        self.local_fade_out = local_fade_out

    def __convert_matrix_values_to_ticks(self, matrix, number_of_bands, as_timings):
        if as_timings is True:
            tile_delta1 = int((self.global_fade_in - self.local_fade_in) / (number_of_bands - 1))
            tile_delta2 = int((self.global_fade_out - self.local_fade_out) / (number_of_bands - 1))
            final_transition_start = self.global_start + self.global_fade_in + self.global_pause

            for row in range(len(matrix)):
                for column in range(len(matrix[0])):
                    local_start = self.global_start + matrix[row][column] * tile_delta1
                    local_start2 = final_transition_start + matrix[row][column] * tile_delta2
                    matrix[row][column] = (local_start,
                                           local_start + self.local_fade_in,
                                           local_start2,
                                           local_start2 + self.local_fade_out)

    @staticmethod
    def __reverse_matrix_values(m, number_of_bands, reverse):
        if reverse is True:
            for row in range(len(m)):
                for column in range(len(m[0])):
                    m[row][column] = number_of_bands - m[row][column] - 1

    @staticmethod
    def __mirror_matrix(m, mirrored):
        if mirrored is True:
            m = [list(reversed(row)) for row in m]
        return m

    @staticmethod
    def __rad_to_deg(x):
        return x * 180.0 / pi

    @staticmethod
    def __spiral_matrix_core(width, height, double_spiral=False):
        matrix = [[0] * width for _ in range(height)]
        row_delta, column_delta = [0, 1, 0, -1], [1, 0, -1, 0]
        row, column, counter = 0, -1, 0
        min_dimension = min(width, height)
        number_of_edges = min_dimension + min_dimension
        if width >= height:
            number_of_edges -= 1

        for edge_number in range(number_of_edges):
            if double_spiral is True:
                if edge_number % 2 == 0:
                    current_edge_count = width - edge_number
                else:
                    current_edge_count = height - edge_number - 1
            else:
                if edge_number % 2 == 0:
                    current_edge_count = (width + width - edge_number) // 2
                else:
                    current_edge_count = (height + height - edge_number) // 2

            for _ in range(current_edge_count):
                row += row_delta[edge_number % 4]
                column += column_delta[edge_number % 4]
                if matrix[row][column] == 0:
                    matrix[row][column] = counter
                    if double_spiral is True:
                        matrix[height - row - 1][width - column - 1] = counter
                    counter += 1

        return matrix

    @staticmethod
    def __multi_spiral_matrix_core(width, height):
        matrix = [[0] * width for _ in range(height)]
        sub_matrix_width = width // 2 + 1
        sub_matrix_height = height // 2 + 1
        sub_matrix = TransitionCreator.__spiral_matrix_core(sub_matrix_width, sub_matrix_height, False)
        for row in range(sub_matrix_height):
            for column in range(sub_matrix_width):
                matrix[row][column] = sub_matrix[row][column]
                matrix[row][column + sub_matrix_width - 1] = [item[::-1] for item in sub_matrix][row][column]
                matrix[row + sub_matrix_height - 1][column] = sub_matrix[::-1][row][column]
                matrix[row + sub_matrix_height - 1][column + sub_matrix_width - 1] = \
                    [item[::-1] for item in sub_matrix[::-1]][row][column]

        return matrix

    @staticmethod
    def __diagonal_matrix_core(width, height, number_of_bands):
        matrix = [[0] * width for _ in range(height)]
        for counter in range(number_of_bands):
            for row in range(height):
                for column in range(width):
                    if row + column == counter:
                        matrix[row][column] = counter

        return matrix

    @staticmethod
    def __double_diagonal_matrix_core(width, height, number_of_bands):
        matrix = TransitionCreator.__diagonal_matrix_core(width, height, width + height - 1)
        for row in range(height):
            for column in range(width):
                matrix[row][column] = matrix[row][column] // 2 if matrix[row][column] % 2 == 0 else \
                    number_of_bands - 1 - matrix[row][column] // 2

        return matrix

    @staticmethod
    def __circle_matrix_core(width, height, number_of_bands):
        matrix = [[0] * width for _ in range(height)]
        for counter in range(number_of_bands):
            for row in range(counter, height - counter):
                for column in range(counter, width - counter):
                    matrix[row][column] = counter

        return matrix

    @staticmethod
    def __vertical_swipes_matrix_core(width, height):
        matrix = [[0] * width for _ in range(height)]
        counter = 0
        for column in range(width // 2):
            for row in range(height):
                if column % 2 == 0:
                    matrix[row][column] = counter
                    matrix[height - row - 1][width - column - 1] = counter
                else:
                    matrix[row][width - column - 1] = counter
                    matrix[height - row - 1][column] = counter
                counter += 1

        column = width // 2
        if width % 2 == 1:
            max_height = (height + 1) // 2

            for row in range(max_height):
                matrix[row][column] = counter
                matrix[height - row - 1][column] = counter
                counter += 1

        return matrix

    @staticmethod
    def __horizontal_swipes_matrix_core(width, height):
        matrix = [[0] * width for _ in range(height)]
        counter = 0
        for row in range(height // 2):
            for column in range(width):
                if row % 2 == 0:
                    matrix[row][column] = counter
                else:
                    matrix[row][width - column - 1] = counter
                counter += 1
            matrix[height - row - 1] = matrix[row][::-1]

        row = height // 2
        if height % 2 == 1:
            max_width = (width + 1) // 2

            for column in range(max_width):
                matrix[row][column] = counter
                matrix[row][width - column - 1] = counter
                counter += 1

        return matrix

    def __clock_matrix_core(self, width, height, number_of_segments=1, cell_width=30, cell_height=30):
        matrix = [[0] * width for _ in range(height)]
        matrix_width = width * cell_width
        matrix_height = height * cell_height
        matrix_center = (matrix_width / 2.0, matrix_height / 2.0)
        for row in range(height):
            for column in range(width):
                matrix[row][column] = (450 + self.__rad_to_deg(
                    atan2(cell_height * row + (cell_height / 2.0) - matrix_center[1],
                          cell_width * column + (cell_width / 2.0) - matrix_center[0]))) % 360

        max_angle = (359 // number_of_segments) + 1
        counter = 0
        for angle in range(max_angle):
            for segment in range(number_of_segments):
                min_angle = angle + segment * max_angle
                for row in range(height):
                    for column in range(width):
                        if isinstance(matrix[row][column], float) and min_angle <= matrix[row][column] < min_angle + 1:
                            matrix[row][column] = counter
            counter += 1

        return matrix

    def multi_spiral_matrix(self, width, height, as_timings=True, reverse=False, mirrored=False):
        matrix = self.__multi_spiral_matrix_core(width, height)
        number_of_bands = (width + 1) * (height + 1) // 4
        matrix = self.__mirror_matrix(matrix, mirrored)
        self.__reverse_matrix_values(matrix, number_of_bands, reverse)
        self.__convert_matrix_values_to_ticks(matrix, number_of_bands, as_timings)
        return matrix

    def spiral_matrix(self, width, height, double_spiral=False, as_timings=True, reverse=False, mirrored=False):
        matrix = self.__spiral_matrix_core(width, height, double_spiral)
        number_of_bands = 1 + width * height // 2 if double_spiral else width * height
        matrix = self.__mirror_matrix(matrix, mirrored)
        self.__reverse_matrix_values(matrix, number_of_bands, reverse)
        self.__convert_matrix_values_to_ticks(matrix, number_of_bands, as_timings)
        return matrix

    def diagonal_matrix(self, width, height, as_timings=True, reverse=False, mirrored=False):
        number_of_bands = width + height - 1
        matrix = self.__diagonal_matrix_core(width, height, number_of_bands)
        matrix = self.__mirror_matrix(matrix, mirrored)
        self.__reverse_matrix_values(matrix, number_of_bands, reverse)
        self.__convert_matrix_values_to_ticks(matrix, number_of_bands, as_timings)
        return matrix

    def double_diagonal_matrix(self, width, height, as_timings=True, reverse=False, mirrored=False):
        number_of_bands = (width + height - 1) // 2
        matrix = self.__double_diagonal_matrix_core(width, height, number_of_bands)
        matrix = self.__mirror_matrix(matrix, mirrored)
        self.__reverse_matrix_values(matrix, number_of_bands + 1, reverse)
        self.__convert_matrix_values_to_ticks(matrix, number_of_bands + 1, as_timings)
        return matrix

    def clock_matrix(self, width, height, number_of_segments=1, cell_width=30, cell_height=30,
                     as_timings=True, reverse=False, mirrored=False):
        matrix = self.__clock_matrix_core(width, height, number_of_segments, cell_width, cell_height)
        number_of_bands = max(max(matrix)) + 1
        matrix = self.__mirror_matrix(matrix, mirrored)
        self.__reverse_matrix_values(matrix, number_of_bands, reverse)
        self.__convert_matrix_values_to_ticks(matrix, number_of_bands, as_timings)
        return matrix

    def circle_matrix(self, width, height, as_timings=True, reverse=False, mirrored=False):
        number_of_bands = (max(width, height) - 1) // 2
        matrix = self.__circle_matrix_core(width, height, number_of_bands)
        matrix = self.__mirror_matrix(matrix, mirrored)
        self.__reverse_matrix_values(matrix, number_of_bands, reverse)
        self.__convert_matrix_values_to_ticks(matrix, number_of_bands, as_timings)
        return matrix

    def vertical_swipes_matrix(self, width, height, as_timings=True, reverse=False, mirrored=False):
        number_of_bands = (width * height + 1) // 2
        matrix = self.__vertical_swipes_matrix_core(width, height)
        matrix = self.__mirror_matrix(matrix, mirrored)
        self.__reverse_matrix_values(matrix, number_of_bands, reverse)
        self.__convert_matrix_values_to_ticks(matrix, number_of_bands, as_timings)
        return matrix

    def horizontal_swipes_matrix(self, width, height, as_timings=True, reverse=False, mirrored=False):
        number_of_bands = (width * height + 1) // 2
        matrix = self.__horizontal_swipes_matrix_core(width, height)
        matrix = self.__mirror_matrix(matrix, mirrored)
        self.__reverse_matrix_values(matrix, number_of_bands, reverse)
        self.__convert_matrix_values_to_ticks(matrix, number_of_bands, as_timings)
        return matrix

    def choose_transition(self, width, height, cell_width=30, cell_height=30):
        transition_type = choice(range(8))
        reverse = choice(range(1)) == 1
        mirror = choice(range(1)) == 1
        number_of_segments = choice([1, 2, 4])
        double_spiral = choice(range(1)) == 1

        if transition_type == 0:
            return self.diagonal_matrix(width, height, as_timings=True, reverse=reverse, mirrored=mirror)
        elif transition_type == 1:
            return self.double_diagonal_matrix(width, height, as_timings=True, reverse=reverse, mirrored=mirror)
        elif transition_type == 2:
            return self.spiral_matrix(width, height, double_spiral, as_timings=True, reverse=reverse, mirrored=mirror)
        elif transition_type == 3:
            return self.multi_spiral_matrix(width, height, as_timings=True, reverse=reverse, mirrored=mirror)
        elif transition_type == 4:
            return self.circle_matrix(width, height, as_timings=True, reverse=reverse, mirrored=mirror)
        elif transition_type == 5:
            return self.horizontal_swipes_matrix(width, height, as_timings=True, reverse=reverse, mirrored=mirror)
        elif transition_type == 6:
            return self.vertical_swipes_matrix(width, height, as_timings=True, reverse=reverse, mirrored=mirror)
        else:  # 7
            return self.clock_matrix(width, height, number_of_segments, cell_width, cell_height,
                                     as_timings=True, reverse=reverse, mirrored=mirror)
