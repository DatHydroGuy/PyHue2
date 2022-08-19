import os.path


class GameConstants:
    FPS = 100
    ASSET_DIR = os.path.join("Game", "Assets")
    LEVELS_DIR = os.path.join(ASSET_DIR, "Levels")
    SCORE_FILE = "scores.json"
    SYM_FONT_FILE = "seguisym.ttf"

    GRID_TYPE_CORNERS = 0
    GRID_TYPE_VERTICAL = 1
    GRID_TYPE_HORIZONTAL = 2
    GRID_TYPE_BORDERS = 3
    GRID_TYPE_ALTERNATING = 4
    GRID_TYPE_DIAGONAL = 5
    GRID_TYPE_KNIGHTS_TOUR = 6
    GRID_TYPE_RANDOM = 7

    SCREEN_SIZE = [800, 600]
    TILE_SIZE = [30, 30]

    SOLVED_FADE_IN = 1500
    SOLVED_PAUSE = 500
    SOLVED_FADE_OUT = 1500

    # SPRITE_BALL = os.path.join("Assets", "ball.png")
    # SPRITE_BRICK = os.path.join("Assets", "standard.png")
    # SPRITE_SPEED_BRICK = os.path.join("Assets", "speed.png")
    # SPRITE_LIFE_BRICK = os.path.join("Assets", "life.png")
