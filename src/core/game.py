import pygame
import sys
from src.config.constants import *
from src.entities.player import Player

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pokémon Roguelike Simulator")
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH * SCALE_FACTOR, WINDOW_HEIGHT * SCALE_FACTOR))
        self.internal_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.state = STATE_OVERWORLD
        self.load_assets()
        
        self.player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    def load_assets(self):
        print("Loading assets...")
        try:
            raw_bg = pygame.image.load(LINK_ROOM_PATH).convert()
            
            cropped_bg = raw_bg.subsurface(pygame.Rect(LINK_ROOM_RECT))
            
            self.bg_link_room = pygame.transform.scale(cropped_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except pygame.error as e:
            print(f"Error loading Link Room background: {e}")
            self.bg_link_room = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.bg_link_room.fill((50, 50, 50)) # Fallback gray

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        if self.state == STATE_OVERWORLD:
            self.player.update()
            
            if self.player.y < 40:
                print("🚨 Battle Triggered! Transitioning to Combat...")
                self.player.y = 40

    def draw(self):
        self.internal_surface.fill(BLACK)
        
        if self.state == STATE_OVERWORLD:
            self.internal_surface.blit(self.bg_link_room, (0, 0))
            self.player.draw(self.internal_surface)
            
        scaled_surface = pygame.transform.scale(self.internal_surface, (WINDOW_WIDTH * SCALE_FACTOR, WINDOW_HEIGHT * SCALE_FACTOR))
        self.screen.blit(scaled_surface, (0, 0))
        
        pygame.display.flip()

    def run(self):
        print("Starting game loop...")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()