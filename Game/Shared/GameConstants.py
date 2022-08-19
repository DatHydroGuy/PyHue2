import os.path


class GameConstants:
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

    SCREEN_SIZE = [800, 600]
    TILE_SIZE = [30, 30]

    SOLVED_FADE_IN = 1500
    SOLVED_PAUSE = 500
    SOLVED_FADE_OUT = 1500
