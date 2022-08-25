import json
import os
from json import JSONDecodeError
from pathlib import Path

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

    def read_level(self, level_number: int) -> tuple:
        width = 0
        height = 0
        corner_colours = []
        try:
            with open(self.levels_file, "r") as read_file:
                try:
                    levels_data = read_file.readlines()
                    line = levels_data[level_number]
                    elements = line.split('(')
                    for index, element in enumerate(elements):
                        element = element.replace(')', '')
                        if index == 0:
                            width, height = [int(x) for x in element.split(',')[:-1]]
                        elif 1 <= index <= 3:
                            corner_colours.append(tuple(int(x) for x in element.split(',')[:-1]))
                        elif index == 4:
                            corner_colours.append(tuple(int(x) for x in element.split(',')))

                except IndexError:
                    width = -1
                    height = -1
                    corner_colours = None
        except FileNotFoundError:
            width = -1
            height = -1
            corner_colours = None
        return width, height, corner_colours

    def get_high_scores(self, level: int, width: int, height: int, pastel: int, spread: int, pins: int) -> dict:
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
            scores_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)][str(pins)] = [0, 0, 0]

        return scores_dict

    def save_high_scores(self, level: int, width: int, height: int, pastel: int, spread: int, pins: int, moves: int,
                         seconds: float) -> None:
        saved_dict = self.get_high_scores(level, width, height, pastel, spread, pins)
        curr_stats = saved_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)][str(pins)]
        new_avg_moves = (curr_stats[1] * curr_stats[0] + moves) / (curr_stats[0] + 1)
        new_avg_time = (curr_stats[2] * curr_stats[0] + seconds) / (curr_stats[0] + 1)
        saved_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)][str(pins)] = [curr_stats[0] + 1,
                                                                                                new_avg_moves,
                                                                                                new_avg_time]

        with open(self.score_file, "w") as write_file:
            json.dump(saved_dict, write_file)
