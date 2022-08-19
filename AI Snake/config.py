import enum

BOARD_SIZE = 16
HEIGHT = 700
GUI_WIDTH = 700
BLOCK_SIZE = GUI_WIDTH / BOARD_SIZE
FRAME_RATE = 30


class Direction(enum.Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class GameState(enum.Enum):
    RUNNING = 1
    PAUSED = 2
    GAME_OVER = 3
