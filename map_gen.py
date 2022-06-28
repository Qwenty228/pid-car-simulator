from settings import *
import pygame as pg
import pickle, os

from debug import debug

class Gen(Window):
    def __init__(self, title: str = None) -> None:
        super().__init__(title)
        self.bg = MAP_IMAGE.convert_alpha()
        self.draw_goal = False
        #self.goal_surface.fill([0,0,0,100])
        self.tool = 'None'
        self._quit = True
     

        try:
            with open(os.path.join(CONFIG_PATH, 'map_config'), 'rb') as file:
                data = pickle.load(file)
                data['goal'] = pg.image.fromstring(data['goal'], self.bg.get_size(), "RGBA")
        except Exception:
            data = {'pos':(0, 0)}
            data['goal'] = pg.Surface(MAP_IMAGE.get_size(),pg.SRCALPHA)

        self.data = data
        self.goal_surface = data['goal']
    
     
    def event(self, event: pg.event.get):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                self.data['pos'] = [int(i/2) for i in pg.mouse.get_pos()]
            if event.key == pg.K_g:
                self.draw_goal = not self.draw_goal
            if event.key == pg.K_r:
                self.goal_surface.fill([0, 0, 0 ,0 ])
     
               



        


    def draw(self):
        if self.draw_goal:
            self.tool = 'Goal draw'
            if any(pg.mouse.get_pressed(5)):
                pg.draw.circle(self.goal_surface, 'red', [int(i/2) for i in pg.mouse.get_pos()], 5)
        else: self.tool = "None"
        self.surface.blit(self.goal_surface, (0, 0))
        pg.draw.circle(self.surface, "black", self.data['pos'], 10)

        debug(self.surface, f'pressed s to set car spawn location, g to {"disable" if self.draw_goal else "enable"} goal tool, r to clear everything, m for debug',
            x=0, y=0)
        if self.debug:
            debug(self.surface, self.data, y=40)
            _ = self.goal_surface.copy()
            _.fill([0,0,0,100])
            self.surface.blit(_, (0, 0))


def gen():
    g = Gen('mapgen')
    g.mainloop()
    data_before_convert = g.data.copy()
    g.data['goal'] = pg.image.tostring(g.goal_surface, "RGBA" )

    # open a file, where you ant to store the data
    with open(os.path.join(CONFIG_PATH, 'map_config'), 'wb') as file:
        # dump information to that file
        pickle.dump(g.data, file)

    return data_before_convert

if __name__ == "__main__":
    gen()
    
