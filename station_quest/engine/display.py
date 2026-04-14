"""
display.py — Terminal colors, formatting, and print helpers.

All visual output goes through here so the rest of the codebase
never touches ANSI codes directly.
"""

import sys
import textwrap
import time

# ─── ANSI Color Codes ────────────────────────────────────────────────────────

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

WRAP_WIDTH = 70

# ─── Utility Functions ────────────────────────────────────────────────────────

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

# ─── Themed Print Functions ───────────────────────────────────────────────────

def title_print(text):
    print(f"\n{C.BOLD}{C.CYAN}{'═' * WRAP_WIDTH}")
    print(f"  {text}")
    print(f"{'═' * WRAP_WIDTH}{C.RESET}\n")

def room_print(name):
    padding = max(0, WRAP_WIDTH - len(name) - 7)
    print(f"\n{C.BOLD}{C.WHITE}┌{'─' * (WRAP_WIDTH - 2)}┐")
    print(f"│  📍 {name}{' ' * padding}│")
    print(f"└{'─' * (WRAP_WIDTH - 2)}┘{C.RESET}")

def dragon_says(text):
    """DRACOS the AI dragon speaks."""
    print(f"\n  {C.MAGENTA}{C.BOLD}🐉 DRACOS:{C.RESET}{C.MAGENTA} \"{wrap(text)}\"{C.RESET}")

def alert(text):
    print(f"\n  {C.YELLOW}⚡ {wrap(text)}{C.RESET}")

def danger(text):
    print(f"\n  {C.RED}☠  {wrap(text)}{C.RESET}")

def success(text):
    print(f"\n  {C.GREEN}✨ {wrap(text)}{C.RESET}")

def info(text):
    print(f"\n  {C.CYAN}{wrap(text)}{C.RESET}")

def dim(text):
    print(f"  {C.DIM}{wrap(text)}{C.RESET}")
