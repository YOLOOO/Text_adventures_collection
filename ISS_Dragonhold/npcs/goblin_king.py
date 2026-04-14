"""
goblin_king.py — Goblin King Zurt and the Goblin Horde.

Located in the Cargo Hold. Can be:
  - Talked to (hints at cheese diplomacy)
  - Befriended with space_cheese (peaceful resolution)
  - Fought (harder combat with minions)
  - Repelled with goblin_repellent (lucky spray)
"""

from npcs.base import NPC
from engine.display import info, dim, danger, success, alert, hr, C
from engine.dice import ask_d20, ask_2d6


class GoblinKing(NPC):
    id = "goblin_king"
    name = "Goblin King Zurt"
    aliases = ["goblin", "king", "zurt", "goblins"]

    # ─── Dialog ───────────────────────────────────────────────────────────

    DIALOG = {
        "talk_success": (
            "Zurt holds up a tiny hand. 'You... not smash? You TALK? "
            "Zurt's people hungry. Station cold. We want home. Also cheese.'"
        ),
        "talk_meh": "Zurt grunts. 'What you want, tall-thing? Bring tribute? Cheese maybe?'",
        "talk_fail": "A goblin throws a bolt at your head.",
        "cheese_success": (
            "King Zurt's eyes go WIDE. He takes the cheese reverently, "
            "takes a bite, and declares you an honorary goblin!"
        ),
        "cheese_fail": "Zurt sniffs the cheese and hisses. 'NOT STINKY ENOUGH!'",
        "repellent_success": "It works! The goblins scatter, coughing and gagging!",
        "repellent_meh": "The goblins sneeze but look more annoyed than repelled.",
        "repellent_fail": "The can backfires! You spray yourself!",
        "combat_intro": "⚔️  COMBAT: Goblin King Zurt + Horde!",
        "defeat": "King Zurt collapses! The remaining goblins scatter into the vents!",
    }

    # ─── Stats ────────────────────────────────────────────────────────────

    HP = 22
    ATTACK = 4
    MINION_COUNT = 3
    MINION_ATTACK = 2
    FIGHT_DC = 11

    # ─── NPC Interface ────────────────────────────────────────────────────

    def is_active(self, game):
        return (not game.check_flag("goblins_defeated")
                and not game.check_flag("goblins_befriended"))

    def describe(self, game, first_visit):
        if not self.is_active(game):
            return
        alert("Goblin King Zurt stares at you. This could go several ways.")

    def look(self, game):
        if game.check_flag("goblins_befriended"):
            dim("King Zurt nods regally. You're honored guests now.")
        elif game.check_flag("goblins_defeated"):
            dim("The goblins have fled.")
        else:
            dim("Goblin King Zurt. Small, fierce, circuit-board crown. "
                "TALK, FIGHT, or USE items.")
        return True

    def talk(self, game):
        info("You attempt to communicate with Goblin King Zurt...")
        roll = ask_d20("Diplomacy — understanding goblin culture")

        if roll >= 12 or roll == 20:
            print(f"  {self.DIALOG['talk_success']}")
            alert("HINT: The goblins can be befriended with cheese!")
        elif roll >= 6:
            print(f"  {self.DIALOG['talk_meh']}")
        else:
            print(f"  {self.DIALOG['talk_fail']}")
            game.take_damage(2)
        return True

    def use_item(self, game, item_id):
        if item_id == "space_cheese":
            return self._use_cheese(game)
        if item_id == "goblin_repellent":
            return self._use_repellent(game)
        return False

    def _use_cheese(self, game):
        info("You offer the Space Cheese to the Goblin King...")
        roll = ask_d20("Diplomacy — goblins love cheese, right?")

        if roll >= 12 or roll == 20:
            success(self.DIALOG["cheese_success"])
            game.set_flag("goblins_befriended")
            game.remove_item("space_cheese")
            game.add_item("goblin_crown")
            success("Received: The Goblin Crown! (It smells, but it's an honor.)")
            return True
        else:
            print(f"  {self.DIALOG['cheese_fail']}")
            game.take_damage(3)
            return True

    def _use_repellent(self, game):
        info("You spray the expired Goblin Repellent!")
        roll = ask_d20("Does expired repellent work?")

        if roll >= 15:
            success(self.DIALOG["repellent_success"])
            game.set_flag("goblins_defeated")
            game.set_flag("goblin_king_alive", False)
            game.remove_item("goblin_repellent")
        elif roll >= 8:
            print(f"  {self.DIALOG['repellent_meh']}")
        else:
            danger(self.DIALOG["repellent_fail"])
            game.take_damage(2)
        return True

    def fight(self, game):
        info(self.DIALOG["combat_intro"])
        king_hp = self.HP
        minions = self.MINION_COUNT
        print(f"  {C.DIM}Zurt HP: {king_hp} | Minions: {minions} | Your HP: {game.hp}{C.RESET}")

        while king_hp > 0 and game.hp > 0 and not game.game_over:
            hr()
            print(f"  {C.BOLD}Your turn!{C.RESET} (ATTACK, USE [item], or FLEE)")
            action = input(f"  {C.CYAN}Combat> {C.RESET}").strip().lower()

            if action.startswith("flee") or action.startswith("run"):
                roll = ask_d20("Escaping the goblin horde")
                if roll >= 12:
                    print("  You bolt for the hatch!")
                    return True
                else:
                    print("  Goblins block every exit!")
                    game.take_damage(2)

            elif action.startswith("use"):
                parts = action.split(maxsplit=1)
                if len(parts) > 1:
                    item = _fuzzy_match_inv(game, parts[1])
                    handled = self.use_item(game, item)
                    if game.check_flag("goblins_befriended") or game.check_flag("goblins_defeated"):
                        return True
                    if not handled:
                        print("  That doesn't help here.")
                else:
                    print("  Use what?")
                    continue

            elif action.startswith("attack") or action.startswith("hit"):
                roll = ask_d20("Attack roll vs. Goblin forces")
                dc = self.FIGHT_DC
                if game.has("plasma_sword"):
                    dc = 8
                if roll >= dc or roll == 20:
                    total, _ = ask_2d6("Damage!")
                    bonus = 4 if game.has("plasma_sword") else 0
                    bonus += 3 if game.check_flag("wand_charged") else 0
                    dmg = total + bonus
                    if roll == 20:
                        dmg *= 2
                        success(f"CRITICAL! {dmg} damage!")
                    else:
                        print(f"  {C.GREEN}Hit! {dmg} damage!{C.RESET}")

                    if minions > 0 and dmg >= 6:
                        minions -= 1
                        print(f"  {C.YELLOW}A goblin minion goes down! ({minions} left){C.RESET}")
                        king_hp -= max(0, dmg - 6)
                    elif minions > 0:
                        print("  You wound a goblin minion!")
                    else:
                        king_hp -= dmg
                else:
                    print("  The goblins dodge your attack!")
            else:
                print("  Try ATTACK, USE [item], or FLEE.")
                continue

            # Goblin retaliation
            if king_hp > 0:
                total_dmg = 0
                if minions > 0:
                    print(f"\n  {C.RED}Goblin minions swarm you!{C.RESET}")
                    total_dmg += minions * self.MINION_ATTACK
                print(f"  {C.RED}King Zurt throws an enchanted circuit board!{C.RESET}")
                total_dmg += self.ATTACK
                game.take_damage(total_dmg)

            print(f"  {C.DIM}Zurt HP: {max(0, king_hp)} | Minions: {minions} | Your HP: {game.hp}{C.RESET}")

        if king_hp <= 0 and not game.game_over:
            success(self.DIALOG["defeat"])
            game.set_flag("goblins_defeated")
            game.set_flag("goblin_king_alive", False)
        return True


def _fuzzy_match_inv(game, word):
    for item in game.inventory:
        if word in item:
            return item
    return word
