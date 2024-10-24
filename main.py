import pygame
import time
import random
from typing import List

# Example file showing a basic pygame "game loop"
WIDTH: int = 1280;
HEIGHT: int = 720;

# pygame setup
pygame.init();
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT));
clock = pygame.time.Clock();
running: bool = True;
dt = 0;

player_pos_x = SCREEN.get_width()/2 - 25 #minus 25 to get in middle
player_pos_y = SCREEN.get_height()/2 + 100 #minus 25 to get in middle
player_pos = pygame.Vector2(player_pos_x, player_pos_y);
screenColor = (0, 100, 0)


class Wall:
    def __init__(self, x, y): #need something that differentiates if it is a horizontal or vertical line
        self.x = x
        self.y = y
        self.line1 = pygame.draw.line(SCREEN, "grey", [self.x, self.y], [self.x+400, self.y], 5)
        self.line2 = pygame.draw.line(SCREEN, "grey", [self.x, self.y+150], [self.x+400, self.y+150], 5)

class Player:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def DrawPlayer(self):
        pygame.draw.rect(SCREEN, "blue", pygame.Rect(self.x, self.y, 40, 40))

    def PlayerCollideWalls(self, walls: List[Wall]):
        for wall in walls:
            if wall.line1.colliderect(self.x, self.y - 300*dt, 40, 40) or wall.line2.colliderect(self.x, self.y - 300*dt, 40, 40):
                return 1 #return number based off what type of wall collided with
            elif (wall.line1.colliderect(self.x, self.y + 300*dt, 40, 40) or wall.line2.colliderect(self.x, self.y + 300*dt, 40, 40)):
                return 2
            elif (wall.line1.colliderect(self.x - 300*dt, self.y, 40, 40) or wall.line2.colliderect(self.x - 300*dt, self.y, 40, 40)):
                return 3
            elif (wall.line1.colliderect(self.x + 300*dt, self.y, 40, 40) or wall.line2.colliderect(self.x + 300*dt, self.y, 40, 40)):
                return 4
            else:
                return 0


    def MovePlayer(self, walls:List[Wall]):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] and self.y > 0 and 1 != self.PlayerCollideWalls(walls)):
            self.y -= 300 * dt
        if (keys[pygame.K_s] and player_pos.y + 40 < 720 and 2 != self.PlayerCollideWalls(walls)):
            self.y += 300*dt
        if (keys[pygame.K_a] and self.x > 0 and 3 != self.PlayerCollideWalls(walls)):
            self.x -= 300 * dt
        if (keys[pygame.K_d] and self.x + 40 < 1280 and 4 != self.PlayerCollideWalls(walls)):
            self.x += 300 * dt


character = Player(player_pos.x,player_pos.y)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    SCREEN.fill(screenColor)

    # RENDER YOUR GAME HERE
    walls = [Wall(300, 200)]
    character.DrawPlayer()

    #movement of player
    character.MovePlayer(walls)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60)/1000  # limits FPS to 60

pygame.quit()