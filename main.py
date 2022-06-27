from settings import *
import pygame as pg
import pickle, os

from debug import debug
from map_gen import gen
from car import Car

class Sim(Window):
    def __init__(self, data, title: str = None) -> None:
        super().__init__(title)
        self.bg = MAP_IMAGE.convert_alpha()
        self.data = data
        self.visible_objects = pg.sprite.Group()
        self.start()
     
    def start(self):
        self.car = Car(self.data, self.surface, self.visible_objects) 
        

    def event(self, event: pg.event.get):
        if event.type == pg.KEYDOWN:
            pass
                


    def draw(self):
        self.visible_objects.draw(self.surface)
        self.visible_objects.update()

        if not self.car.alive:
            self.car.kill()
            self.start()

        self.car.debug = self.debug
        if self.debug:
            debug(self.surface, str(self.data))
            self.surface.blit(self.data['goal'], (0, 0))
            pg.draw.circle(self.surface, 'red', self.car.pos, 3)
            
            


if __name__ == "__main__":
    data = gen()
    S = Sim(data, 'Simulator')
    S.mainloop()
    
