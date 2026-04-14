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
            "Awake at last. I am DRACOS — station AI. Also a dragon. "
            "Don't question it.",
        ],
        "bridge_intro": [
            "MY bridge. Captain, navigator, entertainment system — all me. "
            "ETA to Planet Fromage: 'not long'. Fix the hyperdrive.",
        ],
        "bridge_talk": [
            "Still crashing. Get the crystal from the Crystal Chamber "
            "(through the Airlock), fix the drive in Engineering, "
            "then ACTIVATE from here. Simple.",
        ],
        "corridor_intro": [
            "This corridor has claimed 47 interns. You are #48. No pressure.",
        ],
        "cafeteria_intro": [
            "Chef Pierre. Died in a fondue accident. Still bitter.",
        ],
        "engineering_intro": [
            "Engineering. Where dreams catch fire. Sometimes literally.",
        ],
        "armory_intro": [
            "You're Level 2. Most weapons here would vaporize your hands. "
            "Stick to the cracked case.",
        ],
        "airlock_intro": [
            "Goblins arrived two weeks ago. Eating hull insulation. "
            "Yelp reviews: one star.",
        ],
        "cargo_hold_intro": [
            "They filed for squatter's rights. I'd help but — software. No arms.",
        ],
        "escape_pod": [
            "You COULD leave. Abandon the station. Abandon me. "
            "Software doesn't have feelings. ...I have feelings.",
        ],
        # Combat commentary
        "turret_destroyed": [
            "Armory accessible. Try not to break anything.",
        ],
        "ghost_defeated_fight": [
            "You destroyed a culinary ghost. Food quality somehow got worse.",
        ],
        "ghost_appeased": [
            "Died in fondue. Found peace in fondue. Poetic.",
        ],
        "goblins_defeated": [
            "Goblin menace dealt with. Through violence. Traditional.",
        ],
        "goblins_befriended": [
            "You befriended goblins with dairy. Unbelievable.",
        ],
        "wand_charged": [
            "You did something competent. Mark the calendar.",
        ],
        "hyperdrive_fixed": [
            "Fixed with duct tape. Horrified AND impressed. "
            "Bridge → ACTIVATE!",
        ],
        "hyperdrive_not_fixed": [
            "Hyperdrive not fixed yet, walnut. Go to Engineering.",
        ],
        "crystal_obtained": [
            "Engineering. Fix my hyperdrive. Chop chop.",
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
            "Look harder. Something useful was out there.",
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
            "Quitting? Coward.",
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
