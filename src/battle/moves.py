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
