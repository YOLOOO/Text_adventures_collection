"""
turret.py — Rogue Spell-Turret.

Located in Engineering. Blocks access to the Armory.
Can be fought or zapped with a charged USB wand.
"""

from npcs.base import NPC
from engine.display import info, dim, danger, success, hr, C
from engine.dice import ask_d20, ask_4d6


class Turret(NPC):
    id = "turret"
    name = "Rogue Spell-Turret"
    aliases = ["turret", "spell-turret", "rogue"]

    DIALOG = {
        "combat_intro": "⚔️  COMBAT: Rogue Spell-Turret!",
        "defeat": "The turret sparks, sputters, and collapses into a heap of scrap!",
    }

    HP = 12
    ATTACK = 4
    FIGHT_DC = 12

    def is_active(self, game):
        return not game.check_flag("turret_disabled")

    def describe(self, game, first_visit):
        if self.is_active(game):
            danger("A ROGUE SPELL-TURRET swivels to track you! Its barrel glows ominously.")
        else:
            dim("The destroyed turret smokes quietly in the corner.")

    def look(self, game):
        if self.is_active(game):
            dim("A rogue spell-turret. Tracks your movement. FIGHT it or USE items.")
        else:
            dim("A smoking heap of scrap. Good riddance.")
        return True

    def use_item(self, game, item_id):
        """Charged wand can one-shot the turret."""
        if item_id == "usb_wand" and game.check_flag("wand_charged"):
            info("You aim your charged USB Wand at the spell-turret!")
            roll = ask_d20("Arcane Attack vs. Turret")
            if roll >= 10 or roll == 20:
                total, _ = ask_4d6("Magical damage!")
                success(f"ZAP! {total} damage! The turret explodes in sparks!")
                game.set_flag("turret_disabled")
            else:
                print("  The bolt goes wide! The turret retaliates!")
                game.take_damage(self.ATTACK)
            return True
        return False

    def fight(self, game):
        info(self.DIALOG["combat_intro"])
        enemy_hp = self.HP
        print(f"  {C.DIM}Turret HP: {enemy_hp} | Your HP: {game.hp}{C.RESET}")

        while enemy_hp > 0 and game.hp > 0 and not game.game_over:
            hr()
            print(f"  {C.BOLD}Your turn!{C.RESET} (ATTACK, USE [item], or FLEE)")
            action = input(f"  {C.CYAN}Combat> {C.RESET}").strip().lower()

            if action.startswith("flee") or action.startswith("run"):
                roll = ask_d20("Dodging turret fire to escape")
                if roll >= 10:
                    print("  You dive behind cover and scramble out!")
                    return True
                else:
                    print("  The turret pins you down!")
                    game.take_damage(self.ATTACK // 2)

            elif action.startswith("use"):
                parts = action.split(maxsplit=1)
                if len(parts) > 1:
                    item = _fuzzy_match_inv(game, parts[1])
                    handled = self.use_item(game, item)
                    if game.check_flag("turret_disabled"):
                        return True
                    if not handled:
                        print("  That doesn't help here.")
                else:
                    print("  Use what?")
                    continue

            elif action.startswith("attack") or action.startswith("hit"):
                roll = ask_d20("Attack roll vs. Turret")
                dc = self.FIGHT_DC
                if game.has("plasma_sword"):
                    dc = 9
                if roll >= dc or roll == 20:
                    total, _ = ask_4d6("Damage!")
                    bonus = 5 if game.has("plasma_sword") else 0
                    dmg = total + bonus
                    if roll == 20:
                        dmg *= 2
                        success(f"CRITICAL! {dmg} damage!")
                    else:
                        print(f"  {C.GREEN}Hit! {dmg} damage!{C.RESET}")
                    enemy_hp -= dmg
                else:
                    print("  Attack bounces off the turret's plating!")
            else:
                print("  Try ATTACK, USE [item], or FLEE.")
                continue

            if enemy_hp > 0:
                print(f"\n  {C.RED}The turret fires a spell-bolt!{C.RESET}")
                game.take_damage(self.ATTACK)

            print(f"  {C.DIM}Turret HP: {max(0, enemy_hp)} | Your HP: {game.hp}{C.RESET}")

        if enemy_hp <= 0 and not game.game_over:
            success(self.DIALOG["defeat"])
            game.set_flag("turret_disabled")
        return True


def _fuzzy_match_inv(game, word):
    for item in game.inventory:
        if word in item:
            return item
    return word
