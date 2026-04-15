#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║          HOTEL MIDNIGHT: Room 314                            ║
║          A Noir Mystery with Real Dice                       ║
╚══════════════════════════════════════════════════════════════╝

Run:  python3 main.py
You need: 1 twenty-sided die (d20) and 2 six-sided dice (2d6)
"""

from engine.display import C, WRAP_WIDTH, wrap, hr, slow_print
from engine.game import Game
from engine.commands import process_command
from data.room_descriptions import describe_room


def intro():
    W = WRAP_WIDTH - 4
    print()
    print(f"{C.BOLD}{C.BLUE}")
    print(f"  ╔{'═' * W}╗")
    print(f"  ║{'HOTEL MIDNIGHT: Room 314'.center(W)}║")
    print(f"  ║{'A Noir Mystery with Real Dice'.center(W)}║")
    print(f"  ╚{'═' * W}╝")
    print(f"{C.RESET}")
    print(f"  {C.YELLOW}You need: 1d20 and 2d6{C.RESET}")
    print(f"  {C.DIM}Type 'help' for commands.{C.RESET}")
    hr()
    slow_print(wrap(
        "2:47 AM. You open your eyes on the floor of a rain-soaked "
        "hotel room. There is blood on your hands."
    ), 0.025)
    print()
    slow_print(wrap(
        "You don't know how you got here. Your phone is dead. "
        "The door is locked from the outside. "
        "The bathroom mirror is smashed."
    ), 0.025)
    print()
    slow_print(wrap(
        "On the nightstand: a note. Your handwriting."
    ), 0.025)
    print()
    slow_print(
        f"  {C.BOLD}{C.YELLOW}"
        f"'Don't trust the concierge.{C.RESET}"
    , 0.03)
    slow_print(
        f"  {C.BOLD}{C.YELLOW}"
        f" The key is in the piano.{C.RESET}"
    , 0.03)
    slow_print(
        f"  {C.BOLD}{C.YELLOW}"
        f" Get out before 4 AM.'{C.RESET}"
    , 0.03)
    print()
    slow_print(f"  {C.DIM}Grab your dice. The clock is running.{C.RESET}", 0.02)


def main():
    intro()
    game = Game()
    # Player starts with the note already read
    game.add_item("note")
    describe_room(game)

    while not game.game_over:
        print()
        try:
            raw = input(f"  {C.BOLD}{C.WHITE}> {C.RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            from engine.display import virgil_says
            virgil_says("Leaving without checking out. How unfortunate.")
            break

        if not raw:
            continue

        if not process_command(game, raw):
            break

    if game.game_over and game.won:
        print(f"\n  {C.DIM}Thanks for playing Hotel Midnight.{C.RESET}\n")
    elif game.game_over:
        print(f"\n  {C.DIM}The hotel keeps its secrets.{C.RESET}\n")


if __name__ == "__main__":
    main()
