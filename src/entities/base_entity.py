from abc import ABC, abstractmethod
import pygame
from src.config.constants import DIR_DOWN, DEBUG_MODE

class Entity(ABC):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.direction = DIR_DOWN
        self.frame_index = 1
        self.animation_timer = 0
        self.is_moving = False
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.sprites = {}

    @abstractmethod
    def load_sprites(self):
        pass

    def draw(self, surface):
        if self.direction in self.sprites and self.sprites[self.direction]:
            current_image = self.sprites[self.direction][self.frame_index]
            surface.blit(current_image, (self.x, self.y))
        
        if DEBUG_MODE:
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 1)
