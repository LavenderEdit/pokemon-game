import random
import json
import os
from src.battle.moves import MoveDatabase

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
        
        is_physical = True
        if hasattr(move, 'damage_class') and move.damage_class in ["physical", "special"]:
            is_physical = (move.damage_class == "physical")
        else:
            is_physical = (move.type in physical_types)

        if is_physical:
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

    def get_hp_ratio(self):
        return self.hp / self.max_hp

    def heal_full(self):
        self.hp = self.max_hp
        self.fainted = False


class PokemonDatabase:
    _db = {}
    _loaded = False

    @classmethod
    def load_database(cls):
        if cls._loaded:
            return
            
        path = os.path.join("data", "pokemon.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        cls._db = {str(item.get("id", i)): item for i, item in enumerate(data)}
                        for item in data:
                            if "name" in item:
                                cls._db[item["name"].lower()] = item
                    else:
                        cls._db = data
            except Exception as e:
                print(f"Error cargando pokemon.json: {e}")
                cls._db = {}
                
        cls._loaded = True

    @classmethod
    def create_pokemon(cls, identifier, level, is_enemy=False):
        cls.load_database()
        
        str_id = str(identifier).lower()
        json_data = cls._db.get(str_id, {})
        
        if not json_data:
            print(f"Advertencia: No se encontró data para {identifier}")
            json_data = {"name": str(identifier).capitalize()}

        pokemon_id = json_data.get("id", str_id)
        
        raw_moves = json_data.get("moves", ["tackle"])
        move_objects = []
        for m_id in raw_moves[:4]:
            move_objects.append(MoveDatabase.get_move(m_id))
            
        if not move_objects:
            move_objects.append(MoveDatabase.get_move("tackle"))
            
        return Pokemon(
            pokemon_id=pokemon_id,
            json_data=json_data,
            level=level,
            move_objects=move_objects,
            is_enemy=is_enemy
        )