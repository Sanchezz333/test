import pygame
import math
import random


class Ball:
    color = [0, 0, 0]
    x_position = 0
    y_position = 0
    speed = 4
    touch = False
    x_compression = False
    y_compression = False
    x_compression_rate = 0
    y_compression_rate = 0
    angle_a = 1
    angle_b = 1

    

    def __init__(self, screen, screen_size=[0,0], diametr=10, elastic=0, ):
        self.screen_size = screen_size
        self.diametr = diametr
        self.elastic = diametr * (elastic/100)
        if self.elastic > diametr * 0.9:
            self.elastic = diametr * 0.9
        self.screen = screen
        self.angle = random.randrange(0, 157) / 100
        self.base_angle = self.angle

    
    def set_position(self, x,y):
        self.x_position = x
        self.y_position = y


    def move(self):
        self.x_position += self.speed * math.cos(self.angle)
        self.y_position += self.speed * math.sin(self.angle)
        self.in_frame()
        
        if self.touch: #Рисуем сжатие
            if self.elastic != 0:
                if self.x_compression or self.y_compression:
                    if self.x_compression:
                        self.x_compression_rate += self.speed * math.cos(self.angle) *2
                    if self.y_compression:
                        self.y_compression_rate += self.speed * math.sin(self.angle) *2

                    if self.x_compression_rate >= self.elastic or self.x_compression_rate >= self.elastic:
                        self.x_compression = False
                        self.y_compression = False
                        self.angle = self.angle_b * (self.angle_a * self.base_angle + (self.angle_b - 1)/2 * 3.14)
                        self.base_angle += random.randrange(-10, 10)/ 100 
                else:    
                    if self.x_compression_rate > 0:
                        self.x_compression_rate -= self.speed * math.cos(self.angle) *2
                        if self.x_compression_rate < 0:
                            self.x_compression_rate = 0
                            self.touch = False
                    if self.y_compression_rate > 0:
                        self.y_compression_rate -= self.speed * math.sin(self.angle) *2
                        if self.y_compression_rate < 0:
                            self.y_compression_rate = 0
                            self.touch = False
            else:
                self.angle = self.angle_b * (self.angle_a * self.base_angle + (self.angle_b - 1)/2 * 3.14)
                self.base_angle += random.randrange(-10, 10)/ 100 
            pygame.draw.ellipse(
                    self.screen, 
                    self.get_color(), 
                    [self.x_position, self.y_position, self.diametr-self.x_compression_rate, self.diametr-self.y_compression_rate]
                    )    

        else:            
            self.it_touch()
            pygame.draw.ellipse(self.screen, self.get_color(), [self.x_position, self.y_position, self.diametr, self.diametr])    


    def get_color(self):
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


    def it_touch(self):
        if self.x_position == 0:
            self.touch = True
            self.x_compression = True
            self.angle_b *= -1

        elif self.y_position == 0:
            self.touch = True
            self.y_compression = True
            self.angle_a *= -1


        elif self.x_position == self.screen_size[0]-self.diametr:
            self.touch = True
            self.x_compression = True
            self.angle_b *= -1

        elif self.y_position == self.screen_size[1]-self.diametr:
            self.touch = True
            self.y_compression = True
            self.angle_a *= -1

        
    def in_frame(self):
        if self.x_position < 0:
            self.x_position = 0

        elif self.y_position < 0:
            self.y_position = 0

        elif self.x_position + self.diametr > self.screen_size[0]:
            self.x_position = self.screen_size[0]-self.diametr 

        elif self.y_position + self.diametr > self.screen_size[1]:
            self.y_position = self.screen_size[1]-self.diametr
