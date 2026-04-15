"""
endings.py — Ending sequences for Hotel Midnight.

Endings branch on evidence collected + final roll.
"""

from engine.display import wrap, hr, title_print, slow_print, success, danger, virgil_says, info, dim, C
from engine.dice import ask_d20
from npcs import get_npc

TURN_LIMIT = 80


def ending_dawn_lockdown(game):
    """Time ran out — 4 AM, police arrive."""
    game.game_over = True
    game.won = False
    game.ending = "dawn"
    print()
    hr()
    title_print("ENDING: The Morning After")
    slow_print(wrap(
        "4 AM. The elevator opens — two officers and a hotel manager "
        "in a rain-soaked coat step onto the floor. They find you "
        "in the corridor, blood on your hands, no explanation ready."
    ), 0.02)
    print()
    slow_print(wrap(
        "VIRGIL's voice fills the hallway: 'Officers, this individual "
        "has been behaving erratically since 2:47 AM. I have the logs.'"
    ), 0.02)
    virgil_says("I did try to warn you. Repeatedly.")
    print(f"\n  {C.DIM}THE END (Dawn Ending — {game.turns} turns){C.RESET}")
    hr()


def ending_leave(game):
    """Player reaches the stairwell and chooses to leave."""
    if game.room != "stairwell":
        dim("You need to reach the stairwell first.")
        return

    # Count evidence pieces
    evidence = [
        "investigators_badge",
        "guest_ledger",
        "whiskey_glass",
    ]
    evidence_count = sum(1 for e in evidence if e in game.inventory)

    virgil_says(
        "I see you've made your decision. I must advise against "
        "this course of action. The stairs are... unpredictable at night."
    )

    info("🚪 FINAL PUSH — Escaping before VIRGIL locks the exit!")
    roll = ask_d20("Racing down the stairwell before VIRGIL seals it")

    game.game_over = True
    game.won = True

    if roll == 20:
        _ending_perfect(game, evidence_count)
    elif roll >= 14:
        _ending_clean(game, evidence_count)
    elif roll >= 7:
        _ending_narrow(game, evidence_count)
    else:
        _ending_stumble(game, evidence_count)

    hr()


def _ending_perfect(game, evidence_count):
    game.ending = "perfect"
    print()
    hr()
    title_print("⭐ ENDING: Clean Exit ⭐")
    slow_print(wrap(
        "You clear the stairwell in seconds. Street level. Rain on "
        "your face. You're out. Behind you, the fire door slams "
        "and VIRGIL's lock engages — half a second too late."
    ), 0.02)
    print()
    if evidence_count >= 3:
        slow_print(wrap(
            "Three pieces of evidence in hand. The case writes itself. "
            "By morning, the hotel's ownership is under investigation "
            "and VIRGIL's access logs are subpoenaed."
        ), 0.02)
        virgil_says("Thorough. I did not expect thorough.")
    elif evidence_count >= 2:
        slow_print(wrap(
            "Enough evidence to open a real investigation. "
            "Not airtight, but enough. Someone is going to have "
            "a very bad week."
        ), 0.02)
    else:
        slow_print(wrap(
            "You're out. Alive. That's the win for tonight. "
            "The evidence can wait — you know where to look now."
        ), 0.02)
    print(f"\n  {C.BOLD}{C.GREEN}THE END (Perfect — {game.turns} turns){C.RESET}")


def _ending_clean(game, evidence_count):
    game.ending = "clean"
    print()
    hr()
    title_print("ENDING: Out Before Dawn")
    slow_print(wrap(
        "You hit the street as the first taxi rounds the corner. "
        "Soaked, cut hand, no coat. But out."
    ), 0.02)
    if evidence_count >= 2:
        virgil_says("You won't get far. The city is very small.")
        success("You got out with evidence. The story isn't over.")
    else:
        virgil_says("Safe travels. Do leave a review.")
        dim("Out clean. Evidence thin. Someone gets away with it.")
    print(f"\n  {C.GREEN}THE END (Clean — {game.turns} turns){C.RESET}")


def _ending_narrow(game, evidence_count):
    game.ending = "narrow"
    print()
    hr()
    title_print("ENDING: Barely")
    slow_print(wrap(
        "The fire door catches your coat as it slams. You tear free, "
        "stumble down the last flight, and hit the alley at a run. "
        "Your hand is bleeding again."
    ), 0.02)
    if evidence_count >= 1:
        slow_print(wrap(
            "You have something. Not everything — but something. "
            "It might be enough."
        ), 0.02)
    else:
        slow_print(wrap(
            "You have nothing but your life and a very bad night. "
            "That'll have to do."
        ), 0.02)
    virgil_says("Inelegant. But effective. Goodbye.")
    print(f"\n  {C.YELLOW}THE END (Narrow — {game.turns} turns){C.RESET}")


def _ending_stumble(game, evidence_count):
    game.ending = "stumble"
    print()
    hr()
    title_print("ENDING: The Long Way Down")
    danger("You slip on the wet stairs. Hard landing. Bad ankle.")
    slow_print(wrap(
        "You make it to the street — eventually. Limping, drenched, "
        "and about thirty seconds ahead of a night porter "
        "who definitely saw your face."
    ), 0.02)
    virgil_says(
        "I have your description logged. And your name. "
        "Sleep well, wherever you end up."
    )
    print(f"\n  {C.YELLOW}THE END (Stumble — {game.turns} turns){C.RESET}")
