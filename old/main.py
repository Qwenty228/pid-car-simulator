import pygame as pg
import matplotlib.pyplot as plt

WIDTH, HEIGHT = 500,500
window = pg.display.set_mode((WIDTH,HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()
pg.display.set_caption("pid")
run=True

class car:
    def __init__(self, x,y):
        self.RECT = pg.Rect(x,y,50,75)
        self.RECT.center = (x,y)
        self.VEL = 10
        self.FRIC = 0.5
        self.tick = 0
        self.error = 0
        self.last_error = 0
        self.Terror = 0
        self.movement = []

    def draw(self, surface, color):
        pg.draw.rect(surface, color, self.RECT)

    def moving(self, target):
        kp = 1
        ki = 0.001
        kd = 1


        # sensor timer simulation
        if self.tick >= 10:
            self.error = (target - self.RECT.y)/15
            self.tick = 0
            if self.VEL != 0:
                self.movement.append(abs(self.RECT.y))
        derivative = (self.error - self.last_error)*kd
        if self.Terror <= -200:
            self.Terror += self.error
        else:
            self.Terror = 0

        self.tick += 1
        self.VEL = self.error*kp + self.Terror*ki + derivative + self.VEL*self.FRIC 

        if abs(self.VEL)<= 0.3:
            self.VEL = 0
           
        
        self.RECT.y += self.VEL
        self.last_error = self.error
        
       
        


Car = car(WIDTH/2, HEIGHT*9/10)

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run= False
            
        if event.type == pg.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            window = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        '''if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                plt.plot(Car.movement)
                plt.show()'''
    
    
    window.fill((100,100,100))

    for x in range(WIDTH):
        pg.draw.line(window,'gold',(x, HEIGHT/5 + x**2), (x+1, HEIGHT/5 + (x+1)**2), 3)
    

    Car.moving(HEIGHT/5)
    Car.draw(window,'chartreuse')
    
    pg.display.flip()
    clock.tick(60)

pg.quit()
