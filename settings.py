import pygame as pg
import os

__all__ = ['MAP_IMAGE', 'Window', "CAR_PATH", "CONFIG_PATH", "MAP_PATH"]


CAR_PATH = "data\cars"
CONFIG_PATH = "data\configs"
MAP_PATH = "data\maps"

MAP_IMAGE = pg.image.load(os.path.join(MAP_PATH, 'map.png'))


class Window:
    MAP_SIZE = MAP_IMAGE.get_size()
    FPS = 120
    bg = None
    def __init__(self, title:str=None) -> None:
        pg.init()
        self.debug = False
        self.title = title
        self.ratio = 2
        self.surface = pg.Surface(self.MAP_SIZE)
        self._screen = pg.display.set_mode([self.ratio*i for i in self.MAP_SIZE])
        self.Clock = pg.time.Clock()
        
        self.set_caption(self.title)



    @staticmethod
    def set_caption(title):
        if title:
            pg.display.set_caption(title)



    def _event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_m:
                    self.debug = not self.debug
                    self.set_caption(self.title)
            
            if hasattr(self, "event"):
                self.event(event)



    def mainloop(self):
        self.running = True
        while self.running:
            if self.bg:     self.surface.blit(self.bg, (0, 0))
            if self.debug:  self.set_caption(f'fps: {self.Clock.get_fps():.2f}')
            self._event()
            self.draw()
            self._screen.blit(pg.transform.scale2x(self.surface), (0, 0))
            self.Clock.tick(self.FPS)
            pg.display.flip()



if __name__ == "__main__":
    mapsetup = Window('map')
    mapsetup.mainloop()

    
        


