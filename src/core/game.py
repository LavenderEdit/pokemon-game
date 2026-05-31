import pygame
import sys
from src.config.constants import *
from src.entities.player import Player
from src.overworld.collision import CollisionSystem
from src.entities.npc import NPC

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
        
        self.collision_system = CollisionSystem()
        self.player = Player(113, 143)
        
        self.npc = NPC(START_BATTLE_POSITION[0], START_BATTLE_POSITION[1])
        
        self.fade_alpha = 0
        self.is_fading = False

    def load_assets(self):
        print("Loading assets...")
        try:
            self.map_brendan = pygame.image.load(MAP_BRENDAN_PATH).convert()
            self.map_may = pygame.image.load(MAP_MAY_PATH).convert()
            self.current_bg = self.map_brendan
        except pygame.error as e:
            print(f"Error loading backgrounds: {e}")
            self.map_brendan = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.map_brendan.fill((50, 50, 50))
            self.map_may = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.map_may.fill((34, 139, 34))
            self.current_bg = self.map_brendan

    def set_active_map(self, trainer_name):
        if trainer_name.lower() == "may":
            self.current_bg = self.map_may
            self.collision_system.set_map_collision("may")
        else:
            self.current_bg = self.map_brendan
            self.collision_system.set_map_collision("brendan")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                if event.key == pygame.K_1: self.set_active_map("brendan")
                if event.key == pygame.K_2: self.set_active_map("may")
                
                if event.key == pygame.K_SPACE or event.key == pygame.K_z:
                    if self.state == STATE_OVERWORLD and not self.is_fading:
                        interaction_rect = self.player.rect.inflate(12, 12)
                        if interaction_rect.colliderect(self.npc.rect):
                            print("💬 ¡Interacción con Brendan iniciada! Iniciando secuencia de combate...")
                            self.is_fading = True # Dispara el fundido a negro

    def update(self):
        if self.state == STATE_OVERWORLD:
            self.collision_system.update_dynamic_obstacles([self.npc])

            if not self.is_fading:
                self.player.update(self.collision_system)
            else:
                self.fade_alpha += 15
                if self.fade_alpha >= 255:
                    self.fade_alpha = 255
                    
                    self.player.x, self.player.y = PLAYER_REPOSITION_TO_START_BATTLE
                    self.player.direction = DIR_RIGHT
                    self.player.rect.topleft = (self.player.x, self.player.y)
                    
                    self.npc.reposition(BRENDAN_SPAWN_LOCATION, DIR_LEFT)
                    
                    self.is_fading = False
                    self.fade_alpha = 0
                    self.state = STATE_BATTLE
                    print("⚔️ ¡Posiciones listas! Transición al motor de combate completada.")

    def draw(self):
        self.internal_surface.fill(BLACK)
        
        if self.state == STATE_OVERWORLD or self.state == STATE_BATTLE:
            bg_x = (WINDOW_WIDTH - self.current_bg.get_width()) // 2
            bg_y = (WINDOW_HEIGHT - self.current_bg.get_height()) // 2
            self.internal_surface.blit(self.current_bg, (bg_x, bg_y))
            
            if DEBUG_MODE:
                for wall in self.collision_system.walls:
                    pygame.draw.rect(self.internal_surface, (255, 0, 0), wall, 1)
            
            self.npc.draw(self.internal_surface)
            self.player.draw(self.internal_surface)
            
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            fade_surface.fill(BLACK)
            fade_surface.set_alpha(self.fade_alpha)
            self.internal_surface.blit(fade_surface, (0, 0))
            
        scaled_surface = pygame.transform.scale(
            self.internal_surface, 
            (WINDOW_WIDTH * SCALE_FACTOR, WINDOW_HEIGHT * SCALE_FACTOR)
        )
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