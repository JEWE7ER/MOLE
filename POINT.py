################ инит

import os, sys, pygame, PLAYER
width = PLAYER.width #длина хитбокса игрока
height = PLAYER.height
################ цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'App\\Points')
points_img = pygame.image.load(os.path.join(img_folder, 'points.png')).convert()
points_img=pygame.transform.scale(points_img,(width,height))


class Point(pygame.sprite.Sprite):
    def __init__(self,x=0,y=0,img=None):
        super().__init__()
        self.image=img
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)
