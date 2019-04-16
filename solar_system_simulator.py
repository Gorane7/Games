import pygame
import math

clock = pygame.time.Clock()
pygame.font.init()

G = 6.67408 * ( 1 / 10**11 )

solar_system_diameter = 10.0 * 10**11
solar_mass = 1.98855 * 10**30
solar_speed = 0

earth_mass = 5.972 * 10**24
earth_distance = 149.6 * 10**9
earth_speed = 30.0 * 10**3

mercury_mass = 3.285 * 10**23
mercury_distance = 57.91 * 10**9
mercury_speed = 47.36 * 10**3

venus_mass = 4.867 * 10**24
venus_distance = 108.2 * 10**9
venus_speed = -35.02 * 10**3

mars_mass = 6.39 * 10**23
mars_distance = 227.9 * 10**9
mars_speed = -24.08 * 10**3

jupiter_mass = 1.898 * 10**27
jupiter_distance = 778.5 * 10**9
jupiter_speed = 13.1 * 10**3

saturn_mass = 5.683 * 10**27
saturn_distance = 1429.0 * 10**9
saturn_speed = -9.6 * 10**3

uranus_mass = 8.681 * 10**25
uranus_distance = 2871.0 * 10**9
uranus_speed = 6.8 * 10**3

neptune_mass = 1.024 * 10**26
neptune_distance = 4498.0 * 10**9
neptune_speed = -5.43 * 10**3

sims_per_tick = 7
sim_time = 90000

#CONSTANTS
screen_length = 500
screen_size = (screen_length,screen_length)
game_name = "Solar System"
pixel_size = solar_system_diameter / screen_length
tick = 0

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

class Body():
    def __init__(self, mass, location, vel, colour):
        self.mass = mass
        self.location = location
        self.vel = vel
        self.colour = colour

class System():
    def __init__(self):
        self.bodies = []
        self.accelerations = []

    def add_body(self, body):
        self.bodies.append(body)

    def calculate_acceleration(self, time):
        self.accelerations = []
        for force_body in self.bodies:
            x_force = 0.0
            y_force = 0.0
            for pulling_body in self.bodies:
                if force_body != pulling_body:
                    x_dist = pulling_body.location[0] - force_body.location[0]
                    y_dist = pulling_body.location[1] - force_body.location[1]
                    distance = math.sqrt ( x_dist**2 + y_dist**2 )
                    force = ( G * force_body.mass * pulling_body.mass ) / distance**2
                    x_force += ( x_dist * force ) / distance
                    y_force += ( y_dist * force ) / distance
            x_acceleration = x_force / force_body.mass
            y_acceleration = y_force / force_body.mass
            self.accelerations.append ([ x_acceleration, y_acceleration ])
    
    def calculate_movement(self, time, tick):
        for i, body in enumerate(self.bodies):
            if tick == 0:
                body.vel[0] = body.vel[0] + self.accelerations[i][0] * time
                body.vel[1] = body.vel[1] + self.accelerations[i][1] * time
            body.location[0] = body.location[0] + body.vel[0] * time + ( self.accelerations[i][0] * time**2 ) / 2
            body.location[1] = body.location[1] + body.vel[1] * time + ( self.accelerations[i][1] * time**2 ) / 2
            if tick == 1:
                body.vel[0] = body.vel[0] + self.accelerations[i][0] * time
                body.vel[1] = body.vel[1] + self.accelerations[i][1] * time

def setup():
    pygame.init()
    display = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(game_name)
    return display

def location_to_pixel(location):
    x = location[0]
    y = location[1]
    x_pixel = x / ( solar_system_diameter / screen_length )
    y_pixel = y / ( solar_system_diameter / screen_length )
    x_pixel += screen_length / 2
    y_pixel += screen_length / 2
    return [int(x_pixel), int(y_pixel)]

def draw_game():
    #Resets the display
    #game_display.fill(black)

    #draws every object
    for body in solar_system.bodies:
        pygame.draw.circle( game_display, body.colour, location_to_pixel( body.location ), 0)
    #Actually updates
    pygame.display.update()

def event_handle():
    global game_exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

def one_loop():
    event_handle()
    physics_simulation(sims_per_tick, sim_time)
    draw_game()
    clock.tick(24)

def physics_simulation(times, seconds):
    for i in range(times):
        global tick
        tick += 1
        this_tick = tick % 2
        solar_system.calculate_acceleration(seconds)
        solar_system.calculate_movement(seconds, this_tick)

def game_loop():
    while not game_exit:
        one_loop()

solar_system = System()

sun = Body(solar_mass, [0.0, 0.0], [0.0, solar_speed], white)
solar_system.add_body(sun)

earth = Body(earth_mass, [earth_distance, 0.0], [0.0, earth_speed], green)
solar_system.add_body(earth)

mercury = Body(mercury_mass, [mercury_distance, 0.0], [0.0, mercury_speed], grey)
solar_system.add_body(mercury)

venus = Body(venus_mass, [venus_distance, 0.0], [0.0, venus_speed], yellow)
solar_system.add_body(venus)

mars = Body(mars_mass, [mars_distance, 0.0], [0.0, mars_speed], red)
solar_system.add_body(mars)

jupiter = Body(jupiter_mass, [jupiter_distance, 0.0], [0.0, jupiter_speed], grey)
solar_system.add_body(jupiter)

saturn = Body(saturn_mass, [saturn_distance, 0.0], [0.0, saturn_speed], yellow)
solar_system.add_body(saturn)

uranus = Body(uranus_mass, [uranus_distance, 0.0], [0.0, uranus_speed], blue)
solar_system.add_body(uranus)

neptune = Body(neptune_mass, [neptune_distance, 0.0], [0.0, neptune_speed], blue)
solar_system.add_body(neptune)

game_display=setup()
game_display.fill(black)
game_loop()

pygame.quit()
quit()
