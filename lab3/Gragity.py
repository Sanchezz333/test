# Imports

import pygame
import math
import random
from Ball_2 import Ball

def drawGravitymeter(x, y, x_a, y_a):
    radius = 50
    color = [0, 0, 0]
    betta = 157/1000
    a = math.sqrt(x_a**2 + y_a**2)
    alpha = math.acos(x_a/a)
    if math.asin(y_a/a) < 0:
        alpha *= -1
    rx = radius / a * x_a
    ry = radius / a * y_a
    pygame.draw.circle(screen, color, [x, y], radius, 2)
    pygame.draw.line(screen, color, [x-rx, y-ry],[x+rx, y+ry])

    pygame.draw.line(screen, color, [x+rx-0.5*radius*math.cos(alpha+betta), y+ry-0.5*radius*math.sin(alpha+betta)],[x+rx, y+ry])
    pygame.draw.line(screen, color, [x+rx-0.5*radius*math.cos(alpha-betta), y+ry-0.5*radius*math.sin(alpha-betta)],[x+rx, y+ry])



# Initialize game engine
pygame.init()

# Window
SIZE = (800, 600)
TITLE = "Major League Soccer"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)


ball = Ball(list(SIZE), 50, 40)
ball.x_speed = random.randrange(20, 50) / 10
ball.y_speed = random.randrange(20, 50) / 10
ball.y_acceleration = 3
ball.x_acceleration = 1


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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            ball.x_acceleration, ball.y_acceleration = ball.y_acceleration, -ball.x_acceleration
    
    screen.fill((200, 200, 200))

    drawGravitymeter(400, 300, ball.x_acceleration, ball.y_acceleration)

    pos = ball.getDrawPosition()
    ball.real_move()
    ball.colorUpdare()
    pygame.draw.ellipse(screen, ball.color, [pos[0], pos[1], ball.x_size, ball.y_size])

    

    pygame.display.flip()

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()