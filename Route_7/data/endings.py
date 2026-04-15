"""
endings.py — Ending sequences for Route 7.

Endings branch on:
  - Escape method (rear door vs. driver's cab)
  - Evidence count (newspaper + map + log + report)
  - Final d20 roll
"""

from engine.display import (
    wrap, hr, title_print, slow_print, success, danger,
    dispatch_says, info, dim, alert, C
)
from engine.dice import ask_d20

TURN_LIMIT = 70


# ─── Time-out ending ──────────────────────────────────────────────────────────

def ending_end_of_line(game):
    """Bus reaches End of Line."""
    game.game_over = True
    game.won = False
    game.ending = "end_of_line"
    print()
    hr()
    title_print("ENDING: End of Line")
    slow_print(wrap(
        "The bus slows. Outside: nothing. No street, no lights, "
        "no sky. Just a grey expanse and a terminus sign "
        "that wasn't there a moment ago."
    ), 0.02)
    print()
    slow_print(wrap(
        "The doors open. The two rear passengers stand "
        "simultaneously and walk, without looking back, "
        "into the grey."
    ), 0.02)
    dispatch_says(
        "End of Line. All passengers please disembark. "
        "Route 7 will not be returning to service."
    )
    print()
    slow_print(wrap(
        "You have a choice. The doors are open. "
        "But the grey outside is very still, "
        "and very quiet, and goes on forever."
    ), 0.02)
    print(f"\n  {C.DIM}THE END (End of Line — {game.turns} turns){C.RESET}")
    hr()


# ─── Escape endings ───────────────────────────────────────────────────────────

def ending_escape_rear(game):
    """Player jumps from emergency rear door."""
    if game.room != "rear_seats":
        dim("You need to be at the rear of the bus.")
        return
    if not game.check_flag("lever_pulled"):
        dim(
            "The emergency door is still sealed. "
            "You need to release the latch first."
        )
        return

    dispatch_says(
        "Emergency exit activated. "
        "This is extremely inadvisable. "
        "The bus is travelling at speed."
    )
    info("FINAL ROLL — Jumping from a moving night bus.")
    roll = ask_d20("Hitting the road at sixty miles an hour")

    evidence = _count_evidence(game)
    game.game_over = True
    game.won = True

    if roll == 20:
        _ending_perfect_rear(game, evidence)
    elif roll >= 14:
        _ending_clean_rear(game, evidence)
    elif roll >= 7:
        _ending_narrow_rear(game, evidence)
    else:
        _ending_stumble_rear(game, evidence)

    hr()


def ending_escape_cab(game):
    """Player forces bus to stop from the driver's cab."""
    if game.room != "drivers_cab":
        dim("You need to be in the driver's cab.")
        return

    _describe_driver_confrontation(game)
    info("FINAL ROLL — Seizing control of a ghost bus.")
    roll = ask_d20("Forcing the wheel, hitting the brakes, screaming at the dead")

    evidence = _count_evidence(game)
    game.game_over = True
    game.won = True

    if roll == 20:
        _ending_perfect_cab(game, evidence)
    elif roll >= 14:
        _ending_clean_cab(game, evidence)
    elif roll >= 7:
        _ending_narrow_cab(game, evidence)
    else:
        _ending_stumble_cab(game, evidence)

    hr()


# ─── Evidence counter ─────────────────────────────────────────────────────────

def _count_evidence(game):
    evidence = ["newspaper_1987", "folded_map", "drivers_log", "bus_report"]
    return sum(1 for e in evidence if e in game.inventory)


# ─── Rear door escape subbranches ─────────────────────────────────────────────

def _ending_perfect_rear(game, evidence):
    game.ending = "perfect_rear"
    print()
    hr()
    title_print("⭐ ENDING: Hard Landing ⭐")
    slow_print(wrap(
        "You tuck and roll. Tarmac, hard and real. "
        "Behind you, the bus accelerates into the dark "
        "and is gone without a sound."
    ), 0.02)
    print()
    _evidence_epilogue(game, evidence)
    dispatch_says("Passenger deregistered from Route 7. Have a pleasant evening.")
    print(f"\n  {C.BOLD}{C.GREEN}THE END (Perfect — {game.turns} turns){C.RESET}")


def _ending_clean_rear(game, evidence):
    game.ending = "clean_rear"
    print()
    hr()
    title_print("ENDING: Out the Back")
    slow_print(wrap(
        "You hit the road shoulder and slide twenty feet. "
        "Skinned palms, torn jacket. Alive. "
        "The bus rounds a bend and vanishes."
    ), 0.02)
    _evidence_epilogue(game, evidence)
    print(f"\n  {C.GREEN}THE END (Clean — {game.turns} turns){C.RESET}")


def _ending_narrow_rear(game, evidence):
    game.ending = "narrow_rear"
    print()
    hr()
    title_print("ENDING: Barely")
    danger("You clip the road barrier. Ribs. Definite ribs.")
    slow_print(wrap(
        "You crawl to the verge. The bus is gone. "
        "The road is empty. You are on a motorway "
        "that isn't on any map you've ever seen."
    ), 0.02)
    if evidence >= 1:
        slow_print(wrap(
            "You have something. Enough to ask questions, "
            "if anyone will listen."
        ), 0.02)
    else:
        slow_print(wrap(
            "You have nothing. No proof, no explanation. "
            "Just a bus that wasn't there and a road that isn't either."
        ), 0.02)
    dispatch_says("Route 7 service concludes. Thank you for travelling with us.")
    print(f"\n  {C.YELLOW}THE END (Narrow — {game.turns} turns){C.RESET}")


def _ending_stumble_rear(game, evidence):
    game.ending = "stumble_rear"
    print()
    hr()
    title_print("ENDING: The Long Way Back")
    danger("You land badly. Your ankle is wrong. Very wrong.")
    slow_print(wrap(
        "You lie on cold tarmac for a long time. "
        "When you finally get up, you're alone on an empty road. "
        "No bus. No sign. No idea which way is home."
    ), 0.02)
    dispatch_says(
        "Passenger status: ambulatory, distressed. "
        "Route 7 thanks you for your custom."
    )
    print(f"\n  {C.YELLOW}THE END (Stumble — {game.turns} turns){C.RESET}")


# ─── Driver's cab escape subbranches ─────────────────────────────────────────

def _describe_driver_confrontation(game):
    if not game.check_flag("driver_looked"):
        danger(
            "You grab the driver's shoulder. "
            "They turn, finally. "
            "There is nothing there that should be called a face."
        )
    else:
        info("You lunge for the wheel.")
    dispatch_says(
        "Driver assistance is not available. "
        "Please return to your seat. "
        "End of Line is imminent."
    )


def _ending_perfect_cab(game, evidence):
    game.ending = "perfect_cab"
    print()
    hr()
    title_print("⭐ ENDING: Full Stop ⭐")
    slow_print(wrap(
        "You wrench the wheel hard left. The bus leaves the road "
        "and skids to a stop on a grass verge. "
        "The engine cuts. Silence — real silence."
    ), 0.02)
    print()
    slow_print(wrap(
        "When you look back, the driver's seat is empty. "
        "The rear passengers are gone. "
        "The bus smells of diesel and 1987."
    ), 0.02)
    print()
    _evidence_epilogue(game, evidence)
    dispatch_says(
        "Service terminated. Route 7 has been decommissioned. "
        "We apologise for any inconvenience."
    )
    print(f"\n  {C.BOLD}{C.GREEN}THE END (Perfect — {game.turns} turns){C.RESET}")


def _ending_clean_cab(game, evidence):
    game.ending = "clean_cab"
    print()
    hr()
    title_print("ENDING: Forced Stop")
    slow_print(wrap(
        "The bus swerves and grinds to a halt against a crash barrier. "
        "Doors spring open. You're out before the engine dies."
    ), 0.02)
    _evidence_epilogue(game, evidence)
    dispatch_says("Unscheduled stop. Please mind the gap.")
    print(f"\n  {C.GREEN}THE END (Clean — {game.turns} turns){C.RESET}")


def _ending_narrow_cab(game, evidence):
    game.ending = "narrow_cab"
    print()
    hr()
    title_print("ENDING: Close Call")
    danger("The bus clips a barrier at speed before it stops.")
    slow_print(wrap(
        "You stagger out. The driver's seat is empty. "
        "The whole bus is empty. "
        "You're in a layby on a road you half-recognise."
    ), 0.02)
    if evidence >= 1:
        info("You have evidence. Strange, hard-to-explain evidence.")
    dispatch_says(
        "Route 7: end of service. "
        "Have you considered the night bus?"
    )
    print(f"\n  {C.YELLOW}THE END (Narrow — {game.turns} turns){C.RESET}")


def _ending_stumble_cab(game, evidence):
    game.ending = "stumble_cab"
    print()
    hr()
    title_print("ENDING: Wreck")
    danger("The bus hits something. Hard. The windscreen goes.")
    slow_print(wrap(
        "You wake up in the verge ditch. "
        "No bus. No road. A housing estate on the horizon. "
        "Your watch reads 11:47 PM."
    ), 0.02)
    dispatch_says(
        "Journey complete. "
        "Route 7 thanks you for your patience."
    )
    print(f"\n  {C.RED}THE END (Wreck — {game.turns} turns){C.RESET}")


# ─── Evidence epilogue ────────────────────────────────────────────────────────

def _evidence_epilogue(game, evidence):
    if evidence >= 3:
        slow_print(wrap(
            "You have the newspaper, the logbook, the route map. "
            "Three pieces of a story nobody will believe "
            "until you lay them on a table and make them look."
        ), 0.02)
        print()
    elif evidence == 2:
        slow_print(wrap(
            "You have two pieces. Enough to ask questions. "
            "Not enough to answer them — yet."
        ), 0.02)
        print()
    elif evidence == 1:
        slow_print(wrap(
            "You have one thing. One piece of 1987 "
            "that shouldn't exist tonight."
        ), 0.02)
        print()
    else:
        slow_print(wrap(
            "You have nothing but the memory of it. "
            "Which is already starting to feel like a dream."
        ), 0.02)
        print()
