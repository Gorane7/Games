import pygame
import random
import math

random.seed(9)

clock = pygame.time.Clock()
pygame.font.init()

#CONSTANTS
screen_pixels = 500
screen_size = (500,500)
game_name = "Galaxy"
stars_in_galaxy = 100
gravity_constant = 1e-8
initial_speed = 1e-4
game_speed = 300
black_hole_mass = 10
has_black_hole = False
star_creation_mode = "sector based"

#COLORS
green = (0,255,0)
blue = (0,0,255)
red = (255,0,0)
grey = (127,127,127)
black = (0,0,0)
white = (255,255,255)
yellow = (255,255,0)

#VARIABLES
game_display = None
game_exit = False
galaxy = None

class Galaxy():
    def __init__(self, star_amount):
        self.stars = []
        for i in range(0,star_amount):
            self.stars.append(Star())
            if star_creation_mode == "sector based":
                self.stars[i].sector_start()
            elif star_creation_mode == "random":
                self.stars[i].random_start()
            elif star_creation_mode == "standing":
                self.stars[i].standing_start()

        #To make the average speed equal 0
        galaxy_vel = self.get_vel()
        self.adjust_vel(galaxy_vel)

    def get_vel(self):
        vel = [0.0, 0.0]
        for i in range(0,len(self.stars)):
            vel[0] += self.stars[i].x_vel
            vel[1] += self.stars[i].y_vel
        vel[0] = vel[0] / len(self.stars)
        vel[1] = vel[1] / len(self.stars)
        return vel

    def get_single_potential(self, star):
        energy = 0
        for i in range(0,len(self.stars)):
                distance = math.sqrt((self.stars[i].x_pos - self.stars[star].x_pos)**2 + (self.stars[i].y_pos - self.stars[star].y_pos)**2)
                if distance != 0:
                    energy -= gravity_constant / distance
        return energy

    def get_star_energies(self):
        energies = []
        for i in range(0,len(self.stars)):
            energy = 0
            
            velocity = math.sqrt(self.stars[i].x_vel**2 + self.stars[i].y_vel**2)
            energy += velocity**2 / 2

            for j in range(0,len(self.stars)):
                distance = math.sqrt((self.stars[i].x_pos - self.stars[j].x_pos)**2 + (self.stars[i].y_pos - self.stars[j].y_pos)**2)
                if distance != 0:
                    energy -= gravity_constant / distance
            energies.append(energy)
        return energies
            

    def get_kinetic_energy(self):
        energy = 0
        for i in range(0,len(self.stars)):
            velocity = math.sqrt(self.stars[i].x_vel**2 + self.stars[i].y_vel**2)
            energy += velocity**2 / 2
        return energy

    def get_potential_energy(self):
        energy = 0
        for i in range(0,len(self.stars)):
            for j in range(0,len(self.stars)):
                distance = math.sqrt((self.stars[i].x_pos - self.stars[j].x_pos)**2 + (self.stars[i].y_pos - self.stars[j].y_pos)**2)
                if distance != 0:
                    energy -= gravity_constant / distance
        return energy

    def print_total_energy(self):
        kinetic = self.get_kinetic_energy()
        potential = self.get_potential_energy()
        total = kinetic + potential
        print(total)
    
    def print_potential_energy(self):
        energy = self.get_potential_energy()
        print(energy)

    def print_kinetic_energy(self):
        energy = self.get_kinetic_energy()
        print(energy)

    def print_vel(self):
        galaxy_vel = self.get_vel()
        print(galaxy_vel)
    
    def adjust_vel(self, vel):
        for i in range(0,len(self.stars)):
            self.stars[i].x_vel -= vel[0]
            self.stars[i].y_vel -= vel[1]

    def move_stars(self):
        for i in range(0,len(self.stars)):
            self.stars[i].move_update()

    def process_gravity(self):
        for i in range(0,len(self.stars)):
            self.get_force_vector(i)
        self.update_velocities()

    def update_velocities(self):
        for i in range(0,len(self.stars)):
            self.stars[i].velocity_update()

    def calculate_single_vector(self, pos1, pos2, vel1, vel2, mass1, mass2, times_to_calculate):
        x_f = 0.0
        y_f = 0.0
        for i in range(0,times_to_calculate):
            distance_vector = self.get_dist_vector(pos1, pos2)
            distance_square = distance_vector[0]**2 + distance_vector[1]**2
            if distance_square != 0.0:
                force = gravity_constant * mass1 * mass2 / (distance_square * times_to_calculate)
                ratio = math.sqrt(distance_square) / force
                if ratio > 10:
                    return distance_vector[0] / ratio, distance_vector[1] / ratio
                else:
                    return distance_vector[0] / 10.0, distance_vector[1] / 10.0
            else:
                return x_f, y_f
        

    def get_force_vector(self, star):
        force_vector = [0.0, 0.0]
        first_star_pos = [self.stars[star].x_pos, self.stars[star].y_pos]
        first_star_vel = [self.stars[star].x_vel, self.stars[star].y_vel]
        first_star_mass = self.stars[star].mass
        for i in range(0,len(self.stars)):

            
            second_star_pos = [self.stars[i].x_pos, self.stars[i].y_pos]
            second_star_vel = [self.stars[i].x_vel, self.stars[i].y_vel]
            second_star_mass = self.stars[i].mass

            x, y = self.calculate_single_vector(first_star_pos, second_star_pos, first_star_vel, second_star_vel, first_star_mass, second_star_mass, 1)
            
            force_vector = [force_vector[0] + x, force_vector[1] + y]

        #imaginary black hole at center
        if has_black_hole:
            distance_vector_center = [0.5 - self.stars[star].x_pos, 0.5 - self.stars[star].y_pos]
            distance_square_center = distance_vector_center[0]**2 + distance_vector_center[1]**2

            black_hole_pos = [0.5, 0.5]
            black_hole_vel = [0.0, 0.0]
            this_black_hole_mass = first_star_mass * black_hole_mass
            x, y = self.calculate_single_vector(first_star_pos, black_hole_pos, first_star_vel, black_hole_vel, first_star_mass, this_black_hole_mass, 1)

            force_vector = [force_vector[0] + x, force_vector[1] + y]
        
        self.stars[star].force_vector = force_vector

    def get_dist_vector(self, first_star_pos, second_star_pos):
        x = second_star_pos[0] - first_star_pos[0]
        y = second_star_pos[1] - first_star_pos[1]

        return [x, y]

class Star():
    def __init__(self):
        self.x_pos = 0.0
        self.y_pos = 0.0
        
        self.x_vel = 0.0
        self.y_vel = 0.0

        self.force_vector = [0.0, 0.0]

        self.mass = 1.0

    def random_start(self):
        self.x_pos = random.random()
        self.y_pos = random.random()

        self.x_vel = random.random() * initial_speed
        self.y_vel = random.random() * initial_speed

    def standing_start(self):
        self.x_pos = random.random()
        self.y_pos = random.random()
        
    def sector_start(self):
        self.x_pos = random.random()
        self.y_pos = random.random()

        self.x_vel = random.random() * initial_speed
        self.y_vel = random.random() * initial_speed

        if self.x_pos < 0.5 and self.y_pos < 0.5:
            self.x_vel = self.x_vel * 2
            self.y_vel = self.y_vel - 0.5 * initial_speed
        elif self.x_pos > 0.5 and self.y_pos < 0.5:
            self.x_vel = self.x_vel - 0.5 * initial_speed
            self.y_vel = self.y_vel * 2
        elif self.x_pos > 0.5 and self.y_pos > 0.5:
            self.x_vel = 0 - self.x_vel * 2
            self.y_vel = self.y_vel - 0.5 * initial_speed
        elif self.x_pos < 0.5 and self.y_pos > 0.5:
            self.x_vel = self.x_vel - 0.5 * initial_speed
            self.y_vel = 0 - self.y_vel * 2
            
    def move_update(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        if self.x_pos > 1.0:
            self.x_pos -= 1.0
            self.x_vel = self.x_vel / 2
            self.y_vel = self.y_vel / 2
        if self.y_pos > 1.0:
            self.y_pos -= 1.0
            self.x_vel = self.x_vel / 2
            self.y_vel = self.y_vel / 2
        if self.x_pos < 0.0:
            self.x_pos += 1.0
            self.x_vel = self.x_vel / 2
            self.y_vel = self.y_vel / 2
        if self.y_pos < 0.0:
            self.y_pos += 1.0
            self.x_vel = self.x_vel / 2
            self.y_vel = self.y_vel / 2

    def velocity_update(self):
        self.x_vel += self.force_vector[0] / self.mass
        self.y_vel += self.force_vector[1] / self.mass
        self.force_vector = [0.0, 0.0]

def setup():
    global galaxy
    pygame.init()
    galaxy = Galaxy(stars_in_galaxy)
    display = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(game_name)
    return display

def physics_update():
    galaxy.process_gravity()
    galaxy.move_stars()

def draw_game():
    #Resets the display
    game_display.fill(black)

    #Draws the black hole
    if has_black_hole:
        pygame.draw.circle(game_display, red, [int(screen_pixels/2), int(screen_pixels/2)], 2)
    
    #Draws the stars
    for i in range(0,len(galaxy.stars)):
        pygame.draw.circle(game_display, white, [int(galaxy.stars[i].x_pos * screen_pixels), int(galaxy.stars[i].y_pos * screen_pixels)], 0)

    #Actually updates
    pygame.display.update()

def event_handle():
    global game_exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

def one_loop():
    event_handle()
    draw_game()
    physics_update()
    clock.tick(game_speed)

def game_loop():
    while not game_exit:
        one_loop()

game_display=setup()
game_loop()

pygame.quit()
quit()
