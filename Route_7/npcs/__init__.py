"""
npcs/__init__.py — NPC Registry for Route 7.
"""

from npcs.dispatch import Dispatch
from npcs.rosa import Rosa
from npcs.driver import Driver


NPC_REGISTRY = {
    "dispatch": Dispatch(),
    "rosa":     Rosa(),
    "driver":   Driver(),
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
    # DISPATCH is accessible everywhere via the bus PA
    dispatch = NPC_REGISTRY.get("dispatch")
    if dispatch and dispatch.matches(word):
        return dispatch
    return None


def get_active_npcs(room_id, game):
    return [npc for npc in get_room_npcs(room_id) if npc.is_active(game)]
