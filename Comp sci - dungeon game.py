
import random

rooms_cleared = 0
current_gold = 0
directions = []
game_over = False

# Map 2 - Named rooms
rooms = [
    "Entrance",
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


# Component 2 - Combat System
def combat():
    global current_gold

    print("\n₊˚ ✧ ━━━━⊱ Combat ⊰━━━━ ✧ ₊˚")
    print("1. Attack (+3 to your roll)")
    print("2. Defend (-5 to enemy roll)")

    # Force a valid combat choice
    while True:
        action = input("Choose your action (1 or 2): ")

        if action == "1" or action == "2":
            break
        else:
            print("Invalid choice! Please enter 1 or 2.")

    player_roll = random.randint(1, 20)
    enemy_roll = random.randint(1, 20)

    # Attack gives the player +3
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

        # Fight before clearing the room
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
    print("\n1. Enter Next Room")
    print("2. Show Map")
    print("3. Quit")

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
        print("Returning to main menu...")
        break

    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
