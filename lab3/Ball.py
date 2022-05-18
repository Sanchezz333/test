import pygame
import math
import random


class Ball:
    x_position = 0
    y_position = 0
    speed = 4
    touch = False
    x_compression = False
    y_compression = False
    x_compression_rate = 0
    y_compression_rate = 0
    move_side_y = 1
    move_side_x = 1
    touch_side = [[False, False], [False, False]]

    def __init__(self, screen, screen_size=[0, 0], diametr=10, elastic=0, ):
        self.screen_size = screen_size
        self.diametr = diametr
        self.elastic = diametr * (elastic/100)
        if self.elastic > diametr * 0.9:
            self.elastic = diametr * 0.9
        self.screen = screen
        self.angle = random.randrange(0, 157) / 100
        self.base_angle = self.angle
        self.color = [0, 0, 0]

    def setPosition(self, x, y):
        self.x_position = x
        self.y_position = y

    def setColor(self, r, g, b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b

    def move(self):
        self.x_position += self.speed * math.cos(self.angle)
        self.y_position += self.speed * math.sin(self.angle)

        if self.itTouch():
            if self.elastic != 0:  # Для эластичного
                if not self.touch:  # Определение оси сжатия
                    self.touchSide()
                    self.touch = True
                    self.x_compression = self.touch_side[0][0] or self.touch_side[0][1]
                    self.y_compression = self.touch_side[1][0] or self.touch_side[1][1]

                if self.x_compression or self.y_compression:  # Сжатие
                    if self.x_compression:
                        self.x_compression_rate += abs(
                            self.speed * math.cos(self.angle))
                    if self.y_compression:
                        self.y_compression_rate += abs(
                            self.speed * math.sin(self.angle))
                    if self.x_compression_rate >= self.elastic or self.y_compression_rate >= self.elastic:  # Сжатие закончено
                        self.x_compression = False
                        self.y_compression = False
                        self.getAngle()
                        self.touchSideReset()

                else:  # Расширение
                    if self.x_compression_rate > 0:
                        self.x_compression_rate -= abs(
                            self.speed * math.cos(self.angle))
                    if self.y_compression_rate > 0:
                        self.y_compression_rate -= abs(
                            self.speed * math.sin(self.angle))
                    if self.x_compression_rate < 0 or self.y_compression_rate < 0:  # Расширение закончено
                        self.touch = False
                        self.x_compression_rate = 0
                        self.y_compression_rate = 0

                pygame.draw.ellipse(self.screen,self.getColor(),[
                                    self.x_position + self.x_compression_rate/3,
                                    self.y_position + self.y_compression_rate/3,
                                    self.diametr - self.x_compression_rate,
                                    self.diametr - self.y_compression_rate])

            else:
                self.touchSide()
                self.getAngle()
                self.touchSideReset()
                self.inFrame()
                pygame.draw.ellipse(self.screen, self.getColor(), [
                                    self.x_position, self.y_position, self.diametr, self.diametr])
        else:
            self.touch = False
            self.x_compression_rate = 0
            self.y_compression_rate = 0
            pygame.draw.ellipse(self.screen, self.getColor(), [
                                self.x_position, self.y_position, self.diametr, self.diametr])

    def getColor(self):
        if self.color[0] == 255:
            if self.color[2] == 0:
                self.color[1] += 1
                if self.color[1] > 255:
                    self.color[1] = 255
                    self.color[0] = 254
            else:
                self.color[2] -= 1
        elif self.color[1] == 255:
            if self.color[0] == 0:
                self.color[2] += 1
                if self.color[2] > 255:
                    self.color[2] = 255
                    self.color[1] = 254
            else:
                self.color[0] -= 1
        else:
            if self.color[1] == 0:
                self.color[0] += 1
                if self.color[0] > 255:
                    self.color[0] = 255
                    self.color[2] = 254
            else:
                self.color[1] -= 1
        return self.color

    def itTouch(self):
        if self.x_position < 0 or self.y_position < 0 or self.x_position + self.diametr > self.screen_size[0] or self.y_position + self.diametr > self.screen_size[1]:
            return True
        return False

    def touchSide(self):
        if self.x_position < 0:
            self.touch_side[0][0] = True
        elif self.y_position < 0:
            self.touch_side[1][0] = True
        elif self.x_position + self.diametr > self.screen_size[0]:
            self.touch_side[0][1] = True
        elif self.y_position + self.diametr > self.screen_size[1]:
            self.touch_side[1][1] = True

    def touchSideReset(self):
        self.touch_side = [[False, False], [False, False]]

    def getAngle(self):
        if self.touch_side[0][0]:
            self.move_side_x = 1
        if self.touch_side[1][0]:
            self.move_side_y = 1
        if self.touch_side[0][1]:
            self.move_side_x = -1
        if self.touch_side[1][1]:
            self.move_side_y = -1

        self.angle = self.move_side_x * \
            (self.move_side_y * self.base_angle + (self.move_side_x - 1)/2 * 3.14)
        self.base_angle += random.randrange(-10, 10) / 100

    def inFrame(self):
        if self.x_position < 0:
            self.x_position = 0
        elif self.y_position < 0:
            self.y_position = 0
        elif self.x_position + self.diametr > self.screen_size[0]:
            self.x_position = self.screen_size[0]-self.diametr
        elif self.y_position + self.diametr > self.screen_size[1]:
            self.y_position = self.screen_size[1]-self.diametr
