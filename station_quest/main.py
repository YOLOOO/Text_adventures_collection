#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           STATION QUEST: The Arcane Frontier                 ║
║     A Campy Sci-Fantasy Text Adventure with Real Dice        ║
╚══════════════════════════════════════════════════════════════╝

Run:  python3 main.py

You need: 4 six-sided dice (d6) and 1 twenty-sided die (d20)
"""

from engine.display import C, wrap, hr, slow_print
from engine.game import Game
from engine.commands import process_command
from data.room_descriptions import describe_room


def intro():
    print()
    print(f"{C.BOLD}{C.CYAN}")
    print("  ╔══════════════════════════════════════════════════════════╗")
    print("  ║      ⚔️  STATION QUEST: The Arcane Frontier  🚀        ║")
    print("  ║                                                          ║")
    print("  ║   A Campy Sci-Fantasy Text Adventure with REAL DICE     ║")
    print("  ╚══════════════════════════════════════════════════════════╝")
    print(f"{C.RESET}")
    print(f"  {C.YELLOW}You need: 4 six-sided dice (d6) and 1 twenty-sided die (d20){C.RESET}")
    print(f"  {C.DIM}Type 'help' for commands. Roll your real dice when prompted!{C.RESET}")
    hr()
    slow_print(wrap(
        "You are ZAX, a Level 2 Intern Wizard. You were studying for your "
        "Arcane Certification Exam when a rogue teleportation spell zapped you "
        "onto the ISS DRAGONHOLD — a derelict space station that was once a "
        "floating wizard academy. It's infested with space goblins, haunted "
        "by a ghost chef, and hurtling toward a planet made entirely of cheese."
    ), 0.02)
    print()
    slow_print(wrap(
        "The station's AI — DRACOS — insists it's a dragon. The hyperdrive "
        "is broken. And somehow YOU need to fix everything before you become "
        "one with the fondue."
    ), 0.02)
    print()
    slow_print(f"  {C.BOLD}Good luck, Intern. Grab your dice.{C.RESET}", 0.03)


def main():
    intro()
    game = Game()
    describe_room(game)

    while not game.game_over:
        print()
        try:
            raw = input(f"  {C.BOLD}{C.WHITE}> {C.RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            from engine.display import dragon_says
            dragon_says("Disconnecting? Coward.")
            break

        if not raw:
            continue

        if not process_command(game, raw):
            break  # quit

    if game.game_over and game.won:
        print(f"\n  {C.DIM}Thanks for playing Station Quest!{C.RESET}\n")
    elif game.game_over:
        print(f"\n  {C.DIM}Better luck next time, Intern.{C.RESET}\n")


if __name__ == "__main__":
    main()
