import pygame
from src.config.constants import *
from src.engine.sprite_loader import SpriteSheet

TRANSPARENT_COLOR = (255, 127, 39)

class NPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = DIR_DOWN
        self.frame_index = 1
        
        self.width = 17
        self.height = 25
        
        self.sprites = self.load_sprites()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def load_sprites(self):
        sheet = SpriteSheet(TRAINERS_OVERWORLD_PATH)
        sprites = {}
        try:
            sprites = {
                DIR_DOWN: sheet.images_at(BRENDAN_RECTS[DIR_DOWN], colorkey=TRANSPARENT_COLOR),
                DIR_UP: sheet.images_at(BRENDAN_RECTS[DIR_UP], colorkey=TRANSPARENT_COLOR),
                DIR_LEFT: sheet.images_at(BRENDAN_RECTS[DIR_LEFT], colorkey=TRANSPARENT_COLOR),
                DIR_RIGHT: sheet.images_at(BRENDAN_RECTS[DIR_RIGHT], colorkey=TRANSPARENT_COLOR)
            }
        except Exception as e:
            print(f"Error cortando sprites del NPC: {e}")
            fallback = [pygame.Surface((self.width, self.height)) for _ in range(3)]
            for s in fallback: s.fill((0, 255, 0))
            sprites = { DIR_DOWN: fallback, DIR_UP: fallback, DIR_LEFT: fallback, DIR_RIGHT: fallback }
        return sprites

    def reposition(self, new_coords, face_direction):
        self.x, self.y = new_coords
        self.direction = face_direction
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        current_image = self.sprites[self.direction][self.frame_index]
        surface.blit(current_image, (self.x, self.y))
        
        if DEBUG_MODE:
            pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)
