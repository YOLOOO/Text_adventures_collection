"""
ghost_chef.py — Ghost Chef Pierre.

Located in the Cafeteria. Can be:
  - Talked to (hints at wanting cheese)
  - Fought (standard combat)
  - Appeased with space_cheese (peaceful resolution)
"""

from npcs.base import NPC
from engine.display import info, dim, danger, success, alert, hr, C
from engine.dice import ask_d20, ask_4d6


class GhostChef(NPC):
    id = "ghost_chef"
    name = "Ghost Chef Pierre"
    aliases = ["ghost", "chef", "pierre"]

    # ─── Dialog ───────────────────────────────────────────────────────────

    DIALOG = {
        "talk_success": (
            "Pierre pauses. 'You... want to TALK? Nobody talks to Pierre anymore. "
            "All I want... is to cook one more perfect cheese fondue.'"
        ),
        "talk_meh": (
            "Pierre shrieks 'GET OUT OF MY KITCHEN!' but doesn't attack. He seems lonely."
        ),
        "talk_fail": (
            "Pierre hurls a spectral ladle at you!"
        ),
        "cheese_success": (
            "Pierre's eyes light up! He snatches the cheese, cradles it lovingly, "
            "prepares a spectral fondue, gives you a thumbs up, and fades to peaceful rest."
        ),
        "cheese_fail": (
            "Pierre sniffs the cheese and recoils. 'ZEES IS NOT AGED ENOUGH!'"
        ),
        "combat_intro": "⚔️  COMBAT: Ghost Chef Pierre!",
        "defeat": "Ghost Chef Pierre dissipates with a mournful wail about undercooked soufflés!",
    }

    # ─── Stats ────────────────────────────────────────────────────────────

    HP = 14
    ATTACK = 3
    FIGHT_DC = 11  # base DC to hit

    # ─── NPC Interface ────────────────────────────────────────────────────

    def is_active(self, game):
        return not game.check_flag("cafeteria_cleared")

    def describe(self, game, first_visit):
        if not self.is_active(game):
            return
        print()
        alert("Ghost Chef Pierre blocks the way! He looks angry... and transparent.")

    def look(self, game):
        if not self.is_active(game):
            dim("Chef Pierre has moved on to the great kitchen in the sky.")
        else:
            dim("Ghost Chef Pierre. Translucent. Angry. Spectral rolling pin. "
                "TALK, FIGHT, or USE items.")
        return True

    def talk(self, game):
        info("You address the floating ghost chef...")
        roll = ask_d20("Charisma — reasoning with a dead chef")
        game.set_flag("spoke_to_ghost")

        if roll >= 14 or roll == 20:
            print(f"  {self.DIALOG['talk_success']}")
            alert("HINT: Pierre wants cheese!")
        elif roll >= 8:
            print(f"  {self.DIALOG['talk_meh']}")
        else:
            print(f"  {self.DIALOG['talk_fail']}")
            game.take_damage(3)
        return True

    def use_item(self, game, item_id):
        """Handle cheese offering."""
        if item_id != "space_cheese":
            return False

        info("You offer the Space Cheese to Ghost Chef Pierre...")
        roll = ask_d20("Persuasion — does the ghost appreciate cheese?")

        if roll >= 10 or roll == 20:
            success(self.DIALOG["cheese_success"])
            game.set_flag("cafeteria_cleared")
            game.set_flag("ghost_appeased")
            game.remove_item("space_cheese")
            game.add_item("ghost_cookbook")
            success("Pierre left behind: Ghost Chef's Cookbook!")
            # DRACOS comment handled by caller
            return True
        else:
            print(f"  {self.DIALOG['cheese_fail']}")
            game.take_damage(3)
            return True

    def fight(self, game):
        info(self.DIALOG["combat_intro"])
        enemy_hp = self.HP
        print(f"  {C.DIM}Pierre HP: {enemy_hp} | Your HP: {game.hp}{C.RESET}")

        while enemy_hp > 0 and game.hp > 0 and not game.game_over:
            hr()
            print(f"  {C.BOLD}Your turn!{C.RESET} (ATTACK, USE [item], or FLEE)")
            action = input(f"  {C.CYAN}Combat> {C.RESET}").strip().lower()

            if action.startswith("flee") or action.startswith("run"):
                roll = ask_d20("Fleeing the angry ghost")
                if roll >= 8:
                    print("  You scramble away!")
                    return True
                else:
                    print("  Pierre blocks the exit with floating cutlery!")

            elif action.startswith("use"):
                parts = action.split(maxsplit=1)
                if len(parts) > 1:
                    handled = self.use_item(game, _fuzzy_match_inv(game, parts[1]))
                    if game.check_flag("cafeteria_cleared"):
                        return True
                    if not handled:
                        print("  That doesn't help here.")
                else:
                    print("  Use what?")
                    continue

            elif action.startswith("attack") or action.startswith("hit"):
                roll = ask_d20("Attack roll vs. Ghost Chef")
                dc = self.FIGHT_DC
                if game.has("plasma_sword"):
                    dc = 8
                    dim("Plasma Sword crackles against ectoplasm!")
                if game.check_flag("wand_charged"):
                    dc = min(dc, 7)
                    dim("USB Wand glows!")

                if roll >= dc or roll == 20:
                    total, _ = ask_4d6("Damage!")
                    bonus = 4 if game.has("plasma_sword") else 0
                    bonus += 3 if game.check_flag("wand_charged") else 0
                    dmg = total + bonus
                    if roll == 20:
                        dmg *= 2
                        success(f"CRITICAL HIT! {dmg} damage!")
                    else:
                        print(f"  {C.GREEN}Hit! {dmg} damage!{C.RESET}")
                    enemy_hp -= dmg
                else:
                    print("  Your attack passes through the ghost!")
            else:
                print("  Try ATTACK, USE [item], or FLEE.")
                continue

            # Ghost retaliates
            if enemy_hp > 0:
                print(f"\n  {C.RED}Pierre attacks with a spectral rolling pin!{C.RESET}")
                game.take_damage(self.ATTACK)

            print(f"  {C.DIM}Pierre HP: {max(0, enemy_hp)} | Your HP: {game.hp}{C.RESET}")

        if enemy_hp <= 0 and not game.game_over:
            success(self.DIALOG["defeat"])
            game.set_flag("cafeteria_cleared")
        return True


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _fuzzy_match_inv(game, word):
    """Find an inventory item matching a partial word."""
    for item in game.inventory:
        if word in item:
            return item
    return word
