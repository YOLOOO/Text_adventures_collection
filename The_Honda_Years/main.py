#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║          THE HONDA YEARS                                 ║
║          A Family Road Trip Drama-Comedy                 ║
╚══════════════════════════════════════════════════════════╝

Run:  python3 main.py
No dice needed. Just choices.
"""

from engine.display import C, WRAP_WIDTH, wrap, hr, slow_print
from engine.game import Game
from engine.commands import process_command
from data.room_descriptions import describe_room


def intro():
    W = WRAP_WIDTH - 4
    print()
    print(f"{C.BOLD}{C.CYAN}")
    print(f"  ╔{'═' * W}╗")
    print(f"  ║{'THE HONDA YEARS'.center(W)}║")
    print(f"  ║{'A Family Road Trip Drama-Comedy'.center(W)}║")
    print(f"  ╚{'═' * W}╝")
    print(f"{C.RESET}")
    print(f"  {C.DIM}Type 'help' for commands.  No dice needed.{C.RESET}")
    hr()
    slow_print(wrap("5:47 AM. The Honda is packed."), 0.03)
    print()
    slow_print(wrap(
        "Sarah is already in the passenger seat, coffee in hand, "
        "sunglasses on even though it's barely light. "
        "Drew is in the back with his headphones already on. "
        "Emma is drawing something in her notebook."
    ), 0.022)
    print()
    slow_print(wrap(
        "2,100 miles to Portland. "
        "You've been in couples therapy for eight weeks. "
        "Nobody has told the kids."
    ), 0.022)
    print()
    slow_print(wrap(
        "Sarah booked the trip. 'A reset,' she called it. "
        "You're still not sure what you're resetting to."
    ), 0.022)
    print()
    slow_print(
        f"  {C.BOLD}{C.YELLOW}Chicago to Portland. 2,100 miles.{C.RESET}",
        0.03
    )
    slow_print(
        f"  {C.BOLD}{C.YELLOW}Just the four of you.{C.RESET}",
        0.03
    )
    print()


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
            from engine.display import radio_says
            radio_says("This is WKND. Drive safe. Talk to the people in your car.")
            break

        if not raw:
            continue

        if not process_command(game, raw):
            break

    if game.game_over and game.won:
        print(f"\n  {C.DIM}Thanks for playing The Honda Years.{C.RESET}\n")
    elif game.game_over:
        print(f"\n  {C.DIM}Some trips don't have destinations.{C.RESET}\n")


if __name__ == "__main__":
    main()
