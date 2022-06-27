import pygame as pg
pg.init()
font = pg.font.Font(None, 30)

def debug(display_surface, info: str, y:int = 10, x: int = 10):
    """draw debug text"""
    debug_surf = font.render(str(info), True, 'white')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pg.draw.rect(display_surface, 'black', debug_rect)
    display_surface.blit(debug_surf, debug_rect)