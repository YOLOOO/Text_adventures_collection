"""
game.py — Core game state.

Holds the player's HP, inventory, room, flags, and turn counter.
All game state lives here so it can be passed around cleanly.
"""

from engine.display import danger, success, hr, dragon_says


class Game:
    def __init__(self):
        self.hp = 30
        self.max_hp = 30
        self.inventory = []
        self.room = "intern_quarters"
        self.turns = 0
        self.rooms_visited = set()
        self.game_over = False
        self.won = False
        self.ending = ""

        # Flags track story progress. Any system can read/write these.
        # Add new flags here as you add content.
        self.flags = {
            "wand_charged": False,
            "ghost_appeased": False,
            "goblins_befriended": False,
            "goblins_defeated": False,
            "crystal_obtained": False,
            "hyperdrive_fixed": False,
            "dracos_met": False,
            "goblin_king_alive": True,
            "spoke_to_ghost": False,
            "turret_disabled": False,
            "looked_out_window": False,
            "cafeteria_cleared": False,
        }

    # ─── Helpers ──────────────────────────────────────────────────────────

    def has(self, item):
        """Check if player has an item in inventory."""
        return item in self.inventory

    def set_flag(self, flag, value=True):
        """Set a story flag."""
        self.flags[flag] = value

    def check_flag(self, flag):
        """Read a story flag (defaults to False if missing)."""
        return self.flags.get(flag, False)

    def add_item(self, item_id):
        """Add an item to inventory."""
        self.inventory.append(item_id)

    def remove_item(self, item_id):
        """Remove an item from inventory (safe — no error if missing)."""
        if item_id in self.inventory:
            self.inventory.remove(item_id)

    # ─── HP Management ────────────────────────────────────────────────────

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        danger(f"You take {amount} damage! HP: {self.hp}/{self.max_hp}")
        if self.hp <= 0:
            self.die()

    def heal(self, amount):
        old = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        healed = self.hp - old
        if healed > 0:
            success(f"You heal {healed} HP! HP: {self.hp}/{self.max_hp}")

    def die(self):
        print()
        hr()
        danger("YOU HAVE DIED.")
        dragon_says(
            "Well, that was embarrassing. Your corpse will float through space "
            "for eternity, which is kind of poetic if you think about it. "
            "Which you can't. Because you're dead."
        )
        hr()
        self.game_over = True

    # ─── Display ──────────────────────────────────────────────────────────

    def status_bar(self):
        from engine.display import C
        from data.rooms import ROOMS
        from npcs import get_active_npcs
        room_name = ROOMS[self.room]["name"]
        npcs = [npc for npc in get_active_npcs(self.room, self) if npc.id != "dracos"]
        npc_part = " | " + ", ".join(npc.name for npc in npcs) if npcs else ""
        print(f"\n  {C.DIM}HP:{self.hp}/{self.max_hp} | T:{self.turns} | {room_name}{npc_part}{C.RESET}")
