"""
game.py — Core game state for Hotel Midnight.
"""

import random
from engine.display import danger, success, hr, virgil_says


class Game:
    def __init__(self):
        self.hp = 15          # Already injured when you wake up
        self.max_hp = 20
        self.inventory = []
        self.room = "room_314"
        self.turns = 0
        self.rooms_visited = set()
        self.game_over = False
        self.won = False
        self.ending = ""

        self.flags = {
            # Progress
            "piano_key_found":    False,
            "room_316_unlocked":  False,
            "box_opened":         False,
            "ledger_read":        False,
            # NPC states
            "chen_helped":        False,
            "maid_found":         False,
            "maid_talked":        False,
            "virgil_met":         False,
            "confronted_virgil":  False,
            # Evidence
            "whiskey_identified": False,
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
            success(f"Patched up. HP: {self.hp}/{self.max_hp}")

    def die(self):
        print()
        hr()
        danger("YOU HAVE COLLAPSED.")
        virgil_says(
            "Medical assistance has been called. "
            "Please remain where you are."
        )
        hr()
        self.game_over = True

    # ─── Display ──────────────────────────────────────────────────────────

    def status_bar(self):
        from engine.display import C
        from data.rooms import ROOMS
        from npcs import get_active_npcs
        from data.endings import TURN_LIMIT
        room_name = ROOMS[self.room]["name"]
        npcs = [n for n in get_active_npcs(self.room, self) if n.id != "virgil"]
        npc_part = " | " + ", ".join(n.name for n in npcs) if npcs else ""
        print(f"\n  {C.DIM}HP:{self.hp}/{self.max_hp} | "
              f"T:{self.turns}/{TURN_LIMIT} | {room_name}{npc_part}{C.RESET}")
