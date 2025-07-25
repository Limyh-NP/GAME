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

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    with open(filename, 'r') as map_file:
        global MAP_WIDTH
        global MAP_HEIGHT
    
    map_struct.clear()
    
    # TODO: Add your map loading code here (done)
    map_file = map_file.read
    map_struct = map_file.split('\n')
    for i in range(len(map_struct)):
            map_struct[i] = list(map_struct[i])
    
    MAP_WIDTH = len(map_struct[0])
    MAP_HEIGHT = len(map_struct)

    map_file.close()

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
    player['backpackslots'] = 10
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
            if (x, y) == (player['x'], player['y']):
                row += "M"
            elif 0 <= y < MAP_HEIGHT and 0 <= x < MAP_WIDTH:
                row += game_map[y][x] if not fog[y][x] else "?"
            else:
                row += "#"
        print(row + "|")
    print("+---+")
    return

# This function shows the information for the player
def show_information(player):
    print("\n----- Player Information -----")
    print(f"Name: {player['name']}")
    print(f"Current position: ({player['x']}, {player['y']})")
    print(f"Pickaxe level: {player['pickaxe_level']}")
    print(f"Gold: {player['gold']}")
    print(f"Silver: {player['silver']}")
    print(f"Copper: {player['copper']}")
    print(f"Load: {player['copper'] + player['silver'] + player['gold']} / {player['max_load']}")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    print("------------------------------")
    return

# This function saves the game
def save_game(game_map, fog, player):
    # save map
    # save fog
    # save player
    return
        
# This function loads the game
def load_game(game_map, fog, player):
    # load map
    # load fog
    # load player
    return

def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(H)igh scores")
    print("(Q)uit")
    print("------------------")

def show_town_menu(player):
    print(f"\nDAY {player['day']}")
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
    

