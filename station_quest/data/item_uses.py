"""
item_uses.py — Item USE handlers.

When the player types USE [item], the engine:
  1. Fuzzy-matches the word to an inventory item.
  2. Checks if a room NPC wants to handle it (npc.use_item()).
  3. Falls through to the handlers registered here.

To add a new item's USE behavior:
  1. Define a function: def use_my_item(game) → bool
  2. Register it in USE_HANDLERS at the bottom.

Return True if the action consumed a turn, False otherwise.
"""

from engine.display import info, dim, success, danger, dragon_says
from engine.dice import ask_d20, ask_4d6
from data.items import item_name
from npcs import get_npc


def use_charging_crystal(game):
    """Charge the USB Wand with the Arcane Charging Crystal."""
    if not game.has("usb_wand"):
        info("You don't have anything to charge.")
        return True

    info("You jam the Arcane Charging Crystal into the USB Wand's port...")
    roll = ask_d20("Arcane Engineering — can you charge it?")

    if roll >= 8 or roll == 20:
        game.set_flag("wand_charged")
        game.remove_item("charging_crystal")
        success("The USB Wand SURGES to life! LED turns brilliant blue! WAND CHARGED!")
        get_npc("dracos").say("wand_charged")
    else:
        print("  The crystal sparks but doesn't connect. Try again later.")
        if roll == 1:
            danger("You shock yourself!")
            game.take_damage(3)
    return True


def use_usb_wand(game):
    """Use the USB Wand (only interesting when charged)."""
    if not game.check_flag("wand_charged"):
        info("The wand's LED blinks red. Dead battery. It does nothing.")
        return True

    # NPC-specific uses are handled by npc.use_item() in the command layer.
    # This is the generic fallback.
    info("You wave the charged wand. Sparkles fly. Nothing specific happens here.")
    return True


def use_space_cheese(game):
    """Eat the cheese for healing (NPC uses are handled by NPC.use_item)."""
    info("You take a bite of space cheese.")
    total, _ = ask_4d6("Cheese healing power")
    heal_amount = total // 3
    if heal_amount > 0:
        game.heal(heal_amount)
        game.remove_item("space_cheese")
        dragon_says("Eating random space cheese. Bold strategy.")
    else:
        print("  Tastes weird but doesn't help much.")
    return True


def use_goblin_repellent(game):
    """Generic repellent use (room NPC uses handled by GoblinKing.use_item)."""
    info("You spray the repellent into the air. It smells terrible. Nothing happens.")
    return True


def use_enchanted_duct_tape(game):
    """Fix the hyperdrive if you have the crystal and you're in engineering."""
    if game.room != "engineering":
        info("You wave the duct tape around. It fixes nothing here.")
        return True

    if not game.has("hyperdrive_crystal"):
        info("The duct tape needs something to tape INTO the hyperdrive. Like a crystal.")
        return True

    if game.check_flag("hyperdrive_fixed"):
        info("The hyperdrive is already fixed!")
        return True

    info("You tape the Hyperdrive Crystal into the engine with Enchanted Duct Tape...")
    roll = ask_d20("Engineering — can you duct-tape a hyperdrive?")

    if roll >= 8 or roll == 20:
        success(
            "The runes glow, the crystal locks in, and the hyperdrive ROARS to life! "
            "Screen: 'STATUS: Fixed With Tape. Somehow.'"
        )
        game.set_flag("hyperdrive_fixed")
        game.remove_item("enchanted_duct_tape")
        game.remove_item("hyperdrive_crystal")
        get_npc("dracos").say("hyperdrive_fixed")
    else:
        print("  The tape doesn't stick. Try again.")
        if roll == 1:
            danger("You tape your hand to the engine!")
            game.take_damage(2)
    return True


def use_plasma_sword(game):
    info("You ignite the Plasma Sword. It hums with adequate energy.")
    get_npc("dracos").say("adequate")
    return True


def use_ghost_cookbook(game):
    info("You flip through translucent recipes: 'Ectoplasmic Risotto', 'Soul Soufflé'...")
    total, _ = ask_4d6("Culinary inspiration healing")
    heal_amount = total // 4
    if heal_amount > 0:
        game.heal(heal_amount)
        success("Reading the recipes fills you with warmth!")
    return True


def use_goblin_crown(game):
    info("You put on the Goblin Crown. You smell terrible now. The goblins would be proud.")
    return True


# ─── USE HANDLER REGISTRY ────────────────────────────────────────────────────
#
#   Maps item_id → handler function.
#   If an item has no handler, a generic message is shown.

USE_HANDLERS = {
    "charging_crystal":     use_charging_crystal,
    "usb_wand":             use_usb_wand,
    "space_cheese":         use_space_cheese,
    "goblin_repellent":     use_goblin_repellent,
    "enchanted_duct_tape":  use_enchanted_duct_tape,
    "plasma_sword":         use_plasma_sword,
    "ghost_cookbook":        use_ghost_cookbook,
    "goblin_crown":         use_goblin_crown,
}
