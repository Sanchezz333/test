
class Ball:
    x_position = 0
    y_position = 0
    x_speed = 3
    y_speed = 3
    x_compression_rate = 0
    y_compression_rate = 0
    x_acceleration = 0
    y_acceleration = 0

    def __init__(self, screen_size=[0,0], diametr=10, elastic=0):
        '''
        Создание объекта диаметром diametr и эластичностью elastic %, на экране размера screen_size.
        '''
        self.screen_size = screen_size
        self.diametr = diametr
        self.x_size = diametr
        self.y_size = diametr
        self.elastic = diametr * (elastic/100)
        if self.elastic > diametr * 0.9:
            self.elastic = diametr * 0.9
        self.color = [0, 0, 0]        
        self.inFrame()
        self.touch_side = [[False, False],[False, False]]
        self.x_touch = False
        self.y_touch = False
        self.y_compression = False
        self.x_compression = False
    
    def setPosition(self, x,y):
        '''Установить координаты центра объекта '''
        self.x_position = x
        self.y_position = y
        self.inFrame()


    def colorUpdare(self, r, g, b):
        '''Установить цвет объекта'''
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b


    def hard_move(self):
        '''Движенеи твердого объекта'''
        self.x_position += self.x_speed
        self.y_position += self.y_speed
        if self.itTouch(): 
            self.touchSide()
            self.directionUpdate()
            self.touchSideReset()
            self.inFrame()


    def elastic_move(self):
        '''Движение эластичного объекта'''
        self.x_position += self.x_speed
        self.y_position += self.y_speed

        if self.itTouch() :
            if self.elastic == 0: 
                self.hard_move()
            else:
                if not self.x_touch: # Определение оси сжатия
                    self.x_touch = self.touch_side[0][0] or self.touch_side[0][1]
                    self.x_compression = self.touch_side[0][0] or self.touch_side[0][1]

                if not self.y_touch: # Определение оси сжатия
                    self.y_touch = self.touch_side[1][0] or self.touch_side[1][1]
                    self.y_compression = self.touch_side[1][0] or self.touch_side[1][1]

        if self.x_compression:
            self.x_compression_rate += abs(self.x_speed*2)
            self.x_size -= abs(self.x_speed*2)
            if self.x_compression_rate >= self.elastic:  # Сжатие закончено x
                self.x_compression = False
                self.x_compression_rate = self.elastic
                self.x_speed *= -1                
                self.touch_side[0][0] = False
                self.touch_side[0][1] = False
        else:
            if self.x_compression_rate > 0:
                self.x_compression_rate -= abs(self.x_speed*2)
                self.x_size += abs(self.x_speed*2)
            if self.x_compression_rate < 0:  # Расширение закончено x
                self.x_touch = False
                self.x_compression_rate = 0
                self.x_size = self.diametr

        if self.y_compression:
            self.y_compression_rate += abs(self.y_speed*2)
            self.y_size -= abs(self.y_speed*2)
            if self.y_compression_rate >= self.elastic:  # Сжатие закончено y
                self.y_compression_rate = self.elastic
                self.y_compression = False
                self.y_speed *= -1                
                self.touch_side[1][0] = False
                self.touch_side[1][1] = False
        else:
            if self.y_compression_rate > 0:
                self.y_compression_rate -= abs(self.y_speed*2)
                self.y_size += abs(self.y_speed*2)
            if self.y_compression_rate < 0:  # Расширение закончено y
                self.y_touch = False
                self.y_compression_rate = 0
                self.y_size = self.diametr
        

    def real_move(self):
        ''''Движение твердого объекта с учетом ускорения'''
        self.x_position += self.x_speed
        self.y_position += self.y_speed
        if self.itTouch(): 
            if self.touch_side[0][0] or self.touch_side[0][1]:
                self.x_speed *= 0.8
            if self.touch_side[1][0] or self.touch_side[1][1]:
                self.y_speed *= 0.9           
            self.directionUpdate()
            self.touchSideReset()
            self.inFrame()
        self.x_speed += self.x_acceleration / 10
        self.y_speed += self.y_acceleration / 10


    def colorUpdare(self):
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
    

    def itTouch(self):
        self.touchSide()
        return self.touch_side[0][0] or self.touch_side[0][1] or self.touch_side[1][0] or self.touch_side[1][1]


    def touchSide(self):
        if self.x_position - self.x_size/2 < 0:
            self.touch_side[0][0] = True
        if self.y_position- self.y_size/2 < 0:
            self.touch_side[1][0] = True
        if self.x_position + self.x_size/2 > self.screen_size[0]:
            self.touch_side[0][1] = True
        if self.y_position + self.y_size/2 > self.screen_size[1]:
            self.touch_side[1][1] = True


    def touchSideReset(self):
        self.touch_side = [[False, False],[False, False]]


    def directionUpdate(self):
        if self.touch_side[0][0] or self.touch_side[0][1]:
            self.x_speed *= -1
        if self.touch_side[1][0] or self.touch_side[1][1]:
            self.y_speed *= -1

        
    def inFrame(self):
        if self.x_position - self.x_size/2 < 0:
            self.x_position = self.x_size/2
        if self.y_position - self.y_size/2 < 0:
            self.y_position = self.x_size/2
        if self.x_position + self.x_size/2 > self.screen_size[0]:
            self.x_position = self.screen_size[0] - self.x_size/2
        if self.y_position + self.y_size/2 > self.screen_size[1]:
            self.y_position = self.screen_size[1] - self.x_size/2

    def getDrawPosition(self):
        '''дает координаты верхнего левого угла объекта для рисования в pygame'''
        return self.x_position - self.x_size/2, self.y_position - self.y_size/2, 