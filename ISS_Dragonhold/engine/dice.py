"""
dice.py — Physical dice rolling system.

The player rolls REAL dice and enters the results.
All dice logic is centralized here for easy modification
(e.g., adding new dice types, changing feedback thresholds).
"""

from engine.display import C, success, danger, dim


def ask_d20(reason):
    """
    Prompt the player to roll their physical d20.

    Args:
        reason: Why they're rolling (shown to the player).

    Returns:
        int: The roll result (1-20).
    """
    print(f"\n  {C.BOLD}{C.BLUE}🎲 ROLL YOUR d20!{C.RESET}")
    dim(f"Reason: {reason}")

    while True:
        try:
            val = int(input(f"  {C.BLUE}Enter d20 result (1-20): {C.RESET}").strip())
            if 1 <= val <= 20:
                _announce_d20(val)
                return val
            print("  Enter a number between 1 and 20.")
        except ValueError:
            print("  Enter a number between 1 and 20.")


def ask_2d6(reason):
    """
    Prompt the player to roll their 2 physical d6.

    Args:
        reason: Why they're rolling.

    Returns:
        tuple: (total: int, dice: list[int])
    """
    print(f"\n  {C.BOLD}{C.BLUE}🎲 ROLL YOUR 2d6!{C.RESET}")
    dim(f"Reason: {reason}")

    dice = []
    for i in range(2):
        while True:
            try:
                val = int(input(f"  {C.BLUE}Die {i + 1} of 2 (1-6): {C.RESET}").strip())
                if 1 <= val <= 6:
                    dice.append(val)
                    break
                print("  Enter a number between 1 and 6.")
            except ValueError:
                print("  Enter a number between 1 and 6.")

    total = sum(dice)
    _announce_2d6(dice, total)
    return total, dice


# ─── Internal Feedback ────────────────────────────────────────────────────────

def _announce_d20(val):
    if val == 20:
        success("⚔️  NATURAL 20! CRITICAL SUCCESS!")
    elif val == 1:
        danger("💀 NATURAL 1! CRITICAL FAILURE!")
    elif val >= 15:
        print(f"  {C.GREEN}Rolled {val} — solid!{C.RESET}")
    elif val >= 10:
        print(f"  {C.YELLOW}Rolled {val} — decent.{C.RESET}")
    else:
        print(f"  {C.RED}Rolled {val} — yikes.{C.RESET}")


def _announce_2d6(dice, total):
    result_str = " + ".join(str(d) for d in dice)
    if total == 12:
        success(f"[{result_str}] = {total} — Magnificent!")
    elif total >= 9:
        print(f"  {C.GREEN}[{result_str}] = {total} — Nice roll!{C.RESET}")
    elif total >= 6:
        print(f"  {C.YELLOW}[{result_str}] = {total} — Could be worse.{C.RESET}")
    else:
        print(f"  {C.RED}[{result_str}] = {total} — The dice gods frown upon you.{C.RESET}")
