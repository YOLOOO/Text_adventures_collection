"""
rosa.py — Rosa, front-seat passenger on Route 7.

An elderly woman in a good coat. She knows she's dead.
She's been riding Route 7 since November 1987 and has
made a kind of peace with it. She wants you to get out.
"""

from npcs.base import NPC
from engine.display import dim, info, success, alert, wrap


class Rosa(NPC):
    id = "rosa"
    name = "Rosa"
    aliases = ["rosa", "woman", "passenger", "lady", "old woman", "elderly"]

    def is_active(self, game):
        # Rosa disappears once the cab is entered (she has no reason to stay)
        return not game.check_flag("escape_via_cab")

    def describe(self, game, first_visit):
        if first_visit:
            dim(
                "An elderly woman sits in the front bench seat, "
                "hands folded in her lap. She is watching you."
            )
        else:
            dim("Rosa is in the front bench seat.")

    def talk(self, game):
        if not game.check_flag("rosa_met"):
            game.set_flag("rosa_met")
            _rosa_says(
                "You're not supposed to be here. "
                "Not like us. I can tell."
            )
            info(wrap(
                "She looks at her hands. "
                "'We've been on this bus a long time. "
                "The others don't know it anymore. "
                "I do. I think I do.'"
            ))
            dim("Talk to Rosa again. She knows more.")
            return True

        if game.has("newspaper_1987") and not game.check_flag("rosa_gave_report"):
            game.set_flag("rosa_gave_report")
            game.set_flag("rosa_told_truth")
            _rosa_says(
                "You found the paper. Good. "
                "November 14, 1987. That's the night. "
                "That's always the night."
            )
            info(wrap(
                "She reaches into her coat and produces "
                "a folded document — crisp, official. "
                "'I've had this since the inquiry. "
                "They buried it. You should have it.'"
            ))
            success("Rosa gives you the Incident Report (1987).")
            game.add_item("bus_report")
            _rosa_says(
                "There's a floor hatch in the middle section. "
                "Maintenance access. You'll find what you need there. "
                "Lighter first — it's dark."
            )
            return True

        if game.has("emergency_lever") or game.check_flag("lever_pulled"):
            _rosa_says(
                "The rear door. Yes. Jump before the road ends. "
                "It will end."
            )
            return True

        if game.has("maintenance_key") or game.check_flag("cab_unlocked"):
            _rosa_says(
                "The cab. Be ready for what you see. "
                "Don't look at him long."
            )
            alert("LEAVE from the driver's cab to force a stop.")
            return True

        # Generic lines based on progress
        if not game.has("lighter"):
            _rosa_says(
                "Check under the seat to your left. "
                "Someone left something there."
            )
        elif not game.check_flag("hatch_open"):
            _rosa_says(
                "The middle section. Floor hatch. "
                "You'll need the lighter down there."
            )
        else:
            _rosa_says(
                "You should hurry. End of Line comes faster "
                "than you think, the first time."
            )
        return True

    def fight(self, game):
        dim("She looks at you with something that might be pity.")
        dim("'That won't help either of us.'")
        return True

    def look(self, game):
        dim(
            "She looks about seventy. Good coat, sensible shoes. "
            "Her hands are very still. "
            "She doesn't cast a shadow."
        )
        return True

    def use_item(self, game, item_id):
        if item_id == "newspaper_1987" and not game.check_flag("rosa_gave_report"):
            return self.talk(game)
        if item_id == "ticket_stub":
            _rosa_says(
                "November 14, 1987. "
                "That's not a date. That's a loop."
            )
            return True
        return False


def _rosa_says(text):
    from engine.display import C, WRAP_WIDTH
    import textwrap
    filled = textwrap.fill(text, width=WRAP_WIDTH - 2, subsequent_indent="  ")
    print(f"\n  {C.MAGENTA}{C.BOLD}Rosa:{C.RESET}")
    print(f"  {C.MAGENTA}\"{filled}\"{C.RESET}")
