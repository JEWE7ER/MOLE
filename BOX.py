################ инит

import os, sys, pygame, PLAYER
REPEAT = PLAYER.REPEAT
width = PLAYER.width #длина хитбокса игрока
height = PLAYER.height#высота хитбокса игрока
################ берем изображ
game_folder = os.path.dirname(__file__)
img_wall_folder = os.path.join(game_folder, 'App\\Wall')
img_goods_folder = os.path.join(game_folder, 'App\\Goods')
def Img_Loader(img, img_name,img_folder):
    global width,height
    img = pygame.image.load(os.path.join(img_folder, img_name)).convert()
    img=pygame.transform.scale(img,(width,height))
    return img

img=None
wall_img = Img_Loader(img, 'wall_2.png',img_wall_folder)
goods_close_img = Img_Loader(img, 'box_close_2.png',img_goods_folder)
goods_open_img = Img_Loader(img, 'box_open_2.png',img_goods_folder)
################ цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

################ классы стен и боксов с едой
class Wall_Box(pygame.sprite.Sprite):
    def __init__(self,x=0,y=0,img=None):
        super().__init__()
        self.image=img ################ присваиваем изобр стенам
        self.image.set_colorkey(WHITE) ################ убираем чёрный контур
        self.rect = self.image.get_rect() ################ берем спрайт
        self.rect.topleft=(x,y) ################ размещение


class Goods_Box(pygame.sprite.Sprite):
    count=0;recollor_count=0
    ################ аналогично со стеной
    def __init__(self,x=0,y=0,img=None):
        super().__init__()
        self.image=img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)
        self.recollor=False
    
    ################ прост передача для мува для пайгейма
    def Move(self,x,y,point):
        self.rect.x+=x
        self.rect.y+=y
        Goods_Box.count+=1/REPEAT
        self.Change_Collor(point)

    def Change_Collor(self,point):
        if self.recollor==True: ################ если цвет поменли и ушли с круга, то цвет по дефолту
            self.image=goods_close_img
            Goods_Box.recollor_count-=1
            self.recollor=False
        
        ################ попали в круг - меняем цвет. поменяли-вышли
        for i in range (len(point)): ################ но если ушли с круга на круг, то прост снова даём цвет
            if self.rect.collidepoint(point[i].rect.x,point[i].rect.y): 
                self.image = goods_open_img
                self.image.set_colorkey(BLACK)
                Goods_Box.recollor_count+=1
                self.recollor=True
                break
