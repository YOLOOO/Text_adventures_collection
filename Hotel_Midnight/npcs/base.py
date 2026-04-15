"""
base.py — Base NPC class. Identical to ISS Dragonhold.
"""


class NPC:
    id = "base"
    name = "Unknown"
    aliases = []

    def is_active(self, game):
        return True

    def describe(self, game, first_visit):
        pass

    def talk(self, game):
        from engine.display import dim
        dim(f"{self.name} has nothing to say.")
        return False

    def fight(self, game):
        from engine.display import dim
        dim(f"You can't fight {self.name}.")
        return False

    def use_item(self, game, item_id):
        return False

    def look(self, game):
        from engine.display import dim
        dim(f"You see {self.name}. Nothing else stands out.")
        return True

    def matches(self, word):
        return word in self.aliases or word == self.id or word == self.name.lower()
