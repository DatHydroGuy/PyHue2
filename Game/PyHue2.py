import ctypes

import pygame
from pygame._sdl2 import Window

from Game import *
from Game.Scenes import *
from Game.Shared import GameConstants


class PyHue2:
    def __init__(self):
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        self.__time = 0
        self.__moves = 0

        columns = 5
        rows = 5
        self.__level = Level(self, columns, rows)
        self.num_tiles_horizontally = columns
        self.num_tiles_vertically = rows
        self.shuffle_start = None
        self.colour1 = None
        self.colour2 = None

        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("PyHue2")

        self.__clock = pygame.time.Clock()

        window_size = GameConstants.SCREEN_SIZE
        self.screen = pygame.display.set_mode(window_size, pygame.DOUBLEBUF, 32)
        self.pg_window = Window.from_display_module()

        self.__scenes = (
            TitleScene(self),
            MenuScene(self),
            ShuffleScene(self),
            PlayingGameScene(self),
            GameOverScene(self),
            HighScoreScene(self),
        )

        self.__currentScene = 0

        self.__sounds = ()

    def start(self):
        while 1:
            self.__clock.tick(GameConstants.FPS)

            self.screen.fill((0, 0, 0))

            current_scene = self.__scenes[self.__currentScene]
            current_scene.handle_events(pygame.event.get())
            current_scene.update()
            current_scene.render()

            pygame.display.update()

    def change_scene(self, scene):
        self.__currentScene = scene
        self.__scenes[self.__currentScene].setup()

    def set_size(self, width, height):
        self.num_tiles_horizontally = width
        self.num_tiles_vertically = height

    def get_grid(self):
        return self.get_level().get_game_grid()

    def get_level(self):
        return self.__level

    def set_level(self, columns, rows, pastel, spread, corner_colours=None):
        self.__level = Level(self, columns, rows, pastel, spread, corner_colours)

    def load_level(self, level_num):
        if level_num == 0:
            # play random level
            pass
        else:
            # play level from file
            self.__level = Level(self, 5, 5)
            self.__level.load(level_num)

    def get_moves(self):
        return self.__moves

    def set_moves(self, moves):
        self.__moves = moves

    def get_time(self):
        return self.__time

    def set_time(self, time):
        self.__time = time

    def play_sound(self, sound_clip):
        sound = self.__sounds[sound_clip]
        sound.stop()
        sound.play()
