# Imports
import pygame
import math
import random
import Ball


# Initialize game engine
pygame.init()

# Window
SIZE = (800, 600)
TITLE = "Major League Soccer"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

ball_arr = []
for i in range(10):
    ball = Ball.Ball(screen,list(SIZE), random.randrange(10, 100), random.randrange(40))
    ball.setPosition(random.randrange(SIZE[0]), random.randrange(SIZE[1]))
    ball.setColor(random.randrange(255), random.randrange(255), random.randrange(255))
    ball_arr.append(ball)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Game loop
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    ''' for now, we'll just check to see if the X is clicked '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    screen.fill((255, 255, 255))


    for ball in ball_arr:
        ball.move()

    pygame.display.flip()

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()