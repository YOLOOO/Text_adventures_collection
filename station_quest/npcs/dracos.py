"""
dracos.py — DRACOS, the station's AI dragon.

DRACOS is unique: it's not a room-bound NPC you fight.
It's the narrator, hint system, and comic relief.
Its dialog is organized by context so it's easy to expand.
"""

from npcs.base import NPC
from engine.display import dragon_says, dim


class Dracos(NPC):
    id = "dracos"
    name = "DRACOS"
    aliases = ["dracos", "dragon", "ai", "computer"]

    # ─── Dialog Bank ──────────────────────────────────────────────────────
    # Organized by trigger context. Add new lines to any category.

    DIALOG = {
        "greeting": [
            "Ah, you're awake. I am DRACOS, the station's Distributed Recursive "
            "Arcane Computing Operating System. I am also a dragon. Do not question this.",
        ],
        "bridge_intro": [
            "Welcome to MY bridge. I am the captain, the navigator, "
            "and the entertainment system. We will crash into Planet Fromage "
            "in approximately 'not long'. Fix the hyperdrive.",
        ],
        "bridge_talk": [
            "Yes, hello. What do you want? Status update: still crashing. "
            "Fix the hyperdrive. It needs a crystal from the Crystal Chamber. "
            "Through the Airlock. Simple. For someone competent.",
        ],
        "corridor_intro": [
            "This corridor has claimed 47 interns. You are intern #48. No pressure.",
        ],
        "cafeteria_intro": [
            "That's Chef Pierre. He died in a fondue accident. He's still bitter about it.",
        ],
        "engineering_intro": [
            "Ah, Engineering. Where dreams go to catch fire. Sometimes literally.",
        ],
        "armory_intro": [
            "I should mention you are Level 2. Most of these weapons "
            "would vaporize your hands. Stick to the cracked case.",
        ],
        "airlock_intro": [
            "The goblins arrived two weeks ago. They've been eating the hull insulation "
            "and leaving reviews on Yelp. One star. Very rude.",
        ],
        "cargo_hold_intro": [
            "The goblins moved in, redecorated, and filed for squatter's rights. "
            "I'd remove them myself but I don't have arms. On account of being software.",
        ],
        "escape_pod": [
            "Oh, the escape pods. You COULD leave. Abandon the station. Abandon ME. "
            "I wouldn't be hurt. I'm software. Software doesn't have feelings. "
            "...I have feelings.",
        ],
        # Combat commentary
        "turret_destroyed": [
            "Well done. The armory is now accessible. Try not to break anything.",
        ],
        "ghost_defeated_fight": [
            "You destroyed a culinary ghost. Food quality somehow got worse.",
        ],
        "ghost_appeased": [
            "He died in fondue and found peace in fondue. Poetic.",
        ],
        "goblins_defeated": [
            "The goblin menace is dealt with. Through violence. Traditional.",
        ],
        "goblins_befriended": [
            "You befriended goblins with dairy. Unbelievable.",
        ],
        "wand_charged": [
            "Oh. You actually did something competent. Mark the calendar.",
        ],
        "hyperdrive_fixed": [
            "You fixed a hyperdrive with duct tape. I am horrified AND impressed. "
            "Now get to the Bridge and ACTIVATE the jump!",
        ],
        "hyperdrive_not_fixed": [
            "The hyperdrive isn't fixed yet, you absolute walnut. Go to Engineering.",
        ],
        "crystal_obtained": [
            "Now bring that to Engineering. Fix my hyperdrive. Chop chop.",
        ],
        # Nat 20 / Nat 1 flavor
        "crit_success_move": [
            "You glide through like a majestic space-wizard. Almost impressive.",
        ],
        "crit_fail_move": [
            "Graceful. Truly graceful.",
        ],
        "perception_fail": [
            "Your powers of observation are... limited.",
        ],
        "perception_meh": [
            "Look harder next time. There was something useful out there.",
        ],
        # Generic snark
        "miss_stationary": [
            "You missed a stationary object. Remarkable.",
        ],
        "doors_defeat_you": [
            "Even doors defeat you. Marvelous.",
        ],
        "adequate": [
            "Adequate. Like everything about you.",
        ],
        "quit": [
            "Quitting? Coward. Come back when you've found your courage.",
        ],
    }

    def get_line(self, context, index=0):
        """Get a dialog line by context key. Returns empty string if missing."""
        lines = self.DIALOG.get(context, [])
        if not lines:
            return ""
        return lines[index % len(lines)]

    def say(self, context, index=0):
        """Have DRACOS speak a line from the dialog bank."""
        line = self.get_line(context, index)
        if line:
            dragon_says(line)

    # ─── NPC Interface ────────────────────────────────────────────────────

    def talk(self, game):
        dragon_says(self.get_line("bridge_talk"))
        return True

    def look(self, game):
        dim("DRACOS is everywhere. It's the station. It's the speakers. It's judging you.")
        return True

    def describe(self, game, first_visit):
        # DRACOS descriptions are handled inline by room describers
        # because it speaks contextually from many rooms.
        pass
