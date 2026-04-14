"""
base.py — Base NPC class.

Every NPC inherits from this. To create a new NPC:

  1. Create a new file in npcs/ (e.g., npcs/my_npc.py).
  2. Define a class that inherits from NPC.
  3. Override the methods you need:
       - describe(game)       → What the player sees when entering the room.
       - talk(game)           → What happens on TALK command.
       - fight(game)          → What happens on FIGHT command.
       - use_item(game, item) → What happens when player USEs an item here.
       - is_active(game)      → Is this NPC still present? (default: True)
  4. Set the class attributes: id, name, aliases.
  5. Register it in npcs/__init__.py.

The registry (npcs/__init__.py) maps NPC IDs → instances, so the engine
can look up any NPC by the ID referenced in rooms.py.
"""


class NPC:
    """Base class for all NPCs."""

    id = "base"                  # Unique ID (matches rooms.py "npcs" list)
    name = "Unknown NPC"         # Display name
    aliases = []                 # Words the player might type to target this NPC

    def is_active(self, game):
        """
        Is this NPC currently present and interactable?
        Override to gate on flags (e.g., ghost disappears after being appeased).
        """
        return True

    def describe(self, game, first_visit):
        """
        Called when the player enters or LOOKs at the room.
        Should print any NPC-specific description.
        """
        pass

    def talk(self, game):
        """Handle TALK command. Return True if the action consumed a turn."""
        from engine.display import dim
        dim(f"{self.name} has nothing to say.")
        return False

    def fight(self, game):
        """Handle FIGHT command. Return True if the action consumed a turn."""
        from engine.display import dim
        dim(f"You can't fight {self.name}.")
        return False

    def use_item(self, game, item_id):
        """
        Handle USE [item] when this NPC is the contextual target.
        Return True if the NPC handled the item, False to fall through.
        """
        return False

    def look(self, game):
        """Handle LOOK [npc_alias]. Print examination text."""
        from engine.display import dim
        dim(f"You see {self.name}. Nothing else stands out.")
        return True

    def matches(self, word):
        """Does a player-typed word match this NPC?"""
        return word in self.aliases or word == self.id or word == self.name.lower()
