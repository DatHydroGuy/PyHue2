import os.path


class GameConstants:
    """ Game constants: Leave this section alone - the user section is found later in this file. """
    FPS = 100
    ASSET_DIR = os.path.join("Game", "Assets")
    LEVELS_DIR = os.path.join(ASSET_DIR, "Levels")
    SCORE_FILE = "scores.json"
    SYM_FONT_FILE = "seguisym.ttf"

    GRID_PINS_CORNERS = 0
    GRID_PINS_VERTICAL = 1
    GRID_PINS_HORIZONTAL = 2
    GRID_PINS_BORDERS = 3
    GRID_PINS_ALTERNATING = 4
    GRID_PINS_DIAGONAL = 5
    GRID_PINS_RANDOM_DIAGONAL = 6
    GRID_PINS_KNIGHTS_TOUR = 7
    GRID_PINS_RANDOM = 8
    GRID_PINS_RANDOMISED = 9
    GRID_PINS_CUSTOM = 10

    FADE_OUT_START = 1000
    FADE_OUT_DURATION = 2500
    FADE_PAUSE = 500
    FADE_IN_DURATION = 2500
    TILE_FADE_OUT_DURATION = 200
    TILE_FADE_IN_DURATION = 200

    SOLVED_FADE_IN = 1500
    SOLVED_PAUSE = 500
    SOLVED_FADE_OUT = 1500

    """ User section: Feel free to play around with these to suit your own needs. """
    SCREEN_SIZE = [1920, 1200]
    WINDOW_SIZE = [800, 600]
    PREVIEW_SIZE = [int(WINDOW_SIZE[0] * 0.75), int(WINDOW_SIZE[1] * 0.75)]
    PREVIEW_X_OFFSET = int(WINDOW_SIZE[0] * 0.125)
    PREVIEW_Y_OFFSET = 50
    TILE_SIZE = [30, 30]
    MIN_GRID_COLUMNS = 5
    MAX_GRID_COLUMNS = SCREEN_SIZE[0] / TILE_SIZE[0] if (SCREEN_SIZE[0] / TILE_SIZE[0]) % 2 == 1 else \
        (SCREEN_SIZE[0] / TILE_SIZE[0]) - 1
    MIN_GRID_ROWS = 5
    # NOTE: In the next line, the -2 allows space for the window title bar and the Windows taskbar
    MAX_GRID_ROWS = (SCREEN_SIZE[1] / TILE_SIZE[1]) - 2 if (SCREEN_SIZE[1] / TILE_SIZE[1]) % 2 == 1 else \
        (SCREEN_SIZE[1] / TILE_SIZE[1]) - 3
    MIN_PASTEL = 0
    MAX_PASTEL = 100
    MIN_SPREAD = 10
    MAX_SPREAD = 100
    DEFAULT_WIDTH = 5
    DEFAULT_HEIGHT = 5
    DEFAULT_PASTEL = 0
    DEFAULT_SPREAD = 100
    MIN_TIME_BETWEEN_BUTTON_CLICKS = 250
