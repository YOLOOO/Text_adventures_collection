"""
npcs/__init__.py — NPC Registry.

Key   = NPC ID (must match the strings used in rooms.py "npcs" lists)
Value = An instance of the NPC class
"""

from npcs.virgil import Virgil
from npcs.mr_chen import MrChen
from npcs.night_maid import NightMaid


NPC_REGISTRY = {
    "virgil":     Virgil(),
    "mr_chen":    MrChen(),
    "night_maid": NightMaid(),
}


def get_npc(npc_id):
    return NPC_REGISTRY.get(npc_id)


def get_room_npcs(room_id):
    from data.rooms import ROOMS
    room = ROOMS.get(room_id, {})
    npc_ids = room.get("npcs", [])
    return [NPC_REGISTRY[nid] for nid in npc_ids if nid in NPC_REGISTRY]


def find_npc_by_alias(room_id, word):
    for npc in get_room_npcs(room_id):
        if npc.matches(word):
            return npc
    # VIRGIL is accessible everywhere via intercom
    virgil = NPC_REGISTRY.get("virgil")
    if virgil and virgil.matches(word):
        return virgil
    return None


def get_active_npcs(room_id, game):
    return [npc for npc in get_room_npcs(room_id) if npc.is_active(game)]
