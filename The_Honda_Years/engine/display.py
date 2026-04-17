"""
display.py — Terminal colors, formatting, and print helpers.
WRAP_WIDTH targets 4.3" 800x480.
"""

import sys
import textwrap
import time


class C:
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    MAGENTA = "\033[95m"
    BLUE    = "\033[94m"
    WHITE   = "\033[97m"
    RESET   = "\033[0m"

WRAP_WIDTH = 58


def wrap(text, width=WRAP_WIDTH):
    return textwrap.fill(text, width=width)

def hr():
    print(f"{C.DIM}{'─' * WRAP_WIDTH}{C.RESET}")

def slow_print(text, delay=0.015):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def title_print(text):
    print(f"\n{C.BOLD}{C.CYAN}{'═' * WRAP_WIDTH}")
    print(f"  {text}")
    print(f"{'═' * WRAP_WIDTH}{C.RESET}\n")

def room_print(name):
    padding = max(0, WRAP_WIDTH - len(name) - 7)
    print(f"\n{C.BOLD}{C.WHITE}┌{'─' * (WRAP_WIDTH - 2)}┐")
    print(f"│  🚗 {name}{' ' * padding}│")
    print(f"└{'─' * (WRAP_WIDTH - 2)}┘{C.RESET}")

def radio_says(text):
    """RADIO — The Honda's car stereo, weirdly on-point."""
    filled = textwrap.fill(text, width=WRAP_WIDTH - 2, subsequent_indent="  ")
    print(f"\n  {C.CYAN}{C.BOLD}📻 RADIO:{C.RESET}")
    print(f"  {C.CYAN}\"{filled}\"{C.RESET}")

def alert(text):
    filled = textwrap.fill(text, width=WRAP_WIDTH - 4, subsequent_indent="    ")
    print(f"  {C.YELLOW}⚡ {filled}{C.RESET}")

def danger(text):
    filled = textwrap.fill(text, width=WRAP_WIDTH - 4, subsequent_indent="    ")
    print(f"\n  {C.RED}✗  {filled}{C.RESET}")

def success(text):
    filled = textwrap.fill(text, width=WRAP_WIDTH - 4, subsequent_indent="    ")
    print(f"  {C.GREEN}✓  {filled}{C.RESET}")

def info(text):
    filled = textwrap.fill(text, width=WRAP_WIDTH - 2, subsequent_indent="  ")
    print(f"  {C.CYAN}{filled}{C.RESET}")

def dim(text):
    filled = textwrap.fill(text, width=WRAP_WIDTH - 2, subsequent_indent="  ")
    print(f"  {C.DIM}{filled}{C.RESET}")

def ask_choice(prompt, options):
    """Present numbered dialogue options. Returns 1-based index."""
    print(f"\n  {C.DIM}{prompt}{C.RESET}")
    for i, opt in enumerate(options, 1):
        print(f"  {C.CYAN}{i}.{C.RESET} {opt}")
    while True:
        try:
            raw = input(f"  {C.BOLD}Choose (1-{len(options)}): {C.RESET}").strip()
            val = int(raw)
            if 1 <= val <= len(options):
                return val
            print(f"  Enter a number between 1 and {len(options)}.")
        except (ValueError, EOFError):
            print(f"  Enter a number between 1 and {len(options)}.")
