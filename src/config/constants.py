import os

# Screen Dimensions
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 320
SCALE_FACTOR = 2

# Colors 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Asset Paths 
ASSETS_DIR = "assets"
DATA_DIR = "data"

# Backgrounds
BATTLE_BG_PATH = os.path.join(ASSETS_DIR, "backgrounds", "battle_bgs.png")
LINK_ROOM_PATH = os.path.join(ASSETS_DIR, "backgrounds", "link_room_battle.png")

# Sprites
POKEMON_SPRITES_PATH = os.path.join(ASSETS_DIR, "sprites", "pokemon", "pokemon_gen1.png")
PLAYER_SPRITE_PATH = os.path.join(ASSETS_DIR, "sprites", "player", "player_spritesheet.png")
TRAINERS_BATTLE_PATH = os.path.join(ASSETS_DIR, "sprites", "trainers", "trainers_battle.png")

# UI
BATTLE_UI_PATH = os.path.join(ASSETS_DIR, "ui", "battle_ui.png")
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "pokemon_fire_red.ttf")

# Databases
POKEMON_DB_PATH = os.path.join(DATA_DIR, "pokemon.json")
MOVES_DB_PATH = os.path.join(DATA_DIR, "moves.json")
EVOLUTIONS_DB_PATH = os.path.join(DATA_DIR, "evolutions.json")

# FPS Limit
FPS = 60