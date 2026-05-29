import pygame
import sys
from src.config.constants import (
    BLACK, FONT_PATH, FPS, SCALE_FACTOR, WHITE, 
    WINDOW_HEIGHT, WINDOW_WIDTH
)
from src.engine.sprite_loader import SpriteSheet

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pokémon Roguelike Simulator")
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH * SCALE_FACTOR, WINDOW_HEIGHT * SCALE_FACTOR))
        
        self.internal_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = None
        
        self.load_assets()

    def load_assets(self):
        print("Loading assets...")
        
        try:
            self.font = pygame.font.Font(FONT_PATH, 16)
        except Exception as e:
            print(f"Warning: Could not load custom font. Using default. Error: {e}")
            self.font = pygame.font.Font(None, 24)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        """Render all graphics to the screen."""
        self.internal_surface.fill(BLACK)
        
        text_surface = self.font.render("Welcome to the Link Room!", True, WHITE)
        self.internal_surface.blit(text_surface, (10, 10))
        
        scaled_surface = pygame.transform.scale(
            self.internal_surface, 
            (WINDOW_WIDTH * SCALE_FACTOR, WINDOW_HEIGHT * SCALE_FACTOR)
        )
        self.screen.blit(scaled_surface, (0, 0))
        
        pygame.display.flip()

    def run(self):
        """Main game loop."""
        print("Starting game loop...")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
