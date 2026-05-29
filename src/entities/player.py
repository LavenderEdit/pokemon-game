import pygame
from src.config.constants import *
from src.engine.sprite_loader import SpriteSheet

DEBUG_MODE = False

TRANSPARENT_COLOR = (255, 127, 39)

PLAYER_RECTS = {
    DIR_DOWN: [
        (8, 55, 16, 19),
        (25, 53, 16, 21),
        (43, 54, 15, 20),
    ],
    DIR_UP: [
        (8, 87, 16, 20),
        (25, 86, 16, 21),
        (42, 87, 16, 20),
    ],
    DIR_LEFT: [
        (8, 120, 15, 20),
        (25, 119, 15, 21),
        (42, 120, 15, 20),
    ],
    DIR_RIGHT: [
        (9, 153, 15, 20),
        (26, 152, 15, 21),
        (43, 153, 15, 20),
    ]
}

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.5
        self.direction = DIR_DOWN
        self.is_moving = False
        
        self.frame_index = 1 
        self.animation_timer = 0
        
        self.sprites = self.load_sprites()
        self.rect = pygame.Rect(self.x, self.y, 16, 22)

    def load_sprites(self):
        sheet = SpriteSheet(PLAYER_SPRITE_PATH)
        sprites = {}
        
        try:
            sprites = {
                DIR_DOWN: sheet.images_at(PLAYER_RECTS[DIR_DOWN], colorkey=TRANSPARENT_COLOR),
                DIR_UP: sheet.images_at(PLAYER_RECTS[DIR_UP], colorkey=TRANSPARENT_COLOR),
                DIR_LEFT: sheet.images_at(PLAYER_RECTS[DIR_LEFT], colorkey=TRANSPARENT_COLOR),
                DIR_RIGHT: sheet.images_at(PLAYER_RECTS[DIR_RIGHT], colorkey=TRANSPARENT_COLOR)
            }
        except Exception as e:
            print(f"Atlas slicing warning: {e}")
            fallback = [pygame.Surface((16, 22)) for _ in range(3)]
            for s in fallback: s.fill((255, 0, 0))
            sprites = { DIR_DOWN: fallback, DIR_UP: fallback, DIR_LEFT: fallback, DIR_RIGHT: fallback }
            
        return sprites

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = DIR_UP
            self.y -= self.speed
            self.is_moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = DIR_DOWN
            self.y += self.speed
            self.is_moving = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = DIR_LEFT
            self.x -= self.speed
            self.is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = DIR_RIGHT
            self.x += self.speed
            self.is_moving = True

        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.handle_input()
        
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= 8:
                self.frame_index = (self.frame_index + 1) % 3
                self.animation_timer = 0
        else:
            self.frame_index = 1 
            self.animation_timer = 0

    def draw(self, surface):
        current_image = self.sprites[self.direction][self.frame_index]
        surface.blit(current_image, (self.x, self.y))
        
        if DEBUG_MODE:
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.rect.width, self.rect.height), 1)
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 1.0
        self.direction = DIR_DOWN
        self.is_moving = False
        
        self.frame_index = 1 
        self.animation_timer = 0
        
        self.sprites = self.load_sprites()
        
        self.rect = pygame.Rect(self.x, self.y, 16, 22)

    def load_sprites(self):
        sheet = SpriteSheet(PLAYER_SPRITE_PATH)
        sprites = {}
        TRANSPARENT_COLOR = (255, 127, 39)
        
        try:
            sprites = {
                DIR_DOWN: sheet.images_at(PLAYER_RECTS[DIR_DOWN], colorkey=TRANSPARENT_COLOR),
                DIR_UP: sheet.images_at(PLAYER_RECTS[DIR_UP], colorkey=TRANSPARENT_COLOR),
                DIR_LEFT: sheet.images_at(PLAYER_RECTS[DIR_LEFT], colorkey=TRANSPARENT_COLOR),
                DIR_RIGHT: sheet.images_at(PLAYER_RECTS[DIR_RIGHT], colorkey=TRANSPARENT_COLOR)
            }
        except Exception as e:
            print(f"Atlas slicing warning: {e}")
            fallback = [pygame.Surface((16, 22)) for _ in range(3)]
            for s in fallback: s.fill((255, 0, 0))
            sprites = { DIR_DOWN: fallback, DIR_UP: fallback, DIR_LEFT: fallback, DIR_RIGHT: fallback }
            
        return sprites

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = DIR_UP
            self.y -= self.speed
            self.is_moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = DIR_DOWN
            self.y += self.speed
            self.is_moving = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = DIR_LEFT
            self.x -= self.speed
            self.is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = DIR_RIGHT
            self.x += self.speed
            self.is_moving = True

        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.handle_input()
        
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= 8:
                self.frame_index = (self.frame_index + 1) % 3
                self.animation_timer = 0
        else:
            self.frame_index = 1 
            self.animation_timer = 0

    def draw(self, surface):
        current_image = self.sprites[self.direction][self.frame_index]
        surface.blit(current_image, (self.x, self.y))
        
        if DEBUG_MODE:
            pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.rect.width, self.rect.height), 1)