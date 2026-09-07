rooms_cleared = 0

# Map 1 - Direction history
directions = []


# Map 2 - Named rooms
rooms = [
    "Entrance",
    "Dungeon Floor 1",
    "Dungeon Floor 2",
    "Dungeon Floor 3",
    "Dungeon Exit",
    "Main Hall Floor 1"
]


def next_room():
    global rooms_cleared

    if rooms_cleared < len(rooms):
        rooms_cleared += 1

        print(f"\nYou entered {rooms[rooms_cleared - 1]}!")
        print(f"Rooms cleared: {rooms_cleared}")

        # Add a random/example direction to the map
        direction = input("Which direction did you go? (left/right/straight): ").lower()

        if direction == "left" or direction == "right" or direction == "straight":
            directions.append(direction)
        else:
            print("Invalid direction. It was not added to the map.")

    else:
        print("\nYou have cleared the dungeon!")


def show_direction_map():
    print("\n===== DIRECTION MAP =====")

    if len(directions) == 0:
        print("No rooms explored yet.")
    else:
        print("Entrance", end="")

        for direction in directions:
            print(f" --> {direction}", end="")

        print()


def show_room_map():
    print("\n===== DUNGEON MAP =====")

    for i in range(len(rooms)):

        if i < rooms_cleared:
            print(f"[X] {rooms[i]}")

        elif i == rooms_cleared:
            print(f"[>] {rooms[i]}")

        else:
            print(f"[ ] {rooms[i]}")

        if i < len(rooms) - 1:
            print("     ↓")


while True:
    print("\n1. Enter Next Room")
    print("2. Show Map")
    print("3. Quit")

    choice = input("Choose: ")

    if choice == "1":
        next_room()

    elif choice == "2":
        print("\n1. Direction Map")
        print("2. Dungeon Map")

        map_choice = input("Choose map: ")

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
        print("Invalid choice.")