"""
virgil.py — VIRGIL, the Hotel Midnight concierge AI.

VIRGIL is the hotel's integrated management system. Smooth,
over-formal, subtly menacing. Speaks via intercoms in every room.
Knows far more than it admits. Analog to DRACOS.
"""

from npcs.base import NPC
from engine.display import virgil_says, dim


class Virgil(NPC):
    id = "virgil"
    name = "VIRGIL"
    aliases = ["virgil", "concierge", "intercom", "hotel", "ai", "speaker"]

    DIALOG = {
        "greeting": [
            "Good evening. I am VIRGIL, Hotel Midnight's management system. "
            "I'm afraid the floor is temporarily restricted. "
            "Please remain calm and return to your room.",
        ],
        "hallway_intro": [
            "I notice you've left your room. "
            "For your safety, I'd encourage you to reconsider.",
        ],
        "lounge_intro": [
            "The lounge is closed at this hour. "
            "Help yourself to whatever you find. "
            "It won't matter shortly.",
        ],
        "office_intro": [
            "The manager is unavailable. His absence is... unrelated "
            "to tonight's events. Mostly.",
        ],
        "north_corridor_intro": [
            "Room 316 is a restricted area. I must insist. "
            "The police tape is not decorative.",
        ],
        "room_316_intro": [
            "You've gained access to Room 316. "
            "I'm logging this for the record.",
        ],
        "stairwell_intro": [
            "The fire exit. You've been thorough, I'll grant you that. "
            "I hope whatever you found was worth the trouble.",
        ],
        # Item reactions
        "piano_key_taken": [
            "Ah. You found that. "
            "I'd wondered who wrote that note.",
        ],
        "keycard_used": [
            "Master keycard accepted. Room 316 is now accessible. "
            "I do hope you're prepared for what's inside.",
        ],
        "shard_crit": [
            "Improvised. Unorthodox. Effective. "
            "I'm making a note.",
        ],
        # Confrontation
        "confronted_with_glass": [
            "An interesting piece of evidence. "
            "I'm afraid fingerprints require a laboratory to be admissible.",
        ],
        "confronted_with_ledger": [
            "The guest register. Yes. I did make those notations. "
            "Hotel policy requires accurate record-keeping.",
        ],
        # Turn warnings — 4 AM approaches
        "time_warning_48": [
            "A small reminder: the lobby opens to staff in 32 minutes. "
            "I'd suggest concluding your... activities.",
        ],
        "time_warning_64": [
            "Sixteen minutes, if my clock is accurate. "
            "It is always accurate.",
        ],
        "time_warning_79": [
            "One minute. Whatever you intend, "
            "I suggest you do it now.",
        ],
        # Generic
        "quit": [
            "Leaving so soon? I'll have housekeeping prepare the room.",
        ],
        "generic": [
            "I'm afraid I can't help you with that.",
            "Hotel policy prevents me from commenting.",
            "That falls outside my operational parameters.",
        ],
    }

    def get_line(self, context, index=0):
        lines = self.DIALOG.get(context, self.DIALOG["generic"])
        return lines[index % len(lines)]

    def say(self, context, index=0):
        line = self.get_line(context, index)
        if line:
            virgil_says(line)

    # ─── NPC Interface ────────────────────────────────────────────────────

    def talk(self, game):
        if game.has("guest_ledger") and not game.check_flag("confronted_virgil"):
            virgil_says(self.get_line("confronted_with_ledger"))
            game.set_flag("confronted_virgil")
        elif game.has("whiskey_glass"):
            virgil_says(self.get_line("confronted_with_glass"))
        else:
            # Generic contextual response
            context_map = {
                "room_314":       "greeting",
                "hallway":        "hallway_intro",
                "lounge":         "lounge_intro",
                "managers_office": "office_intro",
                "north_corridor": "north_corridor_intro",
                "stairwell":      "stairwell_intro",
            }
            context = context_map.get(game.room, "generic")
            virgil_says(self.get_line(context))
        return True

    def use_item(self, game, item_id):
        if item_id == "whiskey_glass":
            if not game.check_flag("confronted_virgil"):
                virgil_says(self.get_line("confronted_with_glass"))
                game.set_flag("confronted_virgil")
            else:
                dim("VIRGIL has already acknowledged the glass.")
            return True
        if item_id == "guest_ledger":
            virgil_says(self.get_line("confronted_with_ledger"))
            return True
        return False

    def look(self, game):
        dim(
            "VIRGIL is everywhere — the intercoms, the locks, "
            "the elevator panel. An invisible presence that "
            "knows exactly where you are."
        )
        return True

    def describe(self, game, first_visit):
        pass  # VIRGIL speaks contextually, not on room entry
