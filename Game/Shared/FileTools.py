import json
import os
from json import JSONDecodeError
from pathlib import Path

from Game.Shared import GameConstants


class FileTools:
    def __init__(self):
        self.score_file = os.path.join(GameConstants.ASSET_DIR, GameConstants.SCORE_FILE)
        self.check_for_scores_file()
        self.levels_file = os.path.join(GameConstants.LEVELS_DIR, 'levels01.dat')
        # self.check_for_levels_file()

    def check_for_scores_file(self):
        scores_file = Path(self.score_file)
        if not scores_file.is_file():
            with open(scores_file, "w") as write_file:
                write_file.write('{}')

    def check_for_levels_file(self):
        levels_file = Path(self.levels_file)
        return levels_file.is_file()
        # if not levels_file.is_file():
        #     with open(levels_file, "w") as write_file:
        #         write_file.write('#columns,rows,upperleftcolour,upperrightcolour,lowerleftcolour,lowerrightcolour\n')

    def read_level(self, level_number):
        width = 0
        height = 0
        corner_colours = []
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
        return width, height, corner_colours

    def get_high_scores(self, level, width, height, pastel, spread):
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
            scores_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)] = [0, 0, 0]

        return scores_dict

    def save_high_scores(self, level, width, height, pastel, spread, moves, seconds):
        saved_dict = self.get_high_scores(level, width, height, pastel, spread)
        curr_stats = saved_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)]
        new_avg_moves = (curr_stats[1] * curr_stats[0] + moves) / (curr_stats[0] + 1)
        new_avg_time = (curr_stats[2] * curr_stats[0] + seconds) / (curr_stats[0] + 1)
        saved_dict[str(level)][str(width)][str(height)][str(pastel)][str(spread)] = [curr_stats[0] + 1,
                                                                                     new_avg_moves,
                                                                                     new_avg_time]

        with open(self.score_file, "w") as write_file:
            json.dump(saved_dict, write_file)
