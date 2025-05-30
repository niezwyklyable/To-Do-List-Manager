
# constants
FPS = 30
WIDTH = 500
HEIGHT = 560 # must be greater than WIDTH
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
BLUE = (0, 0, 255)
CYAN = (0, 153, 153)
RADIUS = 4 # radius of the circle (representation of the event in graphical way)
GAP = 5
MARGIN = 20
BOARD_SIZE = WIDTH - 2 * MARGIN
BIAS_X = 10
BIAS_Y = 20
TILE_SIZE = (BOARD_SIZE - GAP * (7 + 1)) // 7
BIG_TILE_SIZE = (BOARD_SIZE - GAP * (4 + 1)) // 4
UP_ARROW_LEFT_VERTEX = (WIDTH - MARGIN - 2*GAP - 2*TILE_SIZE + BIAS_X,
                        HEIGHT - WIDTH)
UP_ARROW_MIDDLE_VERTEX = (WIDTH - MARGIN - 2*GAP - int(3/2*TILE_SIZE),
                        HEIGHT - WIDTH - int(2/3*TILE_SIZE) + BIAS_Y)
UP_ARROW_RIGHT_VERTEX = (WIDTH - MARGIN - 2*GAP - TILE_SIZE - BIAS_X,
                        HEIGHT - WIDTH)
DOWN_ARROW_LEFT_VERTEX = (WIDTH - MARGIN - GAP - TILE_SIZE + BIAS_X, 
                        HEIGHT - WIDTH - int(2/3*TILE_SIZE) + BIAS_Y)
DOWN_ARROW_MIDDLE_VERTEX = (WIDTH - MARGIN - GAP - int(1/2*TILE_SIZE),
                        HEIGHT - WIDTH)
DOWN_ARROW_RIGHT_VERTEX = (WIDTH - MARGIN - GAP - BIAS_X,
                            HEIGHT - WIDTH - int(2/3*TILE_SIZE) + BIAS_Y)
