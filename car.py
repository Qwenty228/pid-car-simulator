from abc import abstractproperty
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

class Car(pg.sprite.Sprite):
    def __init__(self, data, surf,  *groups: abstractproperty) -> None:
        super().__init__(*groups)
        self.map = MAP_IMAGE.convert_alpha()
        self.sim_surface = surf
        self.data = data
        pos = data['pos']
        self.debug = False

        self._image = pg.image.load(os.path.join(CAR_PATH, 'debug.png')).convert_alpha()
        self._image = pg.transform.scale(self._image, (35, int(35*(self._image.get_height()/self._image.get_width()))))
        self.image = self._image
        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.image.get_rect(center=pos)

        self.pos = pg.math.Vector2(pos)
        self.motor_speed = pg.math.Vector2(0, 0)
        self.angle = 0

        self.alive = True
        self.goal = None

        self._init_pid()
        self.check_goal()

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


    def _init_pid(self):
        self.sum_error = 0
        self.pre_error = 0

    def pid(self, sensors):
        right, mid, left = sensors

        base_speed = 50

        kp = 1
        ki = 0
        kd = 0.25

        error = right - left
        motor_speed = (kp * error) + (ki * self.sum_error) + (kd * (error - self.pre_error))
        print(motor_speed)
        self.motor_speed.x = base_speed + motor_speed
        self.motor_speed.y = base_speed - motor_speed



        self.pre_error = error
        self.sum_error += error

    def move(self):

        diff = (self.motor_speed.x - self.motor_speed.y)
        if abs(diff) < 3:
            diff = 0
        self.angle = (self.angle + diff / (self.image.get_height()*0.5)) % 360


        # print(, self._image.get_rect().top, self._image.get_rect().bottom)

        speed = (self.motor_speed.x + self.motor_speed.y)/50
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
        for d in range(-45, 90, 45):
            pos, dist = self.check_radar(d)
            infrared.append(dist)
            self.draw_radar(pos)
            # if dist == 0:
            #     if self.check_goal():
            #         print('goal!')
            #     else:
            #         self.alive = False
   
        self.input()
        self.pid(infrared)
        self.move()
                    
     
        return super().update()


