from settings import *
import pygame as pg
import pickle, os

from debug import debug, Graph_Display
from map_gen import gen
from car import Car

class Sim(Window):
    def __init__(self, data, title: str = None) -> None:
        super().__init__(title)
        self.bg = MAP_IMAGE.convert_alpha()
        self.data = data
        self.data['FPS'] = self.FPS
        self.visible_objects = pg.sprite.Group()
        self.start()
        self.graph = Graph_Display(300, 60, fps=self.FPS)
     
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

        if self.debug:
            debug(self.surface, str(self.data))
            debug(self.surface, str(self.car.turn), y=40)
            self.surface.blit(self.graph.draw(p=self.car.feedback_control.proportional, 
                                            i=self.car.feedback_control.integral, 
                                            d=self.car.feedback_control.derivative,
                                            pid=self.car.feedback_control.res), 
                                            (self.surface.get_width() - 300, 0))
            self.surface.blit(self.data['goal'], (0, 0))
            pg.draw.circle(self.surface, 'red', self.car.pos, 3)


            
            


if __name__ == "__main__":
    data = gen()
    S = Sim(data, 'Simulator')
    S.mainloop()
