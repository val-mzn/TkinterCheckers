BLACK = 'Red'
WHITE = 'White'
HUMAN = 'human'
BOT = 'bot'

DESIRED_WINDOW_SIZE = 600
if DESIRED_WINDOW_SIZE < 300:
    DESIRED_WINDOW_SIZE = 300

BOARD_SIZE = 10

CASE_SIZE = DESIRED_WINDOW_SIZE // BOARD_SIZE
WINDOW_SIZE = CASE_SIZE * BOARD_SIZE

MIN_TIME_TURN = 1000

SOUND_PIECE_PLAY = 'sounds/Piece Placed2.wav'
BACKGROUND_FILE = 'sprites/backgrounds/Blue 1.png'
TILE_FILE = 'sprites/boards/Tile 1.png'
MOVE_SELECTOR_FILE = 'sprites/other/Move Selector.png'

WHITE_QUEEN_FILE = 'sprites/pieces/White 1 - normal.png'
BLACK_QUEEN_FILE = 'sprites/pieces/Red 1 - normal.png'

WHITE_KING_FILE = 'sprites/pieces/White 1 - king.png'
BLACK_KING_FILE = 'sprites/pieces/Red 1 - king.png'

MINMAX_DEPTH = 4

GUI_WIN_FILE = 'sprites/gui/Large Menu Button Highlighted.png'