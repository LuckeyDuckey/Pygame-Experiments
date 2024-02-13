from scipy.interpolate import CubicSpline
import numpy as np

import pygame
from pygame.locals import *

import random, time, sys

pygame.init()
pygame.display.set_caption("Water Render")

Resolution = (900, 600) # Window size / resolution
Display = pygame.display.set_mode(Resolution, pygame.DOUBLEBUF)

Clock, FPS = pygame.time.Clock(), 140
LastTime = time.time() # For delta time
TimeRate = 60 # How fast time passes here it is 60x

class Spring:
    def __init__(self, pos, spring_constant, resistance):
        self.pos = pos
        self.spring_constant = spring_constant
        self.resistance = resistance
        self.extension = 0
        self.velocity = 0

    def update(self, display, delta_time):
        loss = -self.resistance * self.velocity
        force = -self.spring_constant * self.extension + loss
        self.velocity += force * delta_time
        self.extension += self.velocity * delta_time

class Water:
    def __init__(self, size, num_springs, spring_constant, resistance):
        self.water_surface = pygame.Surface(size)
        self.size = size
        self.springs = []

        for i in range(size[1]):
            interpolation = (1 - (i + 1) / self.size[1])
            pygame.draw.line(self.water_surface, (0, 150 * interpolation, 255 * interpolation), (0, i), (self.size[0], i), width=1)

        for i in range(num_springs):
            self.springs.append(Spring([self.size[0] / (num_springs - 1) * i, size[1] / 2], spring_constant, resistance))

    def generate_smooth_line(self, coordinates):
        x_values, y_values = zip(*coordinates)

        x_values = np.array(x_values)
        y_values = np.array(y_values)

        new_x_values = np.arange(x_values[0], x_values[-1] + 1, 1)

        cs = CubicSpline(x_values, y_values)
        new_y_values = cs(new_x_values)

        new_coordinates = list(zip(new_x_values, new_y_values))

        return new_coordinates

    def update(self, display, delta_time):
        points = []

        for i in range(len(self.springs)):

            if i > 0:
                self.springs[i-1].velocity += 0.015 * (self.springs[i].extension - self.springs[i-1].extension) * delta_time

            if i < len(self.springs) - 1:
                self.springs[i+1].velocity += 0.015 * (self.springs[i].extension - self.springs[i+1].extension) * delta_time
            
            self.springs[i].update(display, delta_time)

            points.append([self.springs[i].pos[0], self.springs[i].pos[1] - self.springs[i].extension])

        points = self.generate_smooth_line(points)

        render_surface = self.water_surface.copy()

        pygame.draw.polygon(render_surface, (255, 0, 0), [[0, 0]] + points + [[self.size[0], 0]])
        pygame.draw.lines(render_surface, (255, 255, 255), False, points, width=1)

        render_surface.set_colorkey((255, 0, 0))
        render_surface.set_alpha(250)
        
        return render_surface

water = Water(Resolution, 61, 0.015, 0.03)

while True:
    
    # Set fps
    Clock.tick(FPS)

    # Update delta time
    DeltaTime = (time.time() - LastTime) * TimeRate
    LastTime = time.time()
    
    Display.fill((0,0,0))

    mx, my = pygame.mouse.get_pos()

    pygame.draw.rect(Display, (255,255,255), pygame.Rect(0, 200, 250, 400))
    pygame.draw.rect(Display, (255,255,255), pygame.Rect(750, 150, 150, 450))
    pygame.draw.rect(Display, (255,255,255), pygame.Rect(400, 350, 100, 250))

    water.update(Display, DeltaTime)

    water.springs[random.randint(0, 60)].velocity += random.uniform(-0.5, 0.5)
    water_surface = water.update(Display, DeltaTime)

    Display.blit(water_surface, (0,0))

    pygame.display.set_caption(f"FPS: {int(Clock.get_fps())}")
    pygame.display.update()
    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                water.springs[min(max(0, int(mx / (900 / 60))), 60)].extension = 300 - my
