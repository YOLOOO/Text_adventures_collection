"""
endings.py — Game ending sequences.

To add a new ending:
  1. Define a function that takes (game) and prints the ending text.
  2. Set game.game_over = True, game.won = True/False, game.ending = "key".
"""

from engine.display import (
    wrap, hr, title_print, slow_print, success, danger, dragon_says, info, C,
)
from engine.dice import ask_d20
from npcs import get_npc


TURN_LIMIT = 82


def ending_cheese_collision(game):
    """Time ran out — the station hits Planet Fromage."""
    from npcs import get_npc
    game.game_over = True
    game.won = False
    game.ending = "cheese_collision"
    print()
    hr()
    title_print("🧀 ENDING: You Are Fondue 🧀")
    slow_print(wrap(
        "The ISS Dragonhold slams into Planet Fromage at full speed. "
        "The hull crumples. Every surface is immediately coated in "
        "warm, gooey cheese. It smells amazing. You do not survive."
    ), 0.02)
    print()
    slow_print(wrap(
        "Somewhere in the wreckage, a speaker crackles one last time."
    ), 0.02)
    get_npc("dracos").say("time_warning_81")
    print(f"\n  {C.DIM}THE END (Cheese Collision — {game.turns} turns){C.RESET}")
    hr()


def ending_launch_escape_pod(game):
    """The coward's way out — escape pod from Escape Pod Bay."""
    dragon_says(
        "You're really doing this? Abandoning the station? Abandoning ME? "
        "Fine. FINE. Roll to see if the pod even works."
    )
    roll = ask_d20("Launching escape pod")
    if roll >= 5:
        game.game_over = True
        game.won = True
        game.ending = "coward"
        print()
        hr()
        title_print("ENDING: The Coward's Exit")
        slow_print(wrap(
            "The escape pod launches with a sad 'fwoomp.' You drift away from "
            "the ISS Dragonhold, watching it spiral toward Planet Fromage. The "
            "station's lights blink in a pattern spelling 'TRAITOR.'"
        ), 0.02)
        print()
        slow_print(wrap(
            "You crash-land on a moon made of crackers. You survive. You live "
            "as a hermit, haunted by cheese and a passive-aggressive AI dragon."
        ), 0.02)
        dragon_says("I hope the crackers are stale. Goodbye forever.")
        print(f"\n  {C.DIM}THE END (Coward Ending — {game.turns} turns){C.RESET}")
        hr()
    else:
        danger("The pod sputters and dies. Even the escape pod rejects you.")
        dragon_says("Ha. You're stuck with me.")


def ending_activate_hyperdrive(game):
    """Activate the hyperdrive from the Bridge — multiple endings based on roll."""
    if not game.check_flag("hyperdrive_fixed"):
        get_npc("dracos").say("hyperdrive_not_fixed")
        return

    dragon_says(
        "Hyperdrive online! Initiating jump! But I need you to calibrate "
        "the final coordinates. Roll well or we jump into a star."
    )

    info("🌟 FINAL CALIBRATION — Arcane Navigation Check!")
    roll = ask_d20("Calibrating hyperdrive jump coordinates")

    game.game_over = True
    game.won = True

    if roll == 20:
        _ending_perfect(game)
    elif roll >= 14:
        _ending_heroic(game)
    elif roll >= 8:
        _ending_messy(game)
    else:
        _ending_cheese(game)

    hr()


def _ending_perfect(game):
    game.ending = "perfect"
    print()
    hr()
    title_print("⭐ ENDING: The Perfect Jump ⭐")
    slow_print(wrap(
        "The ISS Dragonhold leaps through space with a thunderous CRACK! "
        "Stars streak past. You emerge at Wizard Homeworld Prime, "
        "greeted by a fleet of congratulatory dragon-ships."
    ), 0.02)
    print()
    slow_print(wrap(
        "You're promoted from Level 2 Intern to Level 7 Arcane Space Commander. "
        "Corner office. Nebula view. DRACOS is upgraded to Dragon Admiral."
    ), 0.02)
    if game.check_flag("goblins_befriended"):
        print()
        slow_print(wrap(
            "The goblins are granted asylum and open a successful cheese restaurant. "
            "King Zurt becomes a celebrity chef."
        ), 0.02)
    dragon_says("I always believed in you. That is a lie, but it feels appropriate.")
    print(f"\n  {C.BOLD}{C.GREEN}THE END (Perfect Ending — {game.turns} turns){C.RESET}")


def _ending_heroic(game):
    game.ending = "heroic"
    print()
    hr()
    title_print("ENDING: The Heroic Jump")
    slow_print(wrap(
        "The hyperdrive fires! The station lurches through light "
        "and emerges... somewhere safe. Not where you intended, "
        "but alive and cheese-free. That's a win."
    ), 0.02)
    dragon_says("We survived. Barely. Adding 'miracle worker' to your file. Sarcastically.")
    print(f"\n  {C.GREEN}THE END (Heroic Ending — {game.turns} turns){C.RESET}")


def _ending_messy(game):
    game.ending = "messy"
    print()
    hr()
    title_print("ENDING: The Messy Jump")
    slow_print(wrap(
        "The hyperdrive fires sideways. The station pinballs off three asteroids, "
        "clips Planet Fromage (acquiring a fondue coating), and crash-lands "
        "on a resort planet. Everyone survives. Covered in cheese."
    ), 0.02)
    dragon_says("We're alive. We're cheesy. Filing a complaint with the Wizard Council.")
    print(f"\n  {C.YELLOW}THE END (Messy Ending — {game.turns} turns){C.RESET}")


def _ending_cheese(game):
    game.ending = "cheese"
    print()
    hr()
    title_print("🧀 ENDING: The Cheese Ending 🧀")
    slow_print(wrap(
        "The hyperdrive fires wrong. The ISS Dragonhold plunges into "
        "Planet Fromage. But instead of destruction, you sink gently "
        "into warm, gooey cheese. It's... actually kind of nice?"
    ), 0.02)
    print()
    slow_print(wrap(
        "You build a civilization inside the cheese planet. "
        "DRACOS becomes the world's first AI cheese deity."
    ), 0.02)
    dragon_says("I am become cheese. Destroyer of lactose intolerance. BOW BEFORE ME.")
    print(f"\n  {C.YELLOW}THE END (Cheese Ending — {game.turns} turns){C.RESET}")
