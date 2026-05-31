import random

class Pokemon:
    def __init__(self, pokemon_id, json_data, level, move_objects, is_enemy=False):
        self.pokemon_id = str(pokemon_id)
        self.name = json_data.get("name", "MissingNo.")
        self.level = level
        self.is_enemy = is_enemy
        
        self.types = [t.upper() for t in json_data.get("types", ["NORMAL"])]
        
        self.base_exp_yield = json_data.get("base_exp_yield", 64)
        self.growth_rate = json_data.get("growth_rate", "medium")
        self.learnset = json_data.get("learnset", [])
        
        base_stats = json_data.get("base_stats", {})
        b_hp = base_stats.get("hp", 10)
        b_atk = base_stats.get("attack", 10)
        b_def = base_stats.get("defense", 10)
        b_satk = base_stats.get("special-attack", 10)
        b_sdef = base_stats.get("special-defense", 10)
        b_spd = base_stats.get("speed", 10)
        
        self.max_hp = int(((b_hp * 2) * self.level) / 100) + self.level + 10
        self.hp = self.max_hp
        
        self.attack = int(((b_atk * 2) * self.level) / 100) + 5
        self.defense = int(((b_def * 2) * self.level) / 100) + 5
        self.special_attack = int(((b_satk * 2) * self.level) / 100) + 5
        self.special_defense = int(((b_sdef * 2) * self.level) / 100) + 5
        self.speed = int(((b_spd * 2) * self.level) / 100) + 5
        
        self.moves = move_objects[:4] 
        self.fainted = False

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.fainted = True

    def calculate_damage(self, move, target):
        if move.damage_class == "status" or move.power == 0:
            return 0 
            
        level_factor = ((2 * self.level) / 5) + 2
        
        physical_types = ["NORMAL", "FIGHTING", "FLYING", "POISON", "GROUND", "ROCK", "BUG", "GHOST", "STEEL"]
        
        if move.type in physical_types:
            atk_stat = self.attack
            def_stat = target.defense
        else:
            atk_stat = self.special_attack
            def_stat = target.special_defense
            
        if def_stat == 0: def_stat = 1
        
        base_damage = ((level_factor * move.power * (atk_stat / def_stat)) / 50) + 2
        
        stab = 1.5 if move.type in self.types else 1.0
        
        random_mod = random.uniform(0.85, 1.0)
        
        total_damage = int(base_damage * stab * random_mod)
        return max(1, total_damage)

    def get_hp_percentage(self):
        return self.hp / self.max_hp

    def heal_full(self):
        self.hp = self.max_hp
        self.fainted = False
