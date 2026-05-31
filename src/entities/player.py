import pygame
from src.config.constants import *
from src.engine.sprite_loader import SpriteSheet

TRANSPARENT_COLOR = (255, 127, 39)

PLAYER_RECTS = {
    DIR_DOWN: [(8, 55, 16, 19), (25, 53, 16, 21), (43, 54, 15, 20)],
    DIR_UP: [(8, 87, 16, 20), (25, 86, 16, 21), (42, 87, 16, 20)],
    DIR_LEFT: [(8, 120, 15, 20), (25, 119, 15, 21), (42, 120, 15, 20)],
    DIR_RIGHT: [(9, 153, 15, 20), (26, 152, 15, 21), (43, 153, 15, 20)]
}

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.speed = PLAYER_BASE_SPEED
        self.max_hp = PLAYER_MAX_HP
        self.current_hp = PLAYER_MAX_HP
        self.level = PLAYER_START_LEVEL
        self.money = PLAYER_START_MONEY
        
        self.rect = pygame.Rect(self.x + 2, self.y + 14, 16, 8)
        self.direction = DIR_UP
        self.is_moving = False
        self.frame_index = 1
        self.animation_timer = 0
        
        base_w, base_h = 15, 20
        self.width = int(base_w * PLAYER_CUSTOM_SCALE)
        self.height = int(base_h * PLAYER_CUSTOM_SCALE)
        
        self.sprites = self.load_sprites()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def load_sprites(self):
        sheet = SpriteSheet(PLAYER_SPRITE_PATH)
        sprites = {}
        
        try:
            for direction, rect_list in PLAYER_RECTS.items():
                direction_images = []
                for rect in rect_list:
                    img = sheet.image_at(rect, colorkey=TRANSPARENT_COLOR)
                    
                    if PLAYER_CUSTOM_SCALE != 1.0:
                        new_w = int(img.get_width() * PLAYER_CUSTOM_SCALE)
                        new_w = max(1, new_w)
                        new_h = int(img.get_height() * PLAYER_CUSTOM_SCALE)
                        new_h = max(1, new_h)
                        img = pygame.transform.scale(img, (new_w, new_h))
                        
                    direction_images.append(img)
                sprites[direction] = direction_images
                
        except Exception as e:
            print(f"Atlas slicing warning: {e}")
            fallback = [pygame.Surface((self.width, self.height)) for _ in range(3)]
            for s in fallback: s.fill((255, 0, 0))
            sprites = { DIR_DOWN: fallback, DIR_UP: fallback, DIR_LEFT: fallback, DIR_RIGHT: fallback }
            
        return sprites

    def handle_input(self, collision_system):
        keys = pygame.key.get_pressed()
        self.is_moving = False
        
        dx = 0
        dy = 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction = DIR_UP
            dy = -self.speed
            self.is_moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction = DIR_DOWN
            dy = self.speed
            self.is_moving = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction = DIR_LEFT
            dx = -self.speed
            self.is_moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction = DIR_RIGHT
            dx = self.speed
            self.is_moving = True

        if dx != 0:
            next_rect = self.rect.copy()
            next_rect.x += dx
            if not collision_system.check_wall_collision(next_rect):
                self.x += dx
            else:
                self.is_moving = False

        if dy != 0:
            next_rect = self.rect.copy()
            next_rect.y += dy
            if not collision_system.check_wall_collision(next_rect):
                self.y += dy
            else:
                self.is_moving = False

        self.rect.topleft = (int(self.x), int(self.y))

    def update(self, collision_system):
        self.handle_input(collision_system)
        
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
            pygame.draw.rect(surface, (0, 0, 255), self.rect, 1)
