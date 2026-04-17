"""
game.py — Core game state for The Honda Years.

HP is repurposed as Connection health — a measure of how open
Mike and Sarah are being with each other. Starts at 10/20.
Honest choices raise it; deflections lower it.
"""

from engine.display import danger, success, hr


class Game:
    def __init__(self):
        self.hp = 10           # Connection health
        self.max_hp = 20
        self.inventory = []
        self.room = "front_seat"
        self.turns = 0
        self.rooms_visited = set()
        self.game_over = False
        self.won = False
        self.ending = ""

        self.flags = {
            # Road progress gates
            "iowa_stop_done":     False,
            "motel_night_done":   False,
            "breakdown_done":     False,
            "final_stretch_done": False,
            # Sarah arc
            "sarah_met_properly": False,
            "therapy_mentioned":  False,
            "affair_hinted":      False,
            "affair_revealed":    False,
            "sarah_cried":        False,
            "motel_fight":        False,
            "motel_talk":         False,
            # Drew arc
            "drew_spoke":         False,
            "drew_noticed":       False,
            # Emma arc
            "emma_observation":   False,
            "emma_drawing_given": False,
            "emma_drawing_read":  False,
            # Mike choices (int counters stored as ints)
            "honest_choices":     0,
            "deflect_choices":    0,
            # Item flags
            "therapy_notes_read": False,
            "gas_receipt_read":   False,
            "coffee_used":        False,
        }

    # ─── Helpers ──────────────────────────────────────────────────────────

    def has(self, item):
        return item in self.inventory

    def set_flag(self, flag, value=True):
        self.flags[flag] = value

    def check_flag(self, flag):
        return self.flags.get(flag, False)

    def add_item(self, item_id):
        if item_id not in self.inventory:
            self.inventory.append(item_id)

    def remove_item(self, item_id):
        if item_id in self.inventory:
            self.inventory.remove(item_id)

    # ─── Choice Tracking ──────────────────────────────────────────────────

    def honest(self):
        """Record an honest choice; raise connection."""
        self.flags["honest_choices"] = self.flags.get("honest_choices", 0) + 1
        self.heal(1)

    def deflect(self):
        """Record a deflection; lower connection."""
        self.flags["deflect_choices"] = self.flags.get("deflect_choices", 0) + 1
        self.take_damage(1)

    # ─── HP Management ────────────────────────────────────────────────────

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        if self.hp <= 3:
            danger(
                f"Connection: {self.hp}/{self.max_hp} — "
                "The silence is getting louder."
            )

    def heal(self, amount):
        old = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        healed = self.hp - old
        if healed > 0 and self.hp >= 14:
            success(
                f"Connection: {self.hp}/{self.max_hp} — "
                "Something might be working."
            )

    def die(self):
        self.game_over = True

    # ─── Miles Display ────────────────────────────────────────────────────

    def miles_remaining(self):
        """2100 miles total, ~28 miles per turn."""
        return max(0, 2100 - self.turns * 28)

    # ─── Status Bar ───────────────────────────────────────────────────────

    def status_bar(self):
        from engine.display import C
        from data.rooms import ROOMS
        from npcs import get_active_npcs
        from data.endings import TURN_LIMIT
        room_name = ROOMS[self.room]["name"]
        npcs = [n for n in get_active_npcs(self.room, self) if n.id != "radio"]
        npc_part = " | " + ", ".join(n.name for n in npcs) if npcs else ""
        turns_left = TURN_LIMIT - self.turns
        miles = self.miles_remaining()
        print(
            f"\n  {C.DIM}Connection:{self.hp}/{self.max_hp} | "
            f"~{miles}mi | -{turns_left}t | "
            f"{room_name}{npc_part}{C.RESET}"
        )
