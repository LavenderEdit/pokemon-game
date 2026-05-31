import json
import os

class Move:
    def __init__(self, move_id, data_dict):
        self.move_id = move_id
        self.name = data_dict.get("name", "Unknown Move")
        self.type = data_dict.get("type", "normal").upper()
        self.damage_class = data_dict.get("damage_class", "physical")
        self.pp = data_dict.get("pp", 35)
        self.current_pp = self.pp
        self.priority = data_dict.get("priority", 0)
        self.target = data_dict.get("target", "selected-pokemon")
        self.stat_changes = data_dict.get("stat_changes", [])

        power_val = data_dict.get("power")
        self.power = power_val if power_val is not None else 0

        accuracy_val = data_dict.get("accuracy")
        self.accuracy = accuracy_val if accuracy_val is not None else 0


class MoveDatabase:
    _db = {}
    _loaded = False

    @classmethod
    def load_database(cls):
        if cls._loaded:
            return
            
        path = os.path.join("data", "moves.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    cls._db = json.load(f)
            except Exception as e:
                print(f"Error cargando moves.json: {e}")
                cls._db = {}
        
        cls._loaded = True

    @classmethod
    def get_move(cls, move_id):
        cls.load_database()
        
        data_dict = cls._db.get(move_id, {})
        
        if "name" not in data_dict and data_dict:
            data_dict["name"] = move_id.capitalize()
            
        return Move(move_id=move_id, data_dict=data_dict)