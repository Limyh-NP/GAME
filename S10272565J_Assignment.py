from random import randint

player = {}
game_map = []
fog = []

MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

SAVE_FILE = 'savefile.txt'

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
# TODO: Add your map loading code here (done)
def load_map(filename, map_struct):
    global MAP_WIDTH, MAP_HEIGHT
    with open(filename, 'r') as f:
        map_struct.clear()
        for line in f:
            row = list(line.rstrip('\n'))  #only strip newline, keep spaces
            if row:
                map_struct.append(row)

    MAP_HEIGHT = len(map_struct)
    MAP_WIDTH = min(len(row) for row in map_struct) if MAP_HEIGHT > 0 else 0

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    return

def initialize_game(game_map, fog, player):
    # initialize map
    load_map("level1.txt", game_map)

    # TODO: initialize fog (done)
    for x in range(MAP_HEIGHT):
        fog.append([])
        for y in range(MAP_WIDTH):
            fog[x].append("?")
    
    # TODO: initialize player
    #   You will probably add other entries into the player dictionary
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 0
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['name'] = ''
    player['maxslots'] = 10
    player['pickaxelevel'] = 1
    player['portal'] = (0,0)

    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fog
def draw_map(game_map, fog, player):
    print("+" + "-" * MAP_WIDTH + "+")
    for y in range(MAP_HEIGHT):
        row = "|"
        for x in range(MAP_WIDTH):
            if (x, y) == (player['x'], player['y']):
                row += "M"
            elif (x, y) == player['portal']:
                row += "P"
            elif fog[y][x]:
                row += "?"
            else:
                row += game_map[y][x]
        print(row + "|")
    print("+" + "-" * MAP_WIDTH + "+")
    return

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    print("+---+")
    for dy in range(-1, 2):
        row = "|"
        for dx in range(-1, 2):
            x = player['x'] + dx
            y = player['y'] + dy

            if 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                if (x, y) == (player['x'], player['y']):
                    row += "M"
                else:
                    row += game_map[y][x]  # Always show surroundings
            else:
                row += "#"
        print(row + "|")
    print("+---+")

# This function shows the information for the player
def show_information(player):
    print("\n----- Player Information -----")
    print(f"Name: {player['name']}")
    print(f"Current position: ({player['x']}, {player['y']})")
    print(f"Pickaxe level: {player['pickaxelevel']}")
    print(f"Gold: {player['gold']}")
    print(f"Silver: {player['silver']}")
    print(f"Copper: {player['copper']}")
    print(f"Load: {player['copper'] + player['silver'] + player['gold']} / {player['maxslots']}")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    print("------------------------------")
    return

# This function saves the game
def save_game(game_map, fog, player):
    with open(SAVE_FILE, 'w') as f:
        # Save player data
        for key, value in player.items():
            f.write(f"{key}:{value}\n")

        # Save fog data as a line of 0s and 1s per row, separated by |
        f.write("FOG:")
        for row in fog:
            line = ''.join(['1' if cell else '0' for cell in row])
            f.write(line + "|")  # Use '|' to separate rows
    print("Game saved.")
    
# This function loads the game
def load_game(game_map, fog, player):
    global MAP_WIDTH, MAP_HEIGHT
    load_map("level1.txt", game_map)

    fog_data = None
    player.clear()

    with open(SAVE_FILE, 'r') as f:
        for line in f:
            if line.startswith("FOG:"):
                fog_data = line[4:].strip().split("|")
            elif ':' in line:
                key, value = line.strip().split(":", 1)
                if key in ['x', 'y', 'copper', 'silver', 'gold', 'GP', 'day', 'steps', 'turns', 'max_load', 'pickaxe_level']:
                    player[key] = int(value)
                elif key == 'portal':
                    player[key] = eval(value)
                else:
                    player[key] = value

    # Restore fog from saved data
    if fog_data:
        fog.clear()
        for row in fog_data:
            if row:  # skip empty lines
                fog.append([cell == '1' for cell in row])

    # Clamp player position
    player['x'] = min(max(0, player['x']), MAP_WIDTH - 1)
    player['y'] = min(max(0, player['y']), MAP_HEIGHT - 1)

    print("Game loaded.")
    return True

def enter_mine():
    player['turns'] = TURNS_PER_DAY
    print(f"\n{'-'*50}\n{'DAY ' + str(player['day']+1):^50}\n{'-'*50}")

    while player['turns'] > 0:
        draw_view(game_map, fog, player)
        print(f"Turns left: {player['turns']}    Load: {player['copper'] + player['silver'] + player['gold']} / {player['maxslots']}    Steps: {player['steps']}")
        action = input("(WASD) to move | (M)ap | (I)nformation | (P)ortal | (Q)uit: ").strip().lower()

        if action == 'm':
            draw_map(game_map, fog, player)
        elif action == 'i':
            show_information(player)
        elif action == 'q':
            break
        elif action == 'p':
            print("You place your portal stone here and zap back to town.")
            player['portal'] = (player['x'], player['y'])
            sell_ore()
            player['day'] += 1
            return
        elif action in ['w', 'a', 's', 'd']:
            dx, dy = 0, 0
            if action == 'w': dy = -1
            if action == 's': dy = 1
            if action == 'a': dx = -1
            if action == 'd': dx = 1

            new_x = player['x'] + dx
            new_y = player['y'] + dy

            if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
                #check for border
                if 0 <= new_y < len(game_map) and 0 <= new_x < len(game_map[new_y]):
                    target_tile = game_map[new_y][new_x]
                else:
                    print("You can't move there.")
                    continue
                
                load = player['copper'] + player['silver'] + player['gold']

                if target_tile in mineral_names:
                    if load >= player['maxslots']:
                        print("You can't carry any more, so you can't go that way.")
                    else:
                        amount = 0
                        if target_tile == 'C':
                            amount = randint(1, 5)
                        elif target_tile == 'S':
                            amount = randint(1, 3)
                        elif target_tile == 'G':
                            amount = randint(1, 2)

                        actual = min(amount, player['maxslots'] - load)
                        player[mineral_names[target_tile]] += actual
                        print(f"You mined {actual} piece(s) of {mineral_names[target_tile]}.")
                        player['x'] = new_x
                        player['y'] = new_y
                        player['steps'] += 1
                        player['turns'] -= 1
                        clear_fog(fog, player)
                elif target_tile == 'T':
                    print("You returned to town.")
                    sell_ore()
                    player['day'] += 1
                    return
                else:
                    player['x'] = new_x
                    player['y'] = new_y
                    player['steps'] += 1
                    player['turns'] -= 1
                    clear_fog(fog, player)
            else:
                print("You can't move there.")
        else:
            print("Invalid action.")

    print("You are exhausted. You place your portal stone here and zap back to town.")
    player['portal'] = (player['x'], player['y'])
    sell_ore()
    player['day'] += 1

    
def sell_ore():
    total = 0
    for ore in ['copper', 'silver', 'gold']:
        qty = player[ore]
        if qty > 0:
            price = randint(prices[ore][0], prices[ore][1])
            gain = qty * price
            print(f"You sell {qty} {ore} ore for {gain} GP.")
            total += gain
            player[ore] = 0
    player['GP'] += total
    print(f"You now have {player['GP']} GP!")

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu(player):
    print(f"\nDAY {player['day'] + 1}")
    # TODO: Show Day (done)
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")
            

#--------------------------- MAIN GAME ---------------------------
game_state = 'main'
print("---------------- Welcome to Sundrop Caves! ----------------")
print("You spent all your money to get the deed to a mine, a small")
print("  backpack, a simple pickaxe and a magical portal stone.")
print()
print("How quickly can you get the 1000 GP you need to retire")
print("  and live happily ever after?")
print("-----------------------------------------------------------")

# TODO: The game!
while True:
        show_main_menu()
        choice = input("Your choice? ").strip().lower()

        if choice == 'n':
            initialize_game(game_map, fog, player)
            player['name'] = input("Greetings, miner! What is your name? ")
            print(f"Pleased to meet you, {player['name']}. Welcome to Sundrop Town!")

            while True:
                show_town_menu(player)
                town_choice = input("Your choice? ").strip().lower()
                if town_choice == 'q':
                    break
                elif town_choice == 'i':
                    show_information(player)
                elif town_choice == 'm':
                    draw_map(game_map, fog, player)
                elif town_choice == 'v':
                    save_game(game_map, fog, player)
                elif town_choice == 'e':
                    enter_mine()
                else:
                    print("Feature not yet implemented.")

        elif choice == 'l':
            if load_game(game_map, fog, player):
                print(f"Welcome back, {player['name']}!")
                while True:
                    show_town_menu(player)
                    town_choice = input("Your choice? ").strip().lower()
                    if town_choice == 'q':
                        break
                    elif town_choice == 'i':
                        show_information(player)
                    elif town_choice == 'm':
                        draw_map(game_map, fog, player)
                    elif town_choice == 'v':
                        save_game(game_map, fog, player)
                    elif town_choice == 'e':
                        enter_mine()
                    else:
                        print("Feature not yet implemented.")
        elif choice == 'q':
            print("Thanks for playing. Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == '__main__':
    game_state()