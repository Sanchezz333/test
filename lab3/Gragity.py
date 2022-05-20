# Imports

import pygame
import math
import random
from Ball_2 import Ball


def drawGravitymeter(x, y, x_a, y_a):
    '''Рисует Гравиметр в координатах x и y указывающий направление гравитации.
    Для вычистения использует ускорение по осям x_a и y_a'''
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

    pygame.draw.line(screen, color, [x-rx, y-ry], [x+rx, y+ry])
    pygame.draw.line(screen, color, [
                     x+rx-0.5*radius*math.cos(alpha+betta), y+ry-0.5*radius*math.sin(alpha+betta)], [x+rx, y+ry])
    pygame.draw.line(screen, color, [
                     x+rx-0.5*radius*math.cos(alpha-betta), y+ry-0.5*radius*math.sin(alpha-betta)], [x+rx, y+ry])


def changeBallAcceleration(ball, pos, size, max_acceleration):
    ball.x_acceleration = max_acceleration * (pos[0]-ball.x_position) / size[0]
    ball.y_acceleration = max_acceleration * (pos[1]-ball.y_position) / size[1]

def planetGravity(ball, pos, g):
    r = math.sqrt((pos[0]-ball.x_position)**2 + (pos[1]-ball.y_position)**2)
    ball.x_acceleration = g * (pos[0]-ball.x_position) / r
    ball.y_acceleration = g * (pos[1]-ball.y_position) / r



# Initialize game engine
pygame.init()

# Window
SIZE = (800, 600)
TITLE = "Major League Soccer"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

cur_pos = [0, 0]

ball_arr = []
for i in range(10):
    ball = Ball(list(SIZE), 50, 40)
    ball.x_speed = random.randrange(20, 50) / 10
    ball.y_speed = random.randrange(20, 50) / 10
    ball.y_acceleration = random.randrange(20, 50) / 10
    ball.x_acceleration = random.randrange(20, 50) / 10
    ball.x_position = random.randrange(100, 500)
    ball.y_position = random.randrange(100, 500)
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
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     changeBallAcceleration(ball, event.pos, SIZE, 20)
        elif event.type == pygame.MOUSEMOTION:
            cur_pos = event.pos

    screen.fill((200, 200, 200))

    # drawGravitymeter(400, 300, ball.x_acceleration, ball.y_acceleration)
    for ball in ball_arr:
        planetGravity(ball, cur_pos, 1)
        ball.x_speed *= 0.999
        ball.y_speed *= 0.999
        pos = ball.getDrawPosition()
        ball.real_move()
        ball.colorUpdare()
        pygame.draw.ellipse(screen, ball.color, [
                            pos[0], pos[1], ball.x_size, ball.y_size])

    pygame.display.flip()

    # Limit refresh rate of game loop
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
