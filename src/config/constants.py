import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Screen Dimensions (Resolución original GBA)
WINDOW_WIDTH = 240
WINDOW_HEIGHT = 160
SCALE_FACTOR = 4

# Colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game States 
STATE_OVERWORLD = "OVERWORLD"
STATE_BATTLE = "BATTLE"

# Directions 
DIR_DOWN = "DOWN"
DIR_UP = "UP"
DIR_LEFT = "LEFT"
DIR_RIGHT = "RIGHT"

# Asset Paths 
BATTLE_BG_PATH = os.path.join(ASSETS_DIR, "backgrounds", "bg_grass.png")
BATTLE_UI_PATH = os.path.join(ASSETS_DIR, "ui", "battle_ui.png")
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "pokemon_fire_red.ttf")

# Sprites
POKEMON_SPRITES_PATH = os.path.join(ASSETS_DIR, "sprites", "pokemon", "pokemon_gen1.png")
PLAYER_SPRITE_PATH = os.path.join(ASSETS_DIR, "sprites", "player", "player_spritesheet.png")

MAP_BRENDAN_PATH = os.path.join(ASSETS_DIR, "backgrounds", "link_room_classic.png")
MAP_MAY_PATH = os.path.join(ASSETS_DIR, "backgrounds", "link_room_colosseum.png")

# COLISIONES ESPECÍFICAS POR MAPA
WALL_COORDS_BRENDAN = [
    (26, 9, 69, 38),
    (95, 6, 52, 42),
    (147, 9, 69, 39),
    (6, 58, 9, 86),
    (227, 57, 9, 87),
    (17, 146, 87, 17),
    (138, 146, 88, 16),
    (104, 165, 35, 8),
    (8, 9, 18, 39),
    (216, 9, 18, 38)
]

WALL_COORDS_MAY = [
    (0, 0, 240, 48),
]

# Performance 
FPS = 60

# SISTEMA DEBUG GLOBAL
DEBUG_MODE = False

PLAYER_CUSTOM_SCALE = 1.0

PLAYER_BASE_SPEED = 1.0
PLAYER_MAX_HP = 100
PLAYER_START_LEVEL = 5
PLAYER_START_MONEY = 3000

# RUTA DE TEXTURAS DE ENTRENADORES EN EL OVERWORLD
TRAINERS_OVERWORLD_PATH = os.path.join(ASSETS_DIR, "sprites", "trainers", "trainers_overworld.png")

START_BATTLE_POSITION = (112, 80)
BRENDAN_SPAWN_LOCATION = (185, 80)
PLAYER_REPOSITION_TO_START_BATTLE = (41, 80)

BRENDAN_RECTS = {
    DIR_DOWN: [(9, 1985, 16, 23), (26, 1985, 16, 23), (42, 1985, 16, 23)],
    DIR_UP:   [(60, 1985, 16, 23), (77, 1985, 16, 23), (94, 1985, 16, 23)],
    DIR_LEFT: [(111, 1985, 16, 23), (128, 1985, 16, 23), (145, 1985, 16, 23)],
    DIR_RIGHT:[(162, 1985, 16, 23), (179, 1985, 16, 23), (196, 1985, 16, 23)]
}
