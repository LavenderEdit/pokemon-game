import pygame
from src.config.constants import WALL_COORDS_BRENDAN, WALL_COORDS_MAY

class CollisionSystem:
    def __init__(self):
        self.walls = []
        self.set_map_collision("brendan")

    def set_map_collision(self, trainer_name):
        if trainer_name.lower() == "may":
            self.walls = [pygame.Rect(coord) for coord in WALL_COORDS_MAY]
        else:
            self.walls = [pygame.Rect(coord) for coord in WALL_COORDS_BRENDAN]

    def check_wall_collision(self, next_rect):
        for wall in self.walls:
            if next_rect.colliderect(wall):
                return True
        return False
