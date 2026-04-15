"""
game.py — Core game state for Route 7.
"""

from engine.display import danger, success, hr, dispatch_says


class Game:
    def __init__(self):
        self.hp = 20
        self.max_hp = 20
        self.inventory = []
        self.room = "rear_seats"
        self.turns = 0
        self.rooms_visited = set()
        self.game_over = False
        self.won = False
        self.ending = ""

        self.flags = {
            # Discovery
            "newspaper_read":      False,
            "map_read":            False,
            "log_read":            False,
            # NPC states
            "rosa_met":            False,
            "rosa_told_truth":     False,
            "rosa_gave_report":    False,
            "driver_looked":       False,
            "dispatch_confronted": False,
            # Progress
            "hatch_open":          False,
            "lever_pulled":        False,
            "cab_unlocked":        False,
            # Escape
            "escape_via_rear":     False,
            "escape_via_cab":      False,
        }

    # ─── Helpers ──────────────────────────────────────────────────────────

    def has(self, item):
        return item in self.inventory

    def set_flag(self, flag, value=True):
        self.flags[flag] = value

    def check_flag(self, flag):
        return self.flags.get(flag, False)

    def add_item(self, item_id):
        self.inventory.append(item_id)

    def remove_item(self, item_id):
        if item_id in self.inventory:
            self.inventory.remove(item_id)

    # ─── HP Management ────────────────────────────────────────────────────

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        danger(f"You take {amount} damage. HP: {self.hp}/{self.max_hp}")
        if self.hp <= 0:
            self.die()

    def heal(self, amount):
        old = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        healed = self.hp - old
        if healed > 0:
            success(f"HP restored. HP: {self.hp}/{self.max_hp}")

    def die(self):
        print()
        hr()
        danger("YOU HAVE COLLAPSED.")
        dispatch_says(
            "Passenger down on Route 7. "
            "Please remain in your seat. "
            "End of Line approaching."
        )
        hr()
        self.game_over = True

    # ─── Time Display ─────────────────────────────────────────────────────

    def bus_time(self):
        """Current in-game clock. Starts 11:47 PM, 1 min per turn."""
        start_min = 23 * 60 + 47   # 11:47 PM in minutes
        current   = start_min + self.turns
        hour      = (current // 60) % 24
        minute    = current % 60
        period    = "AM" if hour < 12 else "PM"
        hour12    = hour % 12 or 12
        return f"{hour12}:{minute:02d} {period}"

    # ─── Display ──────────────────────────────────────────────────────────

    def status_bar(self):
        from engine.display import C
        from data.rooms import ROOMS
        from npcs import get_active_npcs
        from data.endings import TURN_LIMIT
        room_name = ROOMS[self.room]["name"]
        npcs = [n for n in get_active_npcs(self.room, self) if n.id != "dispatch"]
        npc_part = " | " + ", ".join(n.name for n in npcs) if npcs else ""
        turns_left = TURN_LIMIT - self.turns
        print(f"\n  {C.DIM}HP:{self.hp}/{self.max_hp} | "
              f"{self.bus_time()} | -{turns_left}t | "
              f"{room_name}{npc_part}{C.RESET}")
