#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║          ROUTE 7                                             ║
║          A Ghost Bus Mystery with Real Dice                  ║
╚══════════════════════════════════════════════════════════════╝

Run:  python3 main.py
You need: 1 twenty-sided die (d20)
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
    print(f"  ║{'ROUTE 7'.center(W)}║")
    print(f"  ║{'A Ghost Bus Mystery with Real Dice'.center(W)}║")
    print(f"  ╚{'═' * W}╝")
    print(f"{C.RESET}")
    print(f"  {C.YELLOW}You need: 1d20{C.RESET}")
    print(f"  {C.DIM}Type 'help' for commands.{C.RESET}")
    hr()
    slow_print(wrap(
        "11:47 PM. You open your eyes."
    ), 0.03)
    print()
    slow_print(wrap(
        "You're on a bus. You don't remember getting on. "
        "The seat is cold. "
        "The fluorescent lights hum at a frequency "
        "just below comfortable."
    ), 0.022)
    print()
    slow_print(wrap(
        "The windows show a motorway. No signs. No other cars. "
        "You don't recognise the road."
    ), 0.022)
    print()
    slow_print(wrap(
        "In your jacket pocket: a ticket stub."
    ), 0.025)
    print()
    slow_print(
        f"  {C.BOLD}{C.YELLOW}"
        f"Night Bus — Route 7.{C.RESET}"
    , 0.03)
    slow_print(
        f"  {C.BOLD}{C.YELLOW}"
        f" Destination: END OF LINE.{C.RESET}"
    , 0.03)
    slow_print(
        f"  {C.BOLD}{C.YELLOW}"
        f" Issued: 11:47 PM, November 14, 1987.{C.RESET}"
    , 0.03)
    print()
    slow_print(f"  {C.DIM}Grab your die. The bus is moving.{C.RESET}", 0.02)


def main():
    intro()
    game = Game()
    game.add_item("ticket_stub")
    describe_room(game)

    while not game.game_over:
        print()
        try:
            raw = input(f"  {C.BOLD}{C.WHITE}> {C.RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n")
            from engine.display import dispatch_says
            dispatch_says(
                "Service interrupted. "
                "Route 7 thanks you for travelling with us."
            )
            break

        if not raw:
            continue

        if not process_command(game, raw):
            break

    if game.game_over and game.won:
        print(f"\n  {C.DIM}Thanks for playing Route 7.{C.RESET}\n")
    elif game.game_over:
        print(f"\n  {C.DIM}The route continues.{C.RESET}\n")


if __name__ == "__main__":
    main()
