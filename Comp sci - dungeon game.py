
import random
import json
from pathlib import Path

rooms_cleared = 0
current_gold = 0
last_run_gold = 0
game_over = False
quit_requested = False

rooms = [
    "The Entrance",
    "Dungeon Floor 1",
    "Dungeon Floor 2",
    "Dungeon Floor 3",
    "Dungeon Exit",
    "Main Hall Floor 1",
    "Main Hall Floor 2",
    "Main Hall Floor 3",
    "Guarded Doors",
    "Throne Room",
    "Royal Antechamber",
    "The King's Treasury",
    "Forgotten Library",
    "The Final Guardian",
    "The Inner Sanctum"
]

HIGH_SCORE_FILE = Path("high_score.json")


def save_high_score(score):
    try:
        with HIGH_SCORE_FILE.open("w", encoding="utf-8") as file:
            json.dump({"high_score": score}, file, indent=4)
        return True
    except OSError:
        print("Unable to save high score.")
        return False


def load_high_score():
    try:
        with HIGH_SCORE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            score = data.get("high_score", 0)

            if type(score) is int and score >= 0:
                return score

        print("Invalid high score data. Starting at zero.")
        return 0

    except FileNotFoundError:
        save_high_score(0)
        return 0

    except (json.JSONDecodeError, OSError):
        print("Unable to load high score. Starting at zero.")
        return 0


high_score = load_high_score()


def show_inventory():
    print("\n₊˚ ✧ ━━━━⊱ Inventory ⊰━━━━ ✧ ₊˚")
    print(f"Session gold: {current_gold}")
    print(f"Rooms cleared: {rooms_cleared}/{len(rooms)}")
    print(f"All-time high score: {high_score}")


def show_room_map(outcome=None):
    print("\n₊˚ ✧ ━━━━⊱ Dungeon Map ⊰━━━━ ✧ ₊˚")
    print("[X] = Cleared | [>] = Current | [!] = Defeat | [ ] = Unexplored")

    for i, room in enumerate(rooms):
        if i < rooms_cleared:
            marker = "[X]"
        elif outcome == "defeat" and i == rooms_cleared:
            marker = "[!]"
        elif i == rooms_cleared and not game_over:
            marker = "[>]"
        else:
            marker = "[ ]"

        print(f"{marker} {room}")

        if i < len(rooms) - 1:
            print("    |")


def reset_run():
    global rooms_cleared, current_gold, last_run_gold, game_over

    rooms_cleared = 0
    current_gold = 0
    last_run_gold = 0
    game_over = False

    print("\n₊˚ ✧ ━━━━⊱ New Adventure ⊰━━━━ ✧ ₊˚")
    print("A new dungeon run is beginning!")
    print(f"Your destination is {rooms[0]}.")


def game_over_screen(outcome):
    global game_over, high_score, quit_requested

    game_over = True
    final_score = current_gold

    print("\n" + "=" * 40)

    if outcome == "defeat":
        print("          YOU WERE DEFEATED")
        print("=" * 40)
        print(f"Rooms cleared: {rooms_cleared}/{len(rooms)}")
        print(f"Gold lost: {last_run_gold}")
        print(f"Final score: {final_score} gold")
        print("Good try! Better luck next run.")

    elif outcome == "victory":
        print("          DUNGEON CLEARED!")
        print("=" * 40)
        print("You conquered every room!")
        print(f"Rooms cleared: {rooms_cleared}/{len(rooms)}")
        print(f"Final score: {final_score} gold")

    elif outcome == "cashout":
        print("             CASHED OUT")
        print("=" * 40)
        print(f"Rooms cleared: {rooms_cleared}/{len(rooms)}")
        print(f"Final score: {final_score} gold")

    # Update the all-time high score after a successful cash-out or victory.
    if outcome in ("victory", "cashout"):
        if final_score > high_score:
            if save_high_score(final_score):
                high_score = final_score
                print("\n₊˚ ✧ ━━━━⊱ NEW HIGH SCORE! ⊰━━━━ ✧ ₊˚")
                print(f"Your new record is {high_score} gold!")
            else:
                print("\nYour score could not be saved.")
                print(f"Previous high score: {high_score} gold")
        else:
            print("\nGood try!")
            print(f"Your all-time high score is still {high_score} gold.")

    else:
        print(f"All-time high score: {high_score} gold")

    # Display the dungeon map on victory and defeat screens.
    if outcome in ("victory", "defeat"):
        show_room_map(outcome)

    print("\n" + "=" * 40)

    while True:
        print("\n₊˚ ✧ ━━━━⊱ What Next? ⊰━━━━ ✧ ₊˚")
        print("1. Play Again")
        print("2. Return to Main Menu")
        print("3. Quit Game")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            reset_run()
            return

        elif choice == "2":
            # Reset the ended run so the player can start again from the menu.
            reset_run()
            print("Returning to the main menu...")
            return

        elif choice == "3":
            quit_requested = True
            print("Thanks for playing!")
            return

        else:
            print("Invalid choice. Enter 1, 2, or 3.")


def cash_out():
    if game_over:
        print("Your run has already ended.")
        return

    print("\n₊˚ ✧ ━━━━⊱ Cash Out ⊰━━━━ ✧ ₊˚")
    print(f"You currently have {current_gold} gold.")

    while True:
        confirm = input("Cash out and save your score? (y/n): ").strip().lower()

        if confirm in ("y", "yes"):
            game_over_screen("cashout")
            return

        elif confirm in ("n", "no"):
            print("Cash out cancelled. Keep exploring!")
            return

        else:
            print("Please enter y or n.")


def combat():
    global current_gold, last_run_gold

    player_roll = random.randint(1, 20)
    enemy_roll = random.randint(1, 20)

    print("\n₊˚ ✧ ━━━━⊱ Combat Room ⊰━━━━ ✧ ₊˚")
    print("An enemy appears!")
    print("1. Attack (+3 to your roll)")
    print("2. Defend (-5 to enemy roll, minimum 1)")

    while True:
        choice = input("Enter 1 or 2: ").strip()

        if choice in ("1", "2"):
            break

        print("Invalid choice. Please enter 1 or 2.")

    if choice == "1":
        player_roll += 3
        print("You attack!")

    else:
        enemy_roll = max(1, enemy_roll - 5)
        print("You defend!")

    print(f"Your final roll: {player_roll}")
    print(f"Enemy's final roll: {enemy_roll}")

    if player_roll > enemy_roll:
        current_gold += 10
        print(f"You defeated the enemy! +10 gold. Total: {current_gold}")
        return True

    elif player_roll < enemy_roll:
        print("You were defeated!")

        last_run_gold = current_gold
        current_gold = 0

        return False

    else:
        print("It's a draw! No gold earned.")
        print(f"Current gold: {current_gold}")
        return True


def random_room():
    global current_gold

    encounter = random.choices(
        ["combat", "treasure", "safe"],
        weights=[70, 10, 20],
        k=1
    )[0]

    if encounter == "combat":
        print("\nYou encountered a Combat Room!")
        return combat()

    elif encounter == "treasure":
        treasure_gold = random.randint(10, 30)
        current_gold += treasure_gold

        print("\n₊˚ ✧ ━━━━⊱ Treasure Room ⊰━━━━ ✧ ₊˚")
        print(f"You found {treasure_gold} gold!")
        print(f"Current gold: {current_gold}")

        return True

    else:
        print("\n₊˚ ✧ ━━━━⊱ Safe Room ⊰━━━━ ✧ ₊˚")
        print("There are no enemies here. Take a rest!")
        print(f"Current gold: {current_gold}")

        return True


def next_room():
    global rooms_cleared

    if game_over:
        print("Your run has ended. Start a new run to continue.")
        return

    if rooms_cleared >= len(rooms):
        print("You have already cleared the dungeon!")
        return

    print(f"\n₊˚ ✧ ━━━━⊱ {rooms[rooms_cleared]} ⊰━━━━ ✧ ₊˚")

    if random_room():
        rooms_cleared += 1

        print(f"Rooms cleared: {rooms_cleared}/{len(rooms)}")

        if rooms_cleared == len(rooms):
            game_over_screen("victory")

    else:
        game_over_screen("defeat")


def main():
    print("₊˚ ✧ ━━━━⊱ Dungeon Adventure ⊰━━━━ ✧ ₊˚")

    while not quit_requested:
        print("\n₊˚ ✧ ━━━━⊱ Main Menu ⊰━━━━ ✧ ₊˚")
        print("1. Enter Next Room")
        print("2. Dungeon Map")
        print("3. Inventory")
        print("4. Cash Out & Save Score")
        print("5. Quit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            next_room()

        elif choice == "2":
            show_room_map()

        elif choice == "3":
            show_inventory()

        elif choice == "4":
            cash_out()

        elif choice == "5":
            print("Thanks for playing!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
