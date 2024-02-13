import pygame, math, time, sys
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Gravity Simulation")

Resolution = (1600, 900) # Window size / resolution
Display = pygame.display.set_mode(Resolution, 0, 32)

Clock, FPS = pygame.time.Clock(), 140
LastTime = time.time() # For delta time

font = pygame.font.SysFont(None, 30) # Set font and size

GravConstant = 0.000000000066743015 # Set gravitational constant
TimeRate = 10000 # How fast time should pass in this case 10000x

Objects = []

class Object:
    def __init__(self, Mass, Position, Velocity, Color, Radius):

        # Vars for calcualtions
        self.Mass = Mass
        self.Position = Position
        self.Velocity = Velocity

        # Vars for visuals
        self.Color = Color
        self.Radius = Radius
        
    def update(self, Objects, DeltaTime):
        global Resolution, GravConstant

        for Obj in Objects:

            # 2D vector for x and y difference between objects positions
            DistanceVector = [self.Position[0] - Obj.Position[0], self.Position[1] - Obj.Position[1]]

            # Get distance beetween objects
            Distance = math.sqrt(pow(DistanceVector[0], 2) + pow(DistanceVector[1], 2))

            # Avoid div 0 errors
            if Distance != 0:

                # Get force using newtons equation
                Force = (GravConstant * self.Mass * Obj.Mass) / Distance

                Acceleration = Force / self.Mass # Calculate acceleration

                # Check if objects overlap if so no acceleration
                if self.Radius + Obj.Radius < Distance:
                    
                    # Update velocitys with scaled the acceleration per axis
                    self.Velocity[0] -= Acceleration * (DistanceVector[0] / Distance) * DeltaTime
                    self.Velocity[1] -= Acceleration * (DistanceVector[1] / Distance) * DeltaTime

        # Update position after all velocity has been calculated
        self.Position[0] += self.Velocity[0] * DeltaTime
        self.Position[1] += self.Velocity[1] * DeltaTime

        # Check if object is going outside screen in x
        if self.Position[0] < self.Radius or self.Position[0] > Resolution[0] - self.Radius:
            self.Velocity[0] *= -1 # Reflect is velocity in x

        # Check if object is going outside screen in y
        if self.Position[1] < self.Radius or self.Position[1] > Resolution[1] - self.Radius:
            self.Velocity[1] *= -1 # Reflect is velocity in y

        pygame.draw.circle(Display, self.Color, self.Position, self.Radius)

# Add a sun like object
Objects.append(Object(20000000, [800, 450], [0.01, 0.01], (255,255,0), 15))

while True:
    
    # Set fps
    Clock.tick(FPS)

    # Update delta time
    DeltaTime = (time.time() - LastTime) * TimeRate
    LastTime = time.time()
    
    Display.fill((0,0,0))

    mx, my = pygame.mouse.get_pos()

    # Update objects
    for Obj in Objects:
        Obj.update(Objects, DeltaTime)

    # Text for fps and object count
    Display.blit(font.render(f"FPS: {int(Clock.get_fps())}", True, (255,255,255)), (50, 50))
    Display.blit(font.render(f"OBJ: {len(Objects)}", True, (255,255,255)), (150, 50))

    pygame.display.update()

    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == MOUSEBUTTONDOWN:
            
            if event.button == 1:
                Objects.append(Object(25, [mx, my], [0, 0], (255,0,255), 5)) # Add object at mouse

            if event.button == 3:
                Objects = [] # Clear objects
