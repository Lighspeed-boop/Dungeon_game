
import random
import json
from pathlib import Path

rooms_cleared = 0
current_gold = 0
game_over = False

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


# Save the all-time high score
def save_high_score(score):
    try:
        with HIGH_SCORE_FILE.open("w", encoding="utf-8") as file:
            json.dump({"high_score": score}, file, indent=4)
        return True
    except OSError:
        print("Unable to save high score.")
        return False


# Load the all-time high score
def load_high_score():
    try:
        with HIGH_SCORE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            print("Invalid high score data. Starting at zero.")
            return 0

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


# Display inventory and score information
def show_inventory():
    print("\n₊˚ ✧ ━━━━⊱ Inventory ⊰━━━━ ✧ ₊˚")
    print(f"Session gold: {current_gold}")
    print(f"Rooms cleared: {rooms_cleared}")
    print(f"All-time high score: {high_score}")


# Cash out and save the score if it beats the record
def cash_out():
    global high_score, game_over

    if game_over:
        print("Your run has already ended.")
        return

    print("\n₊˚ ✧ ━━━━⊱ Cash Out ⊰━━━━ ✧ ₊˚")
    print(f"You currently have {current_gold} gold.")

    while True:
        confirm = input(
            "Cash out and save your score? (y/n): "
        ).strip().lower()

        if confirm in ("y", "yes"):
            break
        elif confirm in ("n", "no"):
            print("Cash out cancelled. Keep exploring!")
            return
        else:
            print("Please enter y or n.")

    if current_gold > high_score:
        if save_high_score(current_gold):
            high_score = current_gold
            print("Congratulations! New all-time high score!")
        else:
            print("Your score could not be saved.")
    else:
        print(f"Your best score remains {high_score} gold.")

    game_over = True

    print(f"Final score: {current_gold} gold.")
    print("Your dungeon run has ended.")


# Combat system
def combat():
    global current_gold

    player_roll = random.randint(1, 20)
    enemy_roll = random.randint(1, 20)

    print("\nAn enemy appears!")
    print("Choose your action:")
    print("1. Attack (+3 to your roll)")
    print("2. Defend (-5 to the enemy's roll)")

    while True:
        choice = input("Enter 1 or 2: ").strip()

        if choice in ("1", "2"):
            break

        print("Invalid choice. Please enter 1 or 2.")

    if choice == "1":
        player_roll += 3
        print("You attack! Your roll increases by 3.")
    else:
        enemy_roll = max(1, enemy_roll - 5)
        print("You defend! The enemy's roll decreases by 5.")

    print(f"Your final roll: {player_roll}")
    print(f"Enemy's final roll: {enemy_roll}")

    if player_roll > enemy_roll:
        print("You defeated the enemy!")
        current_gold += 10
        print(f"You earned 10 gold! Current gold: {current_gold}")
        return True

    elif player_roll < enemy_roll:
        print("You were defeated!")
        print("You lose all your session gold.")
        current_gold = 0
        return False

    else:
        print("It's a draw! No gold earned.")
        print(f"Current gold: {current_gold}")
        return True


# Randomly select a combat, treasure, or safe room
def random_room():
    global current_gold

    encounter = random.choices(
        ["combat", "treasure", "safe"],
        weights=[70, 10, 20],
        k=1
    )[0]

    if encounter == "combat":
        print("\nYou encountered a Combat Room!")
        print("An enemy blocks your path!")
        return combat()

    elif encounter == "treasure":
        treasure_gold = random.randint(10, 30)

        print("\n₊˚ ✧ ━━━━⊱ Treasure Room ⊰━━━━ ✧ ₊˚")
        print("You discovered a hidden treasure chest!")
        print(f"You found {treasure_gold} gold!")

        current_gold += treasure_gold

        print(f"Current gold: {current_gold}")
        return True

    else:
        print("\n₊˚ ✧ ━━━━⊱ Safe Room ⊰━━━━ ✧ ₊˚")
        print("You found a peaceful room.")
        print("There are no enemies here. Take a rest!")
        print(f"Current gold: {current_gold}")
        return True


# Enter the next room
def next_room():
    global rooms_cleared, game_over

    if game_over:
        print("\nYour run has ended. Cash out or quit.")
        return

    if rooms_cleared < len(rooms):
        print(f"\nYou entered {rooms[rooms_cleared]}!")

        if random_room():
            rooms_cleared += 1
            print(f"Rooms cleared: {rooms_cleared}")

            if rooms_cleared == len(rooms):
                print("\nYou have cleared every room!")
                print("You can now cash out your gold from the main menu.")

        else:
            game_over = True
            print("\nYour dungeon run has ended.")
            print(f"Final rooms cleared: {rooms_cleared}")
            print("Your session gold was lost.")
            print("Returning to the main menu...")

    else:
        print("\nYou have cleared the dungeon!")
        print("You can cash out your gold from the main menu.")


# Display the dungeon room map
def show_room_map():
    print("\n₊˚ ✧ ━━━━⊱ Dungeon Map ⊰━━━━ ✧ ₊˚")

    for i, room in enumerate(rooms):
        if i < rooms_cleared:
            marker = "[X]"
        elif i == rooms_cleared and not game_over:
            marker = "[>]"
        else:
            marker = "[ ]"

        print(f"{marker} {room}")

        if i < len(rooms) - 1:
            print("    |")


# Main menu
def main():
    print("₊˚ ✧ ━━━━⊱ Dungeon Adventure ⊰━━━━ ✧ ₊˚")

    while True:
        print("\n========== MAIN MENU ==========")
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
