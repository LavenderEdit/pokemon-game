import pygame
import random
import os
import math
from src.battle.pokemon import Pokemon, Move, DatabaseLoader

class BattleScene:
    def __init__(self, screen, player_team, enemy_team, font):
        self.screen = screen
        self.player_team = player_team
        self.enemy_team = enemy_team
        
        self.active_player_idx = 0
        self.active_enemy_idx = 0
        self.player_pkmn = self.player_team[self.active_player_idx]
        self.enemy_pkmn = self.enemy_team[self.active_enemy_idx]
        
        self.scale = 4
        self.bottom_y = 110 * self.scale
        
        # Posiciones Clásicas Actualizadas
        self.pos_enemy_pkmn = (144 * self.scale, 45 * self.scale)
        self.pos_enemy_hp = (21 * self.scale, 27 * self.scale)
        
        self.pos_player_pkmn = (47 * self.scale, 89 * self.scale)
        self.pos_player_hp = (121 * self.scale, 104 * self.scale)
        
        self.pos_player_anim_base = (60 * self.scale, 108 * self.scale)
        
        self.load_assets()
        
        # Estados: "INTRO", "TEXT_DISPLAY", "ANIM_PLAYER_THROW", "SELECT_ACTION", "SELECT_MOVE", "EXECUTE_TURN", "SWITCHING", "SWITCHING_FORCED", "END"
        self.state = "INTRO"
        self.text_queue = [
            "¡El Rival BRENDAN quiere luchar!",
            f"¡BRENDAN envió a {self.enemy_pkmn.name.upper()}!",
            f"¡Ve! ¡{self.player_pkmn.name.upper()}!"
        ]
        self.current_text = ""
        self.menu_cursor = 0
        self.turn_queue = []
        self.battle_result = None
        
        # Variables para la Animación
        self.show_enemy_pkmn = False
        self.show_player_pkmn = False
        self.show_player_trainer = True
        self.show_pokeball = False
        
        self.anim_timer = 0
        self.anim_frame = 0
        self.player_anim_x = self.pos_player_anim_base[0]
        self.pokeball_x = 0
        self.pokeball_y = 0
        self.pokeball_angle = 0
        self.flash_frames = 0
        
        self.advance_text()

    def load_assets(self):
        # Aumentar la fuente a 40px
        try:
            self.font = pygame.font.Font("assets/fonts/pokemon_fire_red.ttf", 40)
        except Exception:
            self.font = pygame.font.SysFont("Arial", 40)
            
        try:
            bg_raw = pygame.image.load("assets/backgrounds/bg_grass.png").convert()
            self.bg_image = pygame.transform.scale(bg_raw, (self.screen.get_width(), self.screen.get_height()))
        except Exception:
            self.bg_image = pygame.Surface((960, 640))
            self.bg_image.fill((112, 192, 112))
            
        try:
            self.ui_sheet = pygame.image.load("assets/ui/battle_ui.png").convert_alpha()
            self.ui_sheet.set_colorkey((255, 255, 255))
        except Exception:
            self.ui_sheet = pygame.Surface((600, 200), pygame.SRCALPHA)
            
        ui_rects = {
            "health_enemy": (2, 2, 102, 31),
            "health_player": (2, 43, 106, 39),
            "menu_choice": (145, 3, 122, 50),
            "menu_arrow": (268, 2, 7, 12),
            "menu_moves": (296, 3, 242, 50),
            "text_box": (296, 55, 242, 50),
            "arrow_narracion": (543, 57, 12, 9)
        }

        self.ui_elements = {}
        for name, rect in ui_rects.items():
            self.ui_elements[name] = self.extract_and_scale(self.ui_sheet, rect)
            
        # Cargar animación del jugador
        self.player_frames = []
        try:
            p_sheet = pygame.image.load("assets/sprites/player/player_spritesheet.png").convert_alpha()
            p_sheet.set_colorkey((255, 166, 166))
            rects = [
                (9, 967, 64, 64), (73, 967, 64, 64), (137, 967, 65, 64), 
                (202, 967, 66, 64), (268, 967, 63, 64)
            ]
            for r in rects:
                sub = p_sheet.subsurface(pygame.Rect(r)).copy()
                sub = pygame.transform.scale(sub, (r[2] * self.scale, r[3] * self.scale))
                self.player_frames.append(sub)
        except Exception as e:
            print(f"Error cargando animación del jugador: {e}")
            fallback = pygame.Surface((64 * self.scale, 64 * self.scale), pygame.SRCALPHA)
            fallback.fill((0, 0, 255, 128))
            self.player_frames = [fallback] * 5
            
        # Cargar Pokébola
        try:
            pb_sheet = pygame.image.load("assets/sprites/pokemon/pokeballs.png").convert_alpha()
            pb_sheet.set_colorkey((255, 166, 166))
            pb_sub = pb_sheet.subsurface(pygame.Rect(32, 20, 16, 17)).copy()
            self.pokeball_img = pygame.transform.scale(pb_sub, (16 * self.scale, 17 * self.scale))
        except Exception:
            self.pokeball_img = pygame.Surface((16 * self.scale, 17 * self.scale), pygame.SRCALPHA)
            pygame.draw.circle(self.pokeball_img, (255, 0, 0), (8 * self.scale, 8 * self.scale), 8 * self.scale)

        self.sprite_cache = {}
        for pk in self.player_team + self.enemy_team:
            self.get_or_cache_sprite(pk.name, pk.pokemon_id, is_ally=(not pk.is_enemy))

    def extract_and_scale(self, sheet, rect_tuple):
        rect = pygame.Rect(rect_tuple)
        if rect.right > sheet.get_width() or rect.bottom > sheet.get_height():
            fallback = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            return pygame.transform.scale(fallback, (rect.width * self.scale, rect.height * self.scale))
            
        sub_surface = sheet.subsurface(rect).copy()
        # Asegurar transparencia blanca de UI
        sub_surface.set_colorkey((255, 255, 255))
        return pygame.transform.scale(sub_surface, (rect.width * self.scale, rect.height * self.scale))

    def get_or_cache_sprite(self, name, pk_id, is_ally):
        cache_key = f"{name}_{'ally' if is_ally else 'enemy'}"
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]
            
        side = "ally" if is_ally else "enemy"
        try:
            filename = f"assets/sprites/pokemon/extracted/{int(pk_id):03d}_{side}.png"
            raw_sprite = pygame.image.load(filename).convert_alpha()
            sprite = pygame.transform.scale(raw_sprite, (raw_sprite.get_width() * self.scale, raw_sprite.get_height() * self.scale))
        except Exception as e:
            sprite = pygame.Surface((65 * self.scale, 65 * self.scale), pygame.SRCALPHA)
            
        self.sprite_cache[cache_key] = sprite
        return sprite

    def advance_text(self):
        if self.text_queue:
            self.current_text = self.text_queue.pop(0)
            self.state = "TEXT_DISPLAY"
            if "envió a" in self.current_text:
                self.show_enemy_pkmn = True
        else:
            self.current_text = ""
            if self.battle_result:
                self.state = "END"
            elif self.player_pkmn.fainted:
                self.state = "SWITCHING_FORCED"
                self.menu_cursor = 0
            elif self.enemy_pkmn.fainted:
                self.handle_enemy_faint_switch()
            else:
                if not self.show_player_pkmn:
                    # Iniciar secuencia de lanzamiento si el pokemon no está en pantalla
                    self.state = "ANIM_PLAYER_THROW"
                    self.anim_timer = 0
                    self.anim_frame = 0
                    self.player_anim_x = self.pos_player_anim_base[0]
                else:
                    self.state = "SELECT_ACTION"
                    self.menu_cursor = 0

    def handle_enemy_faint_switch(self):
        alive_enemies = [p for p in self.enemy_team if not p.fainted]
        if alive_enemies:
            self.enemy_pkmn = alive_enemies[0]
            self.text_queue.append(f"¡BRENDAN envió a {self.enemy_pkmn.name.upper()}!")
            self.advance_text()
        else:
            self.text_queue.append("¡Derrotaste al Rival BRENDAN!")
            self.battle_result = "VICTORY"
            self.advance_text()

    def update(self):
        if self.state == "ANIM_PLAYER_THROW":
            self.anim_timer += 1
            
            # Cambiar cuadro cada 6 ticks
            if self.anim_timer % 6 == 0 and self.anim_frame < 4:
                self.anim_frame += 1
                
            # Desplazar al jugador a la izquierda después de lanzar
            if self.anim_frame >= 2:
                self.player_anim_x -= 8 * self.scale
                
            # Física de la Pokébola
            if self.anim_frame >= 2 and self.anim_timer < 45:
                self.show_pokeball = True
                
                # Progreso de 0.0 a 1.0
                progress = (self.anim_timer - 12) / 33.0
                progress = max(0, min(1, progress))
                
                start_x, start_y = self.pos_player_anim_base[0], self.pos_player_anim_base[1] - (30 * self.scale)
                target_x, target_y = self.pos_player_pkmn[0] + (32 * self.scale), self.pos_player_pkmn[1] + (32 * self.scale)
                
                self.pokeball_x = start_x + (target_x - start_x) * progress
                self.pokeball_y = start_y + (target_y - start_y) * progress
                
                # Parábola (Arco)
                self.pokeball_y -= (1 - (progress - 0.5)**2 * 4) * 40 * self.scale
                self.pokeball_angle += 25
            else:
                self.show_pokeball = False
                
            # Eventos en tiempos específicos
            if self.anim_timer == 45:
                self.flash_frames = 4 # Pantallazo blanco
                
            if self.anim_timer == 48:
                self.show_player_trainer = False
                self.show_player_pkmn = True
                
            if self.anim_timer > 60:
                self.state = "SELECT_ACTION"
                self.menu_cursor = 0
                if self.turn_queue:
                    self.state = "EXECUTE_TURN"

        elif self.state == "EXECUTE_TURN":
            if not self.turn_queue:
                self.check_faint()
            else:
                action = self.turn_queue.pop(0)
                attacker = action['attacker']
                defender = action['defender']
                move = action['move']
                
                if attacker.fainted:
                    self.update()
                    return
                    
                damage = attacker.calculate_damage(move, defender)
                defender.take_damage(damage)
                
                self.text_queue.append(f"¡{attacker.name.upper()} usó {move.name.upper()}!")
                if damage > 0:
                    self.text_queue.append(f"¡Hizo {damage} de daño!")
                self.advance_text()

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return
            
        if self.state == "TEXT_DISPLAY":
            if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_z]:
                self.advance_text()
                
        elif self.state == "SELECT_ACTION":
            if event.key == pygame.K_RIGHT: self.menu_cursor = (self.menu_cursor + 1) % 4
            elif event.key == pygame.K_LEFT: self.menu_cursor = (self.menu_cursor - 1) % 4
            elif event.key == pygame.K_DOWN: self.menu_cursor = (self.menu_cursor + 2) % 4
            elif event.key == pygame.K_UP: self.menu_cursor = (self.menu_cursor - 2) % 4
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_z]:
                if self.menu_cursor == 0:  # LUCHAR
                    self.state = "SELECT_MOVE"
                    self.menu_cursor = 0
                elif self.menu_cursor == 2:  # POKEMON
                    self.state = "SWITCHING"
                    self.menu_cursor = 0
                elif self.menu_cursor == 1:  # MOCHILA
                    self.text_queue.append("¡OPCIÓN EN CONSTRUCCIÓN!")
                    self.advance_text()
                elif self.menu_cursor == 3:  # HUIR
                    self.text_queue.append("¡NO PUEDES HUIR DE UN JEFE!")
                    self.advance_text()
                    
        elif self.state == "SELECT_MOVE":
            if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_x]:
                self.state = "SELECT_ACTION"
                self.menu_cursor = 0
            elif event.key == pygame.K_RIGHT: self.menu_cursor = min(self.menu_cursor + 1, len(self.player_pkmn.moves) - 1)
            elif event.key == pygame.K_LEFT: self.menu_cursor = max(self.menu_cursor - 1, 0)
            elif event.key == pygame.K_DOWN: self.menu_cursor = min(self.menu_cursor + 2, len(self.player_pkmn.moves) - 1)
            elif event.key == pygame.K_UP: self.menu_cursor = max(self.menu_cursor - 2, 0)
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_z]:
                player_move = self.player_pkmn.moves[self.menu_cursor]
                self.queue_battle_round(player_move)
                
        elif self.state in ["SWITCHING", "SWITCHING_FORCED"]:
            if event.key == pygame.K_RIGHT: self.menu_cursor = min(self.menu_cursor + 1, len(self.player_team) - 1)
            elif event.key == pygame.K_LEFT: self.menu_cursor = max(self.menu_cursor - 1, 0)
            elif event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE, pygame.K_x] and self.state == "SWITCHING":
                self.state = "SELECT_ACTION"
                self.menu_cursor = 0
            elif event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_z]:
                selected_pkmn = self.player_team[self.menu_cursor]
                if selected_pkmn.fainted:
                    return
                if selected_pkmn == self.player_pkmn:
                    return
                    
                is_forced = (self.state == "SWITCHING_FORCED")
                self.player_pkmn = selected_pkmn
                self.text_queue.append(f"¡Ve! ¡{self.player_pkmn.name.upper()}!")
                
                # Resetear banderas para volver a ejecutar la animación de lanzar
                self.show_player_pkmn = False
                self.show_player_trainer = True
                
                if not is_forced:
                    enemy_move = random.choice(self.enemy_pkmn.moves)
                    self.turn_queue = [{'attacker': self.enemy_pkmn, 'defender': self.player_pkmn, 'move': enemy_move}]
                    
                self.advance_text()

    def queue_battle_round(self, player_move):
        enemy_move = random.choice(self.enemy_pkmn.moves)
        
        if self.player_pkmn.speed >= self.enemy_pkmn.speed:
            self.turn_queue = [
                {'attacker': self.player_pkmn, 'defender': self.enemy_pkmn, 'move': player_move},
                {'attacker': self.enemy_pkmn, 'defender': self.player_pkmn, 'move': enemy_move}
            ]
        else:
            self.turn_queue = [
                {'attacker': self.enemy_pkmn, 'defender': self.player_pkmn, 'move': enemy_move},
                {'attacker': self.player_pkmn, 'defender': self.enemy_pkmn, 'move': player_move}
            ]
        self.state = "EXECUTE_TURN"
        self.update()

    def check_faint(self):
        if self.enemy_pkmn.fainted:
            self.text_queue.append(f"¡{self.enemy_pkmn.name.upper()} enemigo se debilitó!")
        if self.player_pkmn.fainted:
            self.text_queue.append(f"¡{self.player_pkmn.name.upper()} se debilitó!")
            
        alive_players = [p for p in self.player_team if not p.fainted]
        if not alive_players and self.player_pkmn.fainted:
            self.text_queue.append("¡No te quedan Pokémon!")
            self.battle_result = "DEFEAT"
            
        self.advance_text()

    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        
        if self.show_enemy_pkmn and not self.enemy_pkmn.fainted:
            enemy_sprite = self.get_or_cache_sprite(self.enemy_pkmn.name, self.enemy_pkmn.pokemon_id, is_ally=False)
            self.screen.blit(enemy_sprite, self.pos_enemy_pkmn)
            self.draw_hp_bar("enemy")
            
        if self.show_player_pkmn and not self.player_pkmn.fainted:
            player_sprite = self.get_or_cache_sprite(self.player_pkmn.name, self.player_pkmn.pokemon_id, is_ally=True)
            self.screen.blit(player_sprite, self.pos_player_pkmn)
            self.draw_hp_bar("player")
            
        if self.show_player_trainer:
            frame = self.player_frames[self.anim_frame]
            # Alineación para que los pies queden en la misma Y
            self.screen.blit(frame, (self.player_anim_x, self.pos_player_anim_base[1] - frame.get_height() + (20 * self.scale)))
            
        if self.show_pokeball:
            rotated_pb = pygame.transform.rotate(self.pokeball_img, self.pokeball_angle)
            pb_rect = rotated_pb.get_rect(center=(self.pokeball_x, self.pokeball_y))
            self.screen.blit(rotated_pb, pb_rect)
            
        self.draw_bottom_hud()
        
        # Efecto de Flash
        if self.flash_frames > 0:
            flash_surf = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
            flash_surf.fill((255, 255, 255))
            self.screen.blit(flash_surf, (0, 0))
            self.flash_frames -= 1

    def draw_hp_bar(self, target):
        if target == "enemy":
            pk = self.enemy_pkmn
            pos = self.pos_enemy_hp
            ui_element = self.ui_elements["health_enemy"]
            self.screen.blit(ui_element, pos)
            
            name_surf = self.font.render(pk.name.upper(), True, (60, 60, 60))
            level_surf = self.font.render(f"L{pk.level}", True, (60, 60, 60))
            self.screen.blit(name_surf, (pos[0] + 8 * self.scale, pos[1] + 2 * self.scale))
            self.screen.blit(level_surf, (pos[0] + 72 * self.scale, pos[1] + 2 * self.scale))
            
            ratio = pk.get_hp_ratio()
            fill_w = int(48 * ratio * self.scale)
            color = (88, 208, 128) if ratio > 0.5 else (240, 192, 48) if ratio > 0.2 else (240, 80, 48)
            if fill_w > 0:
                pygame.draw.rect(self.screen, color, (pos[0] + 39 * self.scale, pos[1] + 17 * self.scale, fill_w, 3 * self.scale))
                
        else: # player
            pk = self.player_pkmn
            pos = self.pos_player_hp
            ui_element = self.ui_elements["health_player"]
            self.screen.blit(ui_element, pos)
            
            name_surf = self.font.render(pk.name.upper(), True, (60, 60, 60))
            level_surf = self.font.render(f"L{pk.level}", True, (60, 60, 60))
            hp_text = self.font.render(f"{pk.hp}/{pk.max_hp}", True, (60, 60, 60))
            
            self.screen.blit(name_surf, (pos[0] + 16 * self.scale, pos[1] + 2 * self.scale))
            self.screen.blit(level_surf, (pos[0] + 83 * self.scale, pos[1] + 2 * self.scale))
            self.screen.blit(hp_text, (pos[0] + 55 * self.scale, pos[1] + 18 * self.scale))
            
            ratio = pk.get_hp_ratio()
            fill_w = int(48 * ratio * self.scale)
            color = (88, 208, 128) if ratio > 0.5 else (240, 192, 48) if ratio > 0.2 else (240, 80, 48)
            if fill_w > 0:
                pygame.draw.rect(self.screen, color, (pos[0] + 48 * self.scale, pos[1] + 17 * self.scale, fill_w, 3 * self.scale))

    def draw_bottom_hud(self):
        if self.state in ["TEXT_DISPLAY", "INTRO", "EXECUTE_TURN", "ANIM_PLAYER_THROW"]:
            self.screen.blit(self.ui_elements["text_box"], (0, self.bottom_y))
            text_surf = self.font.render(self.current_text, True, (255, 255, 255))
            self.screen.blit(text_surf, (15 * self.scale, self.bottom_y + 10 * self.scale))
            
            if (len(self.text_queue) > 0 or self.state == "TEXT_DISPLAY") and self.state != "ANIM_PLAYER_THROW":
                if (pygame.time.get_ticks() // 400) % 2 == 0:
                    self.screen.blit(self.ui_elements["arrow_narracion"], (225 * self.scale, self.bottom_y + 35 * self.scale))
                    
        elif self.state == "SELECT_ACTION":
            self.screen.blit(self.ui_elements["text_box"], (0, self.bottom_y))
            menu_x = self.screen.get_width() - self.ui_elements["menu_choice"].get_width()
            self.screen.blit(self.ui_elements["menu_choice"], (menu_x, self.bottom_y))
            
            prompt_surf = self.font.render(f"¿Qué hará", True, (255, 255, 255))
            prompt_surf2 = self.font.render(f"{self.player_pkmn.name.upper()}?", True, (255, 255, 255))
            self.screen.blit(prompt_surf, (15 * self.scale, self.bottom_y + 4 * self.scale))
            self.screen.blit(prompt_surf2, (15 * self.scale, self.bottom_y + 24 * self.scale))
            
            cursor_pts = [
                (menu_x + 9 * self.scale, self.bottom_y + 13 * self.scale),
                (menu_x + 65 * self.scale, self.bottom_y + 13 * self.scale),
                (menu_x + 9 * self.scale, self.bottom_y + 31 * self.scale),
                (menu_x + 65 * self.scale, self.bottom_y + 31 * self.scale)
            ]
            self.screen.blit(self.ui_elements["menu_arrow"], cursor_pts[self.menu_cursor])
            
        elif self.state == "SELECT_MOVE":
            self.screen.blit(self.ui_elements["menu_moves"], (0, self.bottom_y))
            
            for i, mv in enumerate(self.player_pkmn.moves):
                col = i % 2
                row = i // 2
                m_x = 22 * self.scale + col * 95 * self.scale
                m_y = self.bottom_y + 10 * self.scale + row * 18 * self.scale
                text_s = self.font.render(mv.name.upper(), True, (60, 60, 60))
                self.screen.blit(text_s, (m_x, m_y))
                
            c_col = self.menu_cursor % 2
            c_row = self.menu_cursor // 2
            a_x = 10 * self.scale + c_col * 95 * self.scale
            a_y = self.bottom_y + 12 * self.scale + c_row * 18 * self.scale
            self.screen.blit(self.ui_elements["menu_arrow"], (a_x, a_y))
            
        elif self.state in ["SWITCHING", "SWITCHING_FORCED"]:
            self.screen.blit(self.ui_elements["text_box"], (0, self.bottom_y))
            title_s = self.font.render("ELIGE UN POKÉMON:", True, (255, 255, 255))
            self.screen.blit(title_s, (15 * self.scale, self.bottom_y + 6 * self.scale))
            
            for i, pk in enumerate(self.player_team):
                x = 15 * self.scale + i * 38 * self.scale
                y = self.bottom_y + 24 * self.scale
                
                color = (255, 215, 0) if i == self.menu_cursor else (160, 160, 160) if pk.fainted else (255, 255, 255)
                pk_s = self.font.render(pk.name[:5].upper(), True, color)
                self.screen.blit(pk_s, (x, y))