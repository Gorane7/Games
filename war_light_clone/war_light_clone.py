import pygame
import random
import math


clock = pygame.time.Clock()
pygame.font.init()

#CONSTANTS
screen_size = (500,600)
game_name = "WarLight"
field_size = 5
square_size = 100
field_bar_percentage = 0.01
space_between_elements = 1
players = 2
spawn_locations = [[2, 0], [2, 4]]
roads = [[[0, 1, 1, 0], [1, 0, 1, 0], [1, 1, 1, 0], [1, 0, 1, 0], [1, 1, 0, 0]], [[0, 1, 0, 1], [0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 0], [0, 1, 0, 1]], [[0, 1, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0], [1, 1, 0, 1], [0, 1, 0, 1]], [[0, 1, 0, 1], [0, 0, 1, 1], [1, 1, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1]], [[0, 0, 1, 1], [1, 0, 1, 0], [1, 0, 1, 1], [1, 0, 1, 0], [1, 0, 0, 1]]]
#players = 4
#spawn_locations = [[2, 0], [4, 2], [2, 4], [0, 2]]
AI = [1,0,0,0,0]
game_map_location = [0.0, 100.0]
end_turn_button_location = [0.0, 0.0]
end_turn_button_size = [100.0, 25.0]
confirmation_button_size = [200.0, 50.0]
confirmation_button_location = [screen_size[0]/2 - confirmation_button_size[0]/2, screen_size[1]/2 - confirmation_button_size[1]/2]
start_game_button_size = [200.0, 50.0]
start_game_button_location = [screen_size[0]/2 - start_game_button_size[0]/2, screen_size[1]/2 - start_game_button_size[1]/2]
warrior_chance = 0.5
bowman_chance = 0.25

#COLORS
green = (0,255,0)
blue = (0,0,255)
red = (255,0,0)
grey = (127,127,127)
black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)
dark_grey = (63,63,63)

#VARIABLES
current_screen = "Start menu"
game_display = None
game_exit = False
game_field = None
current_turn = 1
orders = []

#BUTTONS
end_turn_button = None
confirmation_button = None
start_game_button = None

#HELPER VARIABLES
player_colours = [grey, red, blue, green, yellow]
players_in_game = []
for i in range(0,players+1):
    players_in_game.append(1)
players_in_game[0] = 0

class Game_field():
    def __init__(self):
        self.tiles = []
        for x in range(0,field_size):
            sub_field = []
            for y in range(0,field_size):
                sub_field.append(Game_tile([x,y]))
            self.tiles.append(sub_field)
        self.initial_owners()
        self.orders = []
        self.current_order_input_tiles = []
        self.current_order_input_units = []
        self.current_unit_input = 0
        self.current_unit_input_amount = 0

    def initial_owners(self):
        for i in range(0,players):
            self.give_field_to_player(i+1, spawn_locations[i][0], spawn_locations[i][1])
            self.tiles[spawn_locations[i][0]][spawn_locations[i][1]].army.add_unit("Bowman", 1)

    def clicked_interactable(self):
        x1 = self.current_order_input_tiles[0]
        y1 = self.current_order_input_tiles[1]
        x2 = self.current_order_input_tiles[2]
        y2 = self.current_order_input_tiles[3]
        direction = mod_to_number(x2-x1, y2-y1)
        previous_order_size = self.tiles[x1][y1].order_sum()
        warriors_available = self.tiles[x1][y1].army.warrior_count - previous_order_size[0] + self.current_order_input_units[0]
        bowmen_available = self.tiles[x1][y1].army.bowman_count - previous_order_size[1] + self.current_order_input_units[1]
        warriors = min(warriors_available, self.current_order_input_units[0])
        bowmen = min(bowmen_available, self.current_order_input_units[1])
        self.tiles[x1][y1].orders[direction].units[0] = warriors
        self.tiles[x1][y1].orders[direction].units[1] = bowmen
        self.tiles[x1][y1].orders[direction].unit_sum = warriors + bowmen
        self.tiles[x1][y1].orders[direction].player = current_turn
        self.current_order_input_tiles = []
        self.current_order_input_units = []

    def press_key(self, key):
        x1 = self.current_order_input_tiles[0]
        y1 = self.current_order_input_tiles[1]
        x2 = self.current_order_input_tiles[2]
        y2 = self.current_order_input_tiles[3]
        direction = mod_to_number(x2-x1, y2-y1)
        if is_int(key.unicode):
            self.current_unit_input_amount = int(str(self.current_unit_input_amount) + str(key.unicode))
            self.tiles[x1][y1].orders[direction].units[self.current_unit_input] = self.current_unit_input_amount
        elif key.unicode == "q":
            if self.current_unit_input == 0:
                self.current_unit_input = 1
                self.current_order_input_units.append(self.current_unit_input_amount)
            else:
                self.current_unit_input = 0
                self.current_order_input_units.append(self.current_unit_input_amount)
                self.clicked_interactable()
                deactivate_all_tiles()
            self.current_unit_input_amount = 0
        elif key.unicode == "a":
            self.current_order_input_units.append(self.tiles[self.current_order_input_tiles[0]][self.current_order_input_tiles[1]].army.warrior_count)
            self.current_order_input_units.append(self.tiles[self.current_order_input_tiles[0]][self.current_order_input_tiles[1]].army.bowman_count)
            self.tiles[x1][y1].orders[direction].units[0] = self.tiles[self.current_order_input_tiles[0]][self.current_order_input_tiles[1]].army.warrior_count
            self.tiles[x1][y1].orders[direction].units[1] = self.tiles[self.current_order_input_tiles[0]][self.current_order_input_tiles[1]].army.bowman_count
            self.current_unit_input = 0
            self.clicked_interactable()
            deactivate_all_tiles()
            self.current_unit_input_amount = 0

    def get_orders(self):
        for y in range(0,field_size):
            for x in range(0,field_size):
                for i in range(0,4):
                    if self.tiles[x][y].orders[i].unit_sum != 0:
                        self.orders.append(self.tiles[x][y].orders[i])

    def resolve_orders(self):
        self.get_orders()
        while len(self.orders) != 0:
            order = random.randint(0,len(self.orders)-1)
            if self.orders[order].player == self.tiles[self.orders[order].x][self.orders[order].y].owner:
                warriors_in_tile = self.tiles[self.orders[order].x][self.orders[order].y].army.warrior_count
                bowmen_in_tile = self.tiles[self.orders[order].x][self.orders[order].y].army.bowman_count
                warriors = min(warriors_in_tile, self.orders[order].units[0])
                bowmen = min(bowmen_in_tile, self.orders[order].units[1])
                x, y = number_to_mod(self.orders[order].direction)
                attack_x = self.orders[order].x + x
                attack_y = self.orders[order].y + y
                if self.orders[order].player != self.tiles[attack_x][attack_y].owner:
                    this_battle = Battle(Army(warriors, bowmen), self.tiles[attack_x][attack_y].army)
                    self.tiles[attack_x - x][attack_y - y].army.remove_unit("Warrior", this_battle.casualties[0])
                    self.tiles[attack_x - x][attack_y - y].army.remove_unit("Bowman", this_battle.casualties[1])
                    if this_battle.victory:
                        self.give_field_to_player(self.orders[order].player, attack_x, attack_y)
                        self.tiles[attack_x - x][attack_y - y].army.remove_unit("Warrior", warriors - this_battle.casualties[0])
                        self.tiles[attack_x - x][attack_y - y].army.remove_unit("Bowman", bowmen - this_battle.casualties[1])
                        self.tiles[attack_x][attack_y].army.add_unit("Warrior", warriors - this_battle.casualties[0])
                        self.tiles[attack_x][attack_y].army.add_unit("Bowman", bowmen - this_battle.casualties[1])
                else:
                    self.tiles[attack_x - x][attack_y - y].army.remove_unit("Warrior", warriors)
                    self.tiles[attack_x - x][attack_y - y].army.remove_unit("Bowman", bowmen)
                    self.tiles[attack_x][attack_y].army.add_unit("Warrior", warriors)
                    self.tiles[attack_x][attack_y].army.add_unit("Bowman", bowmen)
            self.tiles[self.orders[order].x][self.orders[order].y].orders[self.orders[order].direction] = Order(self.tiles[self.orders[order].x][self.orders[order].y].location, [0,0], self.tiles[self.orders[order].x][self.orders[order].y].owner, self.orders[order].direction)
            del self.orders[order]

    def give_field_to_player(self, player, x, y):
        previous_owner = self.tiles[x][y].owner
        self.tiles[x][y].owner = player
        self.check_if_has_land(previous_owner)
        
        if previous_owner != 0:
            self.remove_sight_of_previous_owner(previous_owner, x, y)
        self.tiles[x][y].seen_by_players[player] = 1
        if y-1 != -1:
            if self.tiles[x][y].roads[0] == 1:
                self.tiles[x][y-1].seen_by_players[player] = 1
        if x+1 != 5:
            if self.tiles[x][y].roads[1] == 1:
                self.tiles[x+1][y].seen_by_players[player] = 1
        if y+1 != 5:
            if self.tiles[x][y].roads[2] == 1:
                self.tiles[x][y+1].seen_by_players[player] = 1
        if x-1 != -1:
            if self.tiles[x][y].roads[3] == 1:
                self.tiles[x-1][y].seen_by_players[player] = 1

    def remove_sight_of_previous_owner(self, player, x, y):
        self.tiles[x][y].seen_by_players[player] = check_visibility(x, y, player)
        if y-1 != -1:
            if self.tiles[x][y].roads[0] == 1:
                self.tiles[x][y-1].seen_by_players[player] = check_visibility(x, y-1, player)
        if x+1 != 5:
            if self.tiles[x][y].roads[1] == 1:
                self.tiles[x+1][y].seen_by_players[player] = check_visibility(x+1, y, player)
        if y+1 != 5:
            if self.tiles[x][y].roads[2] == 1:
                self.tiles[x][y+1].seen_by_players[player] = check_visibility(x, y+1, player)
        if x-1 != -1:
            if self.tiles[x][y].roads[3] == 1:
                self.tiles[x-1][y].seen_by_players[player] = check_visibility(x-1, y, player)

    def check_if_has_land(self, player):
        has_land = False
        for y in range(0,field_size):
            for x in range(0,field_size):
                if self.tiles[x][y].owner == player:
                    has_land = True
                    break
        if not has_land:
            eliminate(player)

class Order():
    def __init__(self, location, units, player, direction):
        self.x = location[0]
        self.y = location[1]
        self.units = units
        self.unit_sum = 0
        for i in range(0,len(units)):
            self.unit_sum += self.units[i]
        self.player = player
        self.direction = direction

    def __str__(self):
        location = "Coordinates: " + str([self.x, self.y]) + str("| ")
        direction = "Direction: " + str(self.direction) + str("| ")
        player = "Player: " + str(self.player) + str("| ")
        warriors = "Warriors: " + str(self.units[0]) + str("| ")
        bowmen = "Bowmen: " + str(self.units[1])
        return location + direction + player + warriors + bowmen
    

class Game_tile():
    def __init__(self, location):
        self.roads = roads[location[0]][location[1]]
        #self.roads = [0, 1, 1, 1]
        self.location = location
        self.owner = 0
        self.seen_by_players = []
        for i in range(0,players+1):
            self.seen_by_players.append(0)
        self.army = Army(1, 0)
        self.active = False
        self.orders = []
        for i in range(0,4):
            self.orders.append(Order(self.location, [0,0], self.owner, i))

    def move(self, direction):
        if self.army.exists():
            self.move_armies[direction] = self.army
            self.army = Army(0, 0)

    def order_sum(self):
        return_sum = [0,0]
        for i in range(0,4):
            return_sum[0] += self.orders[i].units[0]
            return_sum[1] += self.orders[i].units[1]
        return return_sum
        

class Unit():
    def __init__(self, hit_chance, unit_type):
        self.hit_chance = hit_chance
        self.unit_type = unit_type

    def attack(self, army_to_attack):
        army = army_to_attack
        attack_roll = random.uniform(0.0, 1.0)
        if attack_roll < self.hit_chance:
            army.kill_random()
            return army, True
        else:
            return army, False

class Warrior(Unit):
    def __init__(self):
        Unit.__init__(self, warrior_chance, "Warrior")

class Bowman(Unit):
    def __init__(self):
        Unit.__init__(self, bowman_chance, "Bowman")

class Army():
    def __init__(self, warrior_amount, bowman_amount):
        self.units = []
        self.warrior_count = warrior_amount
        self.bowman_count = bowman_amount
        for i in range(0,warrior_amount):
            self.units.append(Warrior())
        for i in range(0,bowman_amount):
            self.units.append(Bowman())

    def kill_random(self):
        to_kill = random.randint(0,len(self.units)-1)
        self.remove_count(to_kill)
        del self.units[to_kill]

    def remove_count(self, to_kill):
        if self.units[to_kill].unit_type == "Warrior":
            self.warrior_count -= 1
        elif self.units[to_kill].unit_type == "Bowman":
            self.bowman_count -= 1

    def move(self, field, units, x, y):
        this_field = field
        self.remove_unit("Warrior", units[0])
        self.remove_unit("Bowman", units[1])
        this_field[x][y].army.add_unit("Warrior", units[0])
        this_field[x][y].army.add_unit("Bowman", units[1])

    def remove_unit(self, unit_type, amount):
        if unit_type == "Warrior":
            self.warrior_count -= amount
        elif unit_type == "Bowman":
            self.bowman_count -= amount
        for i in range(0,amount):
            self.kill_unit(unit_type)

    def kill_unit(self, unit_type):
        for i in range(0,len(self.units)):
            if self.units[i].unit_type == unit_type:
                del self.units[i]
                break

    def add_unit(self, unit_type, amount):
        if unit_type == "Warrior":
            for i in range(0,amount):
                self.units.append(Warrior())
                self.warrior_count += 1
        elif unit_type == "Bowman":
            for i in range(0,amount):
                self.units.append(Bowman())
                self.bowman_count += 1

    def exists(self):
        if len(self.units) > 0:
            return True
        return False
            

    def order(self, direction):
        ordered_units = self.order_sum()
        warriors = self.warrior_count-ordered_units[0]
        bowmen = self.bowman_count-ordered_units[1]
        self.orders[direction][0] += warriors
        self.orders[direction][1] += bowmen
        return warriors, bowmen
        

class Battle():
    def __init__(self, attackers, defenders):
        self.initial_attacking_units = [attackers.warrior_count, attackers.bowman_count]
        self.initial_defending_units = [defenders.warrior_count, defenders.bowman_count]
        self.attackers = attackers
        self.defenders = defenders
        self.defenders = self.bowmen_attack(self.attackers, self.defenders)
        self.attackers = self.bowmen_attack(self.defenders, self.attackers)
        self.attackers, self.defenders = self.fight(self.attackers, self.defenders)
        if  not self.defenders.exists():
            self.victory = True
        else:
            self.victory = False
        self.casualties = [self.initial_attacking_units[0] - self.attackers.warrior_count, self.initial_attacking_units[1] - self.attackers.bowman_count]
        self.defender_casualties = [self.initial_defending_units[0] - self.defenders.warrior_count, self.initial_defending_units[1] - self.defenders.bowman_count]

    def bowmen_attack(self, attacking, defending):
        this_attacking = attacking
        this_defending = defending
        for i in range(0,len(this_attacking.units)):
            if this_attacking.units[i].unit_type == "Bowman":
                if this_defending.exists():
                    this_defending, success = this_attacking.units[i].attack(this_defending)
                else:
                    break
        return this_defending

    def fight(self, attacking, defending):
        this_attacking = attacking
        this_defending = defending
        size_a = len(this_attacking.units)
        size_d = len(this_defending.units)
        size = size_a + size_d
        mod_size = size
        for i in range(0,size):
            if not this_attacking.exists() or not this_defending.exists():
                break
            attacker = random.randint(0,mod_size-1)
            if attacker < size_a:
                this_defending, success = this_attacking.units[attacker].attack(this_defending)
                if success:
                    mod_size -= 1
                    size_d -= 1
            else:
                this_attacking, success = this_defending.units[attacker-size_a].attack(this_attacking)
                if success:
                    mod_size -= 1
                    size_a -= 1
            
        return this_attacking, this_defending
        

class Button():
    def __init__(self, text, colour, back_ground_colour, x, y, x_length, y_length):
        self.text_str = text
        self.colour = colour
        self.x = x
        self.y = y
        self.x_length = x_length
        self.y_length = y_length
        self.font = pygame.font.SysFont(None, 30)
        self.text = self.font.render(self.text_str, True, self.colour)
        self.back_ground_colour = back_ground_colour

    def blit_button(self):
        game_display.blit(self.text, [self.x, self.y])

    def draw_back_ground(self):
        game_display.fill(self.back_ground_colour, rect=[self.x, self.y, self.x_length, self.y_length])

    def draw_button(self):
        self.draw_back_ground()
        self.blit_button()

    def in_button(self, coordinates):
        if coordinates[0] >= self.x and coordinates[0] <= self.x + self.x_length and coordinates[1] >= self.y and coordinates[1] <= self.y + self.y_length:
            return True
        return False

def game_setup():
    pygame.init()
    start_menu_buttons()
    display = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(game_name)
    return display

def map_setup():
    global game_field
    
    game_field = Game_field()

def battle_simulator(times, attackers, defenders):
    attacker_casualties = [0,0]
    defender_casualties = [0,0]
    for i in range(0,times):
        this_battle = Battle(Army(attackers[0], attackers[1]), Army(defenders[0], defenders[1]))
        attacker_casualties[0] += this_battle.casualties[0]
        attacker_casualties[1] += this_battle.casualties[1]
        defender_casualties[0] += this_battle.defender_casualties[0]
        defender_casualties[1] += this_battle.defender_casualties[1]
    attacker_casualties[0] = attacker_casualties[0] / times
    attacker_casualties[1] = attacker_casualties[1] / times
    defender_casualties[0] = defender_casualties[0] / times
    defender_casualties[1] = defender_casualties[1] / times
    print(attacker_casualties)
    print(defender_casualties)
        

def eliminate(player):
    global players_in_game
    players_in_game[player] = 0
    check_if_game_over()

def check_if_game_over():
    players_left = 0
    for i in range(0,len(players_in_game)):
        players_left += players_in_game[i]
    if players_left == 1:
        game_over()

def game_over():
    for i in range(0,len(players_in_game)):
        if players_in_game[i] == 1:
            victory(i)
            break

def victory(player):
    print("Player " + str(player) + " wins!!!")

def check_visibility(x, y, player):
    if game_field.tiles[x][y].owner == player:
        return 1
    if y-1 != -1:
        if game_field.tiles[x][y].roads[0] == 1:
            if game_field.tiles[x][y-1].owner == player:
                return 1
    if x+1 != 5:
        if game_field.tiles[x][y].roads[1] == 1:
            if game_field.tiles[x+1][y].owner == player:
                return 1
    if y+1 != 5:
        if game_field.tiles[x][y].roads[2] == 1:
            if game_field.tiles[x][y+1].owner == player:
                return 1
    if x-1 != -1:
        if game_field.tiles[x][y].roads[3] == 1:
            if game_field.tiles[x-1][y].owner == player:
                return 1
    return 0

def end_turn():
    global current_turn
    global current_screen
    deactivate_all_tiles()
    current_turn +=1
    if current_turn > players:
        game_field.resolve_orders()
        current_turn = 1
        add_units()
    if players_in_game[current_turn] == 0:
        end_turn()
    if not AI[current_turn]:
        confirmation_buttons()
        current_screen = "Confirmation"

def resolve_orders():
    global orders
    global game_field
    while len(orders) > 0:
        order = random.randint(0,len(orders)-1)
        if orders[order][4] == game_field[orders[order][1]][orders[order][2]].owner:
            actual_units = []
            
            if game_field[orders[order][1]][orders[order][2]].army.warrior_count >= orders[order][0][0]:
                actual_units.append(orders[order][0][0])
            else:
                actual_units.append(game_field[orders[order][1]][orders[order][2]].army.warrior_count)
            
            if game_field[orders[order][1]][orders[order][2]].army.bowman_count >= orders[order][0][1]:
                actual_units.append(orders[order][0][1])
            else:
                actual_units.append(game_field[orders[order][1]][orders[order][2]].army.bowman_count)

            mod_x, mod_y = number_to_mod(orders[order][3])
            if game_field[orders[order][1] + mod_x][orders[order][2] + mod_y].owner != orders[order][4]:
                this_battle = Battle(Army(actual_units[0], actual_units[1]), game_field[orders[order][1] + mod_x][orders[order][2] + mod_y].army)
                if this_battle.victory:
                    game_field = give_field_to_player(game_field, orders[order][1] + mod_x, orders[order][2] + mod_y, orders[order][4])
                    game_field[orders[order][1] + mod_x][orders[order][2] + mod_y].army = this_battle.attackers
                    #Futur bug, of men replicating after battle
            else:
                game_field = game_field[orders[order][1]][orders[order][2]].army.move(game_field, [actual_units[0], actual_units[1]], orders[order][1] + mod_x, orders[order][2] + mod_y)
            game_field[orders[order][1]][orders[order][2]].army.orders[orders[order][4]] = [0,0]
            del orders[order]
            
            

def add_units():
    global game_field
    for y in range(0,field_size):
        for x in range(0,field_size):
            game_field.tiles[x][y].army.add_unit("Warrior", 1)
            if game_field.tiles[x][y].owner != 0:
                game_field.tiles[x][y].army.add_unit("Bowman", 1)

def in_map_area(coordinates):
    if coordinates[0] > game_map_location[0] and coordinates[0] < game_map_location[0] + field_size*square_size and coordinates[1] > game_map_location[1] and coordinates[1] < game_map_location[1] + field_size*square_size:
        return True
    return False

def check_active():
    for y in range(0,field_size):
        for x in range(0,field_size):
            if game_field.tiles[x][y].active:
                return True
    return False

def check_adjacent_active(x,y):
    if x != 0:
        if game_field.tiles[x][y].roads[3] == 1:
            if game_field.tiles[x-1][y].active:
                return True
    if x != 4:
        if game_field.tiles[x][y].roads[1] == 1:
            if game_field.tiles[x+1][y].active:
                return True
    if y != 0:
        if game_field.tiles[x][y].roads[0] == 1:
            if game_field.tiles[x][y-1].active:
                return True
    if y != 4:
        if game_field.tiles[x][y].roads[2] == 1:
            if game_field.tiles[x][y+1].active:
                return True
    return False

def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def get_active_tile():
    for y in range(0,field_size):
        for x in range(0,field_size):
            if game_field.tiles[x][y].active:
                return x, y

def attack_tile(x, y):
    global game_field
    x_d = x
    y_d = y
    x_a, y_a = get_active_tile()
    this_battle = Battle(game_field[x_a][y_a].army, game_field[x_d][y_d].army)
    if this_battle.victory:
        game_field = give_field_to_player(game_field, x_d, y_d, current_turn)
    deactivate_all_tiles()

def move_troops(x, y):
    global game_field
    x_dest = x
    y_dest = y
    x_dep, y_dep = get_active_tile()
    game_field[x_dep][y_dep].army.move(x_dest, y_dest)
    deactivate_all_tiles()

def deactivate_all_tiles():
    global game_field
    for y in range(0,field_size):
        for x in range(0,field_size):
            game_field.tiles[x][y].active = False

def mod_to_number(x, y):
    if x == 0 and y == -1:
        return 0
    if x == 1 and y == 0:
        return 1
    if x == 0 and y == 1:
        return 2
    if x == -1 and y == 0:
        return 3

def number_to_mod(direction):
    if direction == 0:
        return 0, -1
    if direction == 1:
        return 1, 0
    if direction == 2:
        return 0, 1
    if direction == 3:
        return -1, 0

def add_order(x, y, units, direction, player):
    global orders
    for i in range(0,len(orders)):
        if orders[i][1] == x and orders[i][2] == y and orders[i][3] == direction:
            for j in range(0,len(units)):
                orders[i][0][j] += units[j]
            return
    orders.append([units, x, y, direction, player])

def click_tile(x, y):
    currently_active = check_active()
    if currently_active:
        adjacent_active = check_adjacent_active(x, y)
        if adjacent_active:
            xa, ya = get_active_tile()
            direction = mod_to_number(x-xa, y-ya)
            game_field.tiles[xa][ya].orders[direction].unit_sum = 1
            game_field.current_order_input_tiles = [xa, ya, x, y]
            game_field.current_unit_input = 0
        else:
            deactivate_all_tiles()
    else:
        if game_field.tiles[x][y].owner == current_turn:
            game_field.tiles[x][y].active = True
    
def mouse_press_event_map(mouse_event):
    coordinates = list(mouse_event.pos)
    if end_turn_button.in_button(coordinates):
        end_turn()
    elif in_map_area(coordinates):
        click_tile(int((coordinates[0]-game_map_location[0]) // square_size), int((coordinates[1]-game_map_location[1]) // square_size))

def mouse_press_event_confirmation(mouse_event):
    global current_screen
    coordinates = list(mouse_event.pos)
    if confirmation_button.in_button(coordinates):
        current_screen = "Map"

def mouse_press_event_start_menu(mouse_event):
    global current_screen
    coordinates = list(mouse_event.pos)
    if start_game_button.in_button(coordinates):
        map_setup()
        map_buttons()
        current_screen = "Map"

def draw_confirmation_screen():
    #Resets display to grey
    game_display.fill(grey)

    #Draws the confirmation button
    confirmation_button.draw_button()

    #Actually updates
    pygame.display.update()

def draw_start_menu_screen():
    #Resets display to blue
    game_display.fill(blue)

    #Draws the start game button
    start_game_button.draw_button()

    #Actually updates
    pygame.display.update()

def draw_game_map_screen():
    #Resets the display
    game_display.fill(white)

    #Draws the game tiles
    for y in range(0, field_size):
        for x in range(0, field_size):
            if game_field.tiles[x][y].seen_by_players[current_turn] == 1:
                field_bar_percentages = []
                for i in range(0,4):
                    if game_field.tiles[x][y].roads[i] == 1:
                        field_bar_percentages.append(field_bar_percentage)
                    else:
                        field_bar_percentages.append(field_bar_percentage*5)
                
                game_display.fill(player_colours[game_field.tiles[x][y].owner], rect=[x*square_size+game_map_location[0], y*square_size+game_map_location[1], square_size, square_size])

                #Bars around tile
                game_display.fill(black, rect=[x*square_size+game_map_location[0], y*square_size+game_map_location[1], square_size, field_bar_percentages[0]*square_size])
                game_display.fill(black, rect=[(x + 1 - field_bar_percentages[1])*square_size+game_map_location[0], y*square_size+game_map_location[1], field_bar_percentages[1]*square_size, square_size])
                game_display.fill(black, rect=[x*square_size+game_map_location[0], (y + 1 - field_bar_percentages[2])*square_size+game_map_location[1], square_size, field_bar_percentages[2]*square_size])
                game_display.fill(black, rect=[x*square_size+game_map_location[0], y*square_size+game_map_location[1], field_bar_percentages[3]*square_size, square_size])

                #Active filter
                if game_field.tiles[x][y].active:
                    filter_surface = pygame.Surface((square_size, square_size))
                    filter_surface.set_alpha(63)
                    filter_surface.fill(white)
                    game_display.blit(filter_surface, [x*square_size + game_map_location[0], y*square_size + game_map_location[1]])
                
                #Display creature count
                font = pygame.font.SysFont(None, 25)

                #Centre text
                text_centre = font.render(str(game_field.tiles[x][y].army.warrior_count) + "/" + str(game_field.tiles[x][y].army.bowman_count), True, black)
                text_centre_size = text_centre.get_size()
                vertical_size = text_centre_size[1]
                game_display.blit(text_centre, [(x + 0.5)*square_size - text_centre_size[0]/2 + game_map_location[0], (y + 0.5)*square_size - vertical_size/2 - text_centre_size[1]/2 + game_map_location[1]])

                if current_turn == game_field.tiles[x][y].owner:
                    #North text
                    if game_field.tiles[x][y].orders[0].unit_sum != 0:
                        text_north = font.render(str(game_field.tiles[x][y].orders[0].units[0]) + "/" + str(game_field.tiles[x][y].orders[0].units[1]), True, black)
                        text_north_size = text_north.get_size()
                        game_display.blit(text_north, [(x+0.5)*square_size - text_north_size[0]/2 + game_map_location[0], (y+field_bar_percentage)*square_size + space_between_elements + game_map_location[1]])

                    #East text
                    if game_field.tiles[x][y].orders[1].unit_sum != 0:
                        text_east = font.render(str(game_field.tiles[x][y].orders[1].units[0]) + "/" + str(game_field.tiles[x][y].orders[1].units[1]), True, black)
                        text_east_size = text_east.get_size()
                        game_display.blit(text_east, [(x + 1 - field_bar_percentage)*square_size - text_east_size[0] - space_between_elements + game_map_location[0], (y+0.5)*square_size + vertical_size/2 - text_east_size[1]/2 + game_map_location[1]])

                    #South text
                    if game_field.tiles[x][y].orders[2].unit_sum != 0:
                        text_south = font.render(str(game_field.tiles[x][y].orders[2].units[0]) + "/" + str(game_field.tiles[x][y].orders[2].units[1]), True, black)
                        text_south_size = text_south.get_size()
                        game_display.blit(text_south, [(x+0.5)*square_size - text_south_size[0]/2 + game_map_location[0], (y+1 - field_bar_percentage)*square_size - space_between_elements - text_south_size[1] + game_map_location[1]])

                    #West text
                    if game_field.tiles[x][y].orders[3].unit_sum != 0:
                        text_west = font.render(str(game_field.tiles[x][y].orders[3].units[0]) + "/" + str(game_field.tiles[x][y].orders[3].units[1]), True, black)
                        text_west_size = text_west.get_size()
                        game_display.blit(text_west, [(x + field_bar_percentage)*square_size + space_between_elements + game_map_location[0], (y+0.5)*square_size + vertical_size/2 - text_west_size[1]/2 + game_map_location[1]])
                
            #If not seen by player
            else:
                game_display.fill(dark_grey, rect=[x*square_size+game_map_location[0], y*square_size+game_map_location[1], square_size, square_size])

    #End turn button
    end_turn_button.draw_button()
    
    #Actually updates
    pygame.display.update()


def event_handle_map():
    global game_exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_press_event_map(event)
        elif event.type == pygame.KEYDOWN:
            if len(game_field.current_order_input_tiles) > 0:
                game_field.press_key(event)
    return

def event_handle_start_menu():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global game_exit
            game_exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_press_event_start_menu(event)
    return

def event_handle_confirmation():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_press_event_confirmation(event)
    return

def loop_map():
    draw_game_map_screen()
    event_handle_map()

def loop_confirmation():
    draw_confirmation_screen()
    event_handle_confirmation()

def loop_start_menu():
    draw_start_menu_screen()
    event_handle_start_menu()

def one_loop():
    if current_screen == "Map":
        loop_map()
    elif current_screen == "Confirmation":
        loop_confirmation()
    elif current_screen == "Start menu":
        loop_start_menu()
    clock.tick(30)

def game_loop():
    while not game_exit:
        one_loop()

def confirmation_buttons():
    global confirmation_button
    confirmation_button = Button("Ready", black, player_colours[current_turn], confirmation_button_location[0], confirmation_button_location[1], confirmation_button_size[0], confirmation_button_size[1])

def start_menu_buttons():
    global start_game_button
    start_game_button = Button("Start game", black, red, start_game_button_location[0], start_game_button_location[1], start_game_button_size[0], start_game_button_size[1])

def map_buttons():
    global end_turn_button
    end_turn_button = Button("End turn", black, green, end_turn_button_location[0], end_turn_button_location[1], end_turn_button_size[0], end_turn_button_size[1])

game_display = game_setup()
game_loop()

pygame.quit()
quit()

#battle_simulator(10000000, [1,1], [1,1])


