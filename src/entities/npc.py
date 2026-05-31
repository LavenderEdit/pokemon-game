import pygame
from src.config.constants import *
from src.engine.sprite_loader import SpriteSheet
from src.entities.base_entity import Entity 

TRANSPARENT_COLOR = (255, 127, 39)

class NPC(Entity):
    def __init__(self, x, y, name="brendan"):
        self.name = name
        
        self.width = 16
        self.height = 20
        
        super().__init__(x, y, self.width, self.height)
        
        self.collision_w = 15
        self.collision_h = 20
        
        self.rect = pygame.Rect(self.x, self.y, self.collision_w, self.collision_h)
        
        self.sprites = self.load_sprites()
        self.frame_index = 1

    def load_sprites(self):
        sheet = SpriteSheet(TRAINERS_OVERWORLD_PATH)
        sprites = {}
        try:
            sprites = {
                DIR_DOWN: sheet.images_at(BRENDAN_RECTS[DIR_DOWN], colorkey=TRANSPARENT_COLOR),
                DIR_UP:   sheet.images_at(BRENDAN_RECTS[DIR_UP], colorkey=TRANSPARENT_COLOR),
                DIR_LEFT: sheet.images_at(BRENDAN_RECTS[DIR_LEFT], colorkey=TRANSPARENT_COLOR),
                DIR_RIGHT:sheet.images_at(BRENDAN_RECTS[DIR_RIGHT], colorkey=TRANSPARENT_COLOR)
            }
        except Exception as e:
            print(f"Error cortando sprites del NPC {self.name}: {e}")
            fallback = [pygame.Surface((self.width, self.height)) for _ in range(3)]
            for s in fallback: s.fill((0, 255, 0)) # Cuadrado verde como respaldo
            sprites = { DIR_DOWN: fallback, DIR_UP: fallback, DIR_LEFT: fallback, DIR_RIGHT: fallback }
        return sprites

    def reposition(self, new_coords, face_direction):
        self.x, self.y = new_coords
        self.direction = face_direction
        
        self.rect.topleft = (self.x + 1, self.y + 15)
