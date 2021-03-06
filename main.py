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
        self.graph = Graph_Display(200, 60, fps=self.FPS)
        #self.debug = True

        self.frames = []

        self.record = True
     
    def start(self):
        self.car = Car(self.data, self.surface, self.visible_objects) 
        

    def event(self, event: pg.event.get):
        if event.type == pg.KEYDOWN:
            pass
                


    def draw(self):
        self.visible_objects.draw(self.surface)
        self.visible_objects.update()

        if self.car._win:
            self.record = False
            
        if not self.car.alive:
            self.car.kill()
            self.start()
        

        if self.debug:
            debug(self.surface, str(self.data))
            debug(self.surface, str(self.car.turn), y=30)
            debug(self.surface, f'KP={self.car.Kp}, KI={self.car.Ki}, KD={self.car.Kd}', y=50)
            influence = {'p':self.car.feedback_control.proportional, 'i':self.car.feedback_control.integral, 'd':self.car.feedback_control.derivative}
            debug(self.surface, f'most influence: {max(influence.items(), key=lambda item: abs(item[1]))}', y=70)
            self.surface.blit(self.graph.draw(p=influence['p'], 
                                            i=influence['i'], 
                                            d=influence['d'],
                                            pid=self.car.feedback_control.res), 
                                            (self.surface.get_width() - 200, 0))
            self.surface.blit(self.data['goal'], (0, 0))
            pg.draw.circle(self.surface, 'red', self.car.pos, 3)
            
        
        if self.record:
            self.frames.append(self.surface.copy())


if __name__ == "__main__":
    data = gen()
    S = Sim(data, 'Simulator')
    S.mainloop()
    pg.quit()

    import imageio as iio
    import numpy as np

    
    writer = iio.get_writer(f"data/vid/{MAP.split('.')[0]}_debug_{S.debug}.gif", fps=24)

    n_frames = len(S.frames)
    step = int(n_frames / 200)

    for i, frame in enumerate(S.frames):
        if i % step == 0:
            frame = pg.surfarray.pixels3d(frame)
            writer.append_data(np.rot90(frame, 3)[...,::-1,:])
            print(f"{i}/{n_frames}")

    writer.close()

    

 