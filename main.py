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

#perhaps make wall a parent function that only contains self.x, self.y, and maybe a list of lines make subclasses for the individual wall types
class Wall: #need a corner piece (for each direction), intersection piece (2 and 3 diff directions), vertical piece,
    def __init__(self, x, y, type): #need something that differentiates if it is a horizontal or vertical line
        self.x = x
        self.y = y
        self.type = type #type will be an int
        # self.line1 = pygame.draw.line(SCREEN, "grey", [self.x, self.y], [self.x+400, self.y], 5)
        # self.line2 = pygame.draw.line(SCREEN, "grey", [self.x, self.y+150], [self.x+400, self.y+150], 5)


class HWall(Wall):
    def __init__(self, x, y):
        super().__init__(x, y, 1)
        self.line1_start_pos = (x,y)
        self.line1_end_pos = (x+400, y)
        self.line2_start_pos = (x,y+150)
        self.line2_end_pos = (x+400, y+150)
        self.line_width = 5 #this can be modified/change how it work/may not need to store
        self.line_color = "grey" #may not need to store this
        self.line1 = pygame.draw.line(SCREEN, "grey", [self.line1_start_pos[0], self.line1_start_pos[1]], [self.line1_end_pos[0], self.line1_end_pos[1]], 5)
        self.line2 = pygame.draw.line(SCREEN, "grey", [self.line2_start_pos[0], self.line2_start_pos[1]], [self.line2_end_pos[0], self.line2_end_pos[1]], 5)
       
class VWall(Wall):
    def __init__(self, x, y):
        super().__init__(x, y, 2)
        self.line1_start_pos = (x,y)
        self.line1_end_pos = (x, y+400)
        self.line2_start_pos = (x+150,y)
        self.line2_end_pos = (x+150, y+400)
        self.line_width = 5 #this can be modified/change how it work/may not need to store
        self.line_color = "grey" #may not need to store this
        self.line1 = pygame.draw.line(SCREEN, "grey", [self.line1_start_pos[0], self.line1_start_pos[1]], [self.line1_end_pos[0], self.line1_end_pos[1]], 5)
        self.line2 = pygame.draw.line(SCREEN, "grey", [self.line2_start_pos[0], self.line2_start_pos[1]], [self.line2_end_pos[0], self.line2_end_pos[1]], 5)


class Player:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def DrawPlayer(self):
        pygame.draw.rect(SCREEN, "blue", pygame.Rect(self.x, self.y, 40, 40))

    def PlayerCollideWalls(self, walls: List[Wall]):
        returners = []
        for wall in walls:
            if(wall.type == 1 or wall.type == 2):
                if wall.line1.colliderect(self.x, self.y - 300*dt, 40, 40) or wall.line2.colliderect(self.x, self.y - 300*dt, 40, 40):
                    returners.append(1) #return number based off what type of wall collided with
                elif (wall.line1.colliderect(self.x, self.y + 300*dt, 40, 40) or wall.line2.colliderect(self.x, self.y + 300*dt, 40, 40)):
                    returners.append(2)
                elif (wall.line1.colliderect(self.x - 300*dt, self.y, 40, 40) or wall.line2.colliderect(self.x - 300*dt, self.y, 40, 40)):
                    returners.append(3)
                elif (wall.line1.colliderect(self.x + 300*dt, self.y, 40, 40) or wall.line2.colliderect(self.x + 300*dt, self.y, 40, 40)):
                    returners.append(4)
        return returners


    def MovePlayer(self, walls:List[Wall]):
        moveList = self.PlayerCollideWalls(walls)
        moveLeft = True
        moveRight = True
        moveUp = True
        moveDown = True
        for condition in moveList:
            if(condition == 1):
                moveUp = False
            if(condition == 2):
                moveDown = False
            if(condition == 3):
                moveLeft = False
            if(condition == 4):
                moveRight = False
        
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] and self.y > 0 and moveUp):
            self.y -= 300 * dt
        if (keys[pygame.K_s] and player_pos.y + 40 < 720 and moveDown):
            self.y += 300*dt
        if (keys[pygame.K_a] and self.x > 0 and moveLeft):
            self.x -= 300 * dt
        if (keys[pygame.K_d] and self.x + 40 < 1280 and moveRight):
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
    walls = [HWall(300, 100), VWall(700, 250)]
    character.DrawPlayer()

    #movement of player
    character.MovePlayer(walls)

    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60)/1000  # limits FPS to 60

pygame.quit()