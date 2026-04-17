"""
npcs/__init__.py — NPC Registry for The Honda Years.
"""

from npcs.radio import Radio
from npcs.sarah import Sarah
from npcs.drew import Drew
from npcs.emma import Emma


NPC_REGISTRY = {
    "radio": Radio(),
    "sarah": Sarah(),
    "drew":  Drew(),
    "emma":  Emma(),
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
    radio = NPC_REGISTRY.get("radio")
    if radio and radio.matches(word):
        return radio
    return None


def get_active_npcs(room_id, game):
    return [npc for npc in get_room_npcs(room_id) if npc.is_active(game)]
