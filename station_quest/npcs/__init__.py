"""
npcs/__init__.py — NPC Registry.

This is the CENTRAL MAPPING that connects NPC IDs (used in rooms.py)
to their actual NPC class instances. When you create a new NPC:

  1. Create npcs/my_npc.py with a class inheriting from NPC.
  2. Import it here.
  3. Add an instance to the NPC_REGISTRY dict.

The engine uses get_npc() and get_room_npcs() to find NPCs.
NPCs never need to know about each other — the registry handles wiring.
"""

from npcs.dracos import Dracos
from npcs.ghost_chef import GhostChef
from npcs.goblin_king import GoblinKing
from npcs.turret import Turret


# ─── THE REGISTRY ─────────────────────────────────────────────────────────────
#
#   Key   = NPC ID (must match the strings used in rooms.py "npcs" lists)
#   Value = An instance of the NPC class
#

NPC_REGISTRY = {
    "dracos":      Dracos(),
    "ghost_chef":  GhostChef(),
    "goblin_king": GoblinKing(),
    "turret":      Turret(),
}


# ─── Lookup Functions ─────────────────────────────────────────────────────────

def get_npc(npc_id):
    """Get an NPC instance by its ID. Returns None if not found."""
    return NPC_REGISTRY.get(npc_id)


def get_room_npcs(room_id):
    """
    Get all NPC instances assigned to a room.

    Args:
        room_id: The room key from rooms.py.

    Returns:
        list[NPC]: NPC instances in that room.
    """
    from data.rooms import ROOMS
    room = ROOMS.get(room_id, {})
    npc_ids = room.get("npcs", [])
    return [NPC_REGISTRY[nid] for nid in npc_ids if nid in NPC_REGISTRY]


def find_npc_by_alias(room_id, word):
    """
    Find an NPC in a room by a player-typed word.

    Args:
        room_id:  Current room.
        word:     What the player typed (e.g., "ghost", "turret").

    Returns:
        NPC instance or None.
    """
    for npc in get_room_npcs(room_id):
        if npc.matches(word):
            return npc
    # Also check DRACOS globally (it speaks from anywhere)
    dracos = NPC_REGISTRY.get("dracos")
    if dracos and dracos.matches(word):
        return dracos
    return None


def get_active_npcs(room_id, game):
    """Get NPCs that are currently active (not defeated/appeased) in a room."""
    return [npc for npc in get_room_npcs(room_id) if npc.is_active(game)]
