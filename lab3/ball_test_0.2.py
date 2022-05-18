# Imports
import pygame
import math
import random
from Ball_2 import Ball


# Initialize game engine
pygame.init()

# Window
SIZE = (800, 600)
TITLE = "Major League Soccer"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

ball_arr=[]
for i in range(1):
    ball = Ball(list(SIZE), 50, 40)
    ball.x_speed = random.randrange(20, 50) / 10
    ball.y_speed = random.randrange(20, 50) / 10
    ball.setPosition(200, 200)
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

    pygame.draw.rect(screen, (200, 200, 250), [SIZE[0]-100, SIZE[1]-100, 100, 100])
    pygame.draw.line(screen, (0, 0, 0), [SIZE[0]-100, SIZE[1]-100],[SIZE[0], SIZE[1]])
    pygame.draw.line(screen, (0, 0, 0), [SIZE[0]-100, SIZE[1]-100],[SIZE[0]-100, SIZE[1]-50])
    pygame.draw.line(screen, (0, 0, 0), [SIZE[0]-100, SIZE[1]-100],[SIZE[0]-50, SIZE[1]-100])


    for ball in ball_arr:
        pos = ball.getDrawPosition()
        if pos[0] > SIZE[0]-100 and pos[1] > SIZE[1]-100:
            ball.x_acceleration = -20
            ball.y_acceleration = -25
        else:
            ball.x_acceleration = 0
            ball.y_acceleration = 3
        
        
        ball.elastic_move()
        
        ball.colorUpdare()
        pygame.draw.ellipse(screen, ball.color, [pos[0], pos[1], ball.x_size, ball.y_size])

    

    pygame.display.flip()

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()