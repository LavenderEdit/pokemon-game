import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Screen Dimensions
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
BATTLE_BG_PATH = os.path.join(ASSETS_DIR, "backgrounds", "battle_bgs.png")
LINK_ROOM_PATH = os.path.join(ASSETS_DIR, "backgrounds", "link_room_battle.png")

# Background crop coordinates (X, Y, Width, Height)
LINK_ROOM_RECT = (334, 2, 353, 283)

POKEMON_SPRITES_PATH = os.path.join(ASSETS_DIR, "sprites", "pokemon", "pokemon_gen1.png")
PLAYER_SPRITE_PATH = os.path.join(ASSETS_DIR, "sprites", "player", "player_spritesheet.png")
BATTLE_UI_PATH = os.path.join(ASSETS_DIR, "ui", "battle_ui.png")
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "pokemon_fire_red.ttf")

# Performance 
FPS = 60