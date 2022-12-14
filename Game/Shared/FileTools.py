import json
import os
from json import JSONDecodeError
from pathlib import Path

from . import Slider
from .GameConstants import GameConstants


class FileTools:
    def __init__(self) -> None:
        self.score_file = os.path.join(GameConstants.ASSET_DIR, GameConstants.SCORE_FILE)
        self.check_for_scores_file()
        self.levels_file = os.path.join(GameConstants.LEVELS_DIR, 'levels01.dat')

    def check_for_scores_file(self) -> None:
        scores_file = Path(self.score_file)
        if not scores_file.is_file():
            with open(scores_file, "w") as write_file:
                write_file.write('{}')

    def check_for_levels_file(self) -> bool:
        levels_file = Path(self.levels_file)
        return levels_file.is_file()

    def count_levels_in_file(self) -> int:
        try:
            with open(self.levels_file, "r") as read_file:
                try:
                    levels_data = read_file.readlines()
                    return len(levels_data) - 1
                except IndexError:
                    return -1
        except FileNotFoundError:
            return -1

    def read_level(self, level_number: int) -> tuple:
        width = 0
        height = 0
        pins = GameConstants.GRID_PINS_RANDOMISED
        corner_colours = []
        pin_locations = []
        try:
            with open(self.levels_file, "r") as read_file:
                try:
                    levels_data = read_file.readlines()
                    line = levels_data[level_number]
                    elements = line.split('(')
                    custom_pins = len(elements) > 5
                    for index, element in enumerate(elements):
                        element = element.replace(')', '')
                        if index == 0:
                            width, height, pins = [int(x) for x in element.split(',')[:-1]]
                        elif 1 <= index <= 4:
                            corner_colours.append(tuple(int(x) for x in element.split(',')[:-1]))
                        # elif index == 4:
                        #     if custom_pins:
                        #         pass
                        #     else:
                        #         corner_colours.append(tuple(int(x) for x in element.split(',')[:-1]))
                        if custom_pins and index > 4:
                            if index < len(elements) - 1:
                                pin_locations.append(tuple(int(x) for x in element.split(',')[:-1]))
                            else:
                                element = element.replace(']', '')
                                pin_locations.append(tuple(int(x) for x in element.split(',')))

                except IndexError:
                    width = -1
                    height = -1
                    pins = -1
                    corner_colours = [(-1,)]
        except FileNotFoundError:
            width = -1
            height = -1
            pins = -1
            corner_colours = [(-1,)]
        return width, height, pins, corner_colours, pin_locations

    def save_level(self, sliders: list[Slider], corner_colours: list[list[int]],
                   custom_pins: list[tuple[int, int]]) -> None:
        corner_tuple = [tuple(c) for c in corner_colours]
        custom_pins = str(custom_pins)
        new_level = \
            f'\n{sliders[0].value},{sliders[1].value},{sliders[6].value},{",".join(str(c) for c in corner_tuple)},' \
            f'{custom_pins}'
        try:
            with open(self.levels_file, "a") as write_file:
                write_file.writelines([new_level])
        except FileNotFoundError:
            pass

    def get_high_scores(self, level: int, width: int, height: int, pastel: int, spread: int, pins: int,
                        pin_spread: int) -> dict:
        with open(self.score_file, "r") as read_file:
            try:
                scores_dict = json.load(read_file)
            except JSONDecodeError:
                scores_dict = {}

        try:
            _ = scores_dict[str(level)]
        except KeyError:
            scores_dict[str(level)] = {}

        try:
            _ = scores_dict[str(level)][str(width)]
        except KeyError:
            scores_dict[str(level)][str(width)] = {}

        try:
            _ = scores_dict[str(level)][str(width)][str(height)]
        except KeyError:
            scores_dict[str(level)][str(width)][str(height)] = {}

        try:
            _ = scores_dict[str(level)][str(width)][str(height)][str(pastel)]
        except KeyError:
            scores_dict[str(level)][str(width)][str(height)][str(pastel)] = {}

        try:
            _ = scores_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)]
        except KeyError:
            scores_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)] = {}

        try:
            _ = scores_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)][str(pins)]
        except KeyError:
            scores_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)][str(pins)] = {}

        try:
            _ = scores_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)][str(pins)][str(pin_spread)]
        except KeyError as e:
            scores_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)][str(pins)][str(pin_spread)] = \
                [0, 0, 0]

        return scores_dict

    def save_high_scores(self, level: int, width: int, height: int, pastel: int, spread: int, pins: int,
                         pin_spread: int, moves: int, seconds: float) -> None:
        saved_dict = self.get_high_scores(level, width, height, pastel, spread, pins, pin_spread)
        curr_stats = \
            saved_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)][str(pins)][str(pin_spread)]
        new_avg_moves = (curr_stats[1] * curr_stats[0] + moves) / (curr_stats[0] + 1)
        new_avg_time = (curr_stats[2] * curr_stats[0] + seconds) / (curr_stats[0] + 1)
        saved_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)][str(pins)][str(pin_spread)] = \
            [curr_stats[0] + 1, new_avg_moves, new_avg_time]

        with open(self.score_file, "w") as write_file:
            json.dump(saved_dict, write_file)
