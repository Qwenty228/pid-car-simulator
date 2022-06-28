from abc import abstractproperty
import time
from xml.sax.handler import property_encoding
import pygame as pg
from settings import *
import os
import math
import numpy as np

def tt():
    return 50, 50

def tl():
    return 100, 0

def tr():
    return 0, 100

class PID:
    def __init__(self, kp, ki, kd) -> None:
        self.p = kp
        self.i = ki
        self.d = kd

        self.sum_error = 0
        self.pre_error = 0
        self.error = 0

        self.res = 0

        self.proportional = 0
        self.integral = 0 
        self.derivative = 0

    @property
    def proportional(self):
        return self._proportional * self.p
    @proportional.setter
    def proportional(self, value):
        self._proportional = value

    @property
    def integral(self):
        return self._integral * self.i
    @integral.setter
    def integral(self, value):
        self._integral = value
    
    @property
    def derivative(self):
        return self._derivative * self.d
    @derivative.setter
    def derivative(self, value):
        self._derivative = value

    def calculate(self, error):
        self.proportional = error
        self.integral = self.sum_error
        self.derivative = error - self.pre_error
        
        self.res = self.proportional + self.integral + self.derivative

        self.pre_error = error
        self.sum_error += error
        return self.res

last_time = 0

class Car(pg.sprite.Sprite):
    def __init__(self, data, surf,  *groups: abstractproperty) -> None:
        super().__init__(*groups)
        self.map = MAP_IMAGE.convert_alpha()
        self.sim_surface = surf
        self.data = data
        pos = data['pos']

        self._image = pg.image.load(os.path.join(CAR_PATH, 'debug.png')).convert_alpha()
        self._image = pg.transform.scale(self._image, (35, int(35*(self._image.get_height()/self._image.get_width()))))
        self.image = self._image
        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=pos)

        self.pos = pg.math.Vector2(pos)
        self.motor_speed = pg.math.Vector2(0, 0)
        self.angle = 0

        self.alive = True
        self._win = False
        self.goal = None

        self.feedback_control = PID(3, 0.01, 1)
        self.check_goal()
        self.turn = 'straight'
      

    @staticmethod
    def blitRotate(image, pos, originPos, angle):
        # offset from pivot to center
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pos - image_rect.center

        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # roatetd image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pg.transform.rotate(image, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        return rotated_image_rect, rotated_image


    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.motor_speed.x, self.motor_speed.y = tt()
        elif keys[pg.K_d]:
            self.motor_speed.x, self.motor_speed.y = tl()
        elif keys[pg.K_a]:
            self.motor_speed.x, self.motor_speed.y = tr()
        else:
            self.motor_speed *= 0.9 if self.motor_speed.magnitude() > 1 else 0

    def ai(self, sensors):
        right, left = sensors

        base_speed = 60

        error = right - left
        d_speed =  self.feedback_control.calculate(error)

        self.motor_speed.x = min(base_speed + d_speed, 100)
        self.motor_speed.y = min(base_speed - d_speed, 100) 



    def move(self):
        global last_time
       
        diff = (self.motor_speed.x - self.motor_speed.y)
        if abs(diff) < 3:
            diff = 0

        if abs(diff) < 50:
            self.turn = 'straight'
        elif diff > 0:
            self.turn = 'right'
        else:
            self.turn = 'left'
     

        self.angle = (self.angle + diff / (self.image.get_height()*0.5)) % 360

        dt = time.time() - last_time
        dt *= 60 # dt = fps * deltatime ---> normalize --> fps * deltatime * default_fps / fps
        if dt > 1000:
            dt = 0

        last_time = time.time()

        # print(, self._image.get_rect().top, self._image.get_rect().bottom)
        #print(self.motor_speed)

    

        speed = (self.motor_speed.x + self.motor_speed.y)*0.05 * dt

        self.pos.x += speed * math.cos(math.radians(-self.angle))
        self.pos.y -= speed * math.sin(math.radians(-self.angle))

        # (self._image.get_rect().centerx, int(np.interp(diff, [-100, 100], [0, self._image.get_rect().bottom])))
        image_rect, self.image = self.blitRotate(self._image, self.pos, self._image.get_rect().center, - self.angle)

        self.rect = image_rect



    def check_radar(self, degree):
        length = 0
        x = int(self.rect.center[0] + math.cos(math.radians(360 - (-self.angle + degree))) * length)
        y = int(self.rect.center[1] + math.sin(math.radians(360 - (-self.angle + degree))) * length)

     

        while (self.map.get_at((x, y)) == (179, 179, 179, 255) or self.goal.sprite.image.get_at((x, y)) == (255, 0, 0, 255)) and length < 50:
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(360 - (-self.angle + degree))) * length)
            y = int(self.rect.center[1] + math.sin(math.radians(360 - (-self.angle + degree))) * length)
    

        dist = int(math.sqrt(math.pow(x - self.rect.center[0], 2) + math.pow(y - self.rect.center[1], 2)))

        #print(self.goal)
        return (x, y), dist
        #self.radars.append([(x, y), dist])

    def draw_radar(self, pos):
        pg.draw.line(self.sim_surface, (0, 255, 0), self.rect.center, pos, 1)
        pg.draw.circle(self.sim_surface, (0, 255, 0), pos, 5)

    def check_goal(self):
        if self.goal is None:
            self.goal = pg.sprite.Sprite()
            self.goal.image =  self.data['goal']
            self.goal.rect = self.goal.image.get_rect()
            self.goal.mask = pg.mask.from_surface(self.goal.image)
            self.goal = pg.sprite.GroupSingle(self.goal)

        return pg.sprite.spritecollide(self, self.goal, False, pg.sprite.collide_mask)
    

    def update(self) -> None:
        infrared = []
        for d in range(-45, 90, 90):
            if self.check_goal():
                self._win = True
                break
            pos, dist = self.check_radar(d)
            infrared.append(dist)
            self.draw_radar(pos)
            if dist == 0:    
                self.alive = False
   
        if not self._win:
            self.input()
            self.ai(infrared)
            self.move()
        else:
            self.alive = False
            #print('goal')

      
            
     
        return super().update()




