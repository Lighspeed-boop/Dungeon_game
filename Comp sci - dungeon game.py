
import random
import json
from pathlib import Path

rooms_cleared = 0
current_gold = 0
directions = []
game_over = False


rooms = [
    "The Entrance",
    "Dungeon Floor 1",
    "Dungeon Floor 2",
    "Dungeon Floor 3",
    "Dungeon Exit",
    "Main Hall Floor 1"
    "Main Hall floor 2"
    "Main Hall floor 3"
    "Guarded doors"
    "Throne room"
]



HIGH_SCORE_FILE = Path("high_score.json")


def load_high_score():
    try:
        with HIGH_SCORE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)

        score = data.get("high_score", 0)

        if type(score) is int and score >= 0:
            return score

        return 0

    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return 0


def save_high_score(score):
    try:
        with HIGH_SCORE_FILE.open("w", encoding="utf-8") as file:
            json.dump({"high_score": score}, file, indent=4)

        return True

    except OSError:
        print("Unable to save high score.")
        return False


high_score = load_high_score()


def show_inventory():
    print("\n₊˚ ✧ ━━━━⊱ Inventory ⊰━━━━ ✧ ₊˚")
    print(f"Session gold: {current_gold}")
    print(f"Rooms cleared: {rooms_cleared}")
    print(f"All-time high score: {high_score}")


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



def combat():
    global current_gold

    print("\n₊˚ ✧ ━━━━⊱ Combat ⊰━━━━ ✧ ₊˚")
    print("1. Attack (+3 to your roll)")
    print("2. Defend (-5 to enemy roll)")

  
    while True:
        action = input("Choose your action (1 or 2): ")

        if action == "1" or action == "2":
            break

        else:
            print("Invalid choice! Please enter 1 or 2.")

    player_roll = random.randint(1, 20)
    enemy_roll = random.randint(1, 20)

   
    if action == "1":
        player_roll += 3
        print("You attacked! Your roll is increased by 3.")

    # Defend reduces the enemy's roll by 5
    elif action == "2":
        enemy_roll = max(1, enemy_roll - 5)
        print("You defended! Enemy roll reduced by 5.")

    print(f"Your final roll: {player_roll}")
    print(f"Enemy final roll: {enemy_roll}")

    if player_roll > enemy_roll:
        print("You won the fight!")
        current_gold += 10
        print("You earned 10 gold!")

    elif player_roll < enemy_roll:
        print("You lost the fight! Game Over.")
        current_gold = 0
        return False

    else:
        print("It's a draw! No gold awarded.")

    print(f"Current gold: {current_gold}")
    return True


def next_room():
    global rooms_cleared, game_over

    if game_over:
        print("\nYour run has ended. Start a new run to continue.")
        return

    if rooms_cleared < len(rooms):
        print(f"\nYou entered {rooms[rooms_cleared]}!")

        
        if combat():
            rooms_cleared += 1
            print(f"Rooms cleared: {rooms_cleared}")

            # Force a valid direction
            while True:
                direction = input(
                    "Which direction did you go? "
                    "(1 = left, 2 = right, 3 = straight): "
                ).lower().strip()

                if direction == "1" or direction == "left":
                    directions.append("left")
                    break

                elif direction == "2" or direction == "right":
                    directions.append("right")
                    break

                elif direction == "3" or direction == "straight":
                    directions.append("straight")
                    break

                else:
                    print(
                        "Invalid direction! Enter 1, 2, 3, "
                        "left, right, or straight."
                    )

        else:
            game_over = True
            print("Your dungeon run has ended.")
            print(f"Final rooms cleared: {rooms_cleared}")
            print(f"Gold lost: {current_gold}")
            print("Returning to the main menu...")

    else:
        print("\nYou have cleared the dungeon!")


def show_direction_map():
    print("\n₊˚ ✧ ━━━━⊱ Direction Map ⊰━━━━ ✧ ₊˚")

    if len(directions) == 0:
        print("No rooms explored yet.")

    else:
        print("Entrance", end="")

        for direction in directions:
            print(f" --> {direction}", end="")

        print()


def show_room_map():
    print("\n₊˚ ✧ ━━━━⊱ Dungeon Map ⊰━━━━ ✧ ₊˚")

    for i in range(len(rooms)):
        if i < rooms_cleared:
            print(f"[X] {rooms[i]}")

        elif i == rooms_cleared:
            print(f"[>] {rooms[i]}")

        else:
            print(f"[ ] {rooms[i]}")

        if i < len(rooms) - 1:
            print("     ↓")


# Main Menu
while True:
    print("\n₊˚ ✧ ━━━━⊱ Dungeon Menu ⊰━━━━ ✧ ₊˚")
    print("1. Enter Next Room")
    print("2. Show Map")
    print("3. Inventory")
    print("4. Cash Out & Save Score")
    print("5. Quit")

    choice = input("Choose: ").strip()

    if choice == "1":
        next_room()

    elif choice == "2":
        print("\n1. Direction Map")
        print("2. Dungeon Map")

        map_choice = input("Choose map: ").strip()

        if map_choice == "1":
            show_direction_map()

        elif map_choice == "2":
            show_room_map()

        else:
            print("Invalid map choice.")

    elif choice == "3":
        show_inventory()

    elif choice == "4":
        cash_out()

    elif choice == "5":
        print("Returning to main menu...")
        break

    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, or 5.")
