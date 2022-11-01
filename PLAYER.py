################ инит

import os, sys, pygame, mypyganim as pyganim

################ для изобр плеера
width=50
height=50
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'App\\Player')

def Img_Loader(img, img_name):
    global img_folder
    img = pygame.image.load(os.path.join(img_folder, img_name)).convert()
    img=pygame.transform.scale(img,(width,height))
    return img

img=None
player_face_img=Img_Loader(img,'player_face_man.png')
player_movedown_1_img = Img_Loader(img, 'player_movedown_1_man.png')
player_movedown_2_img = Img_Loader(img, 'player_movedown_2_man.png')

player_face_left_img = Img_Loader(img, 'player_face_left_man.png')
player_moveleft_1_img = Img_Loader(img, 'player_left_move_1_man.png')
player_moveleft_2_img = Img_Loader(img, 'player_left_move_2_man.png')

player_face_up_img = Img_Loader(img, 'player_face_up_man.png')
player_moveup_1_img = Img_Loader(img, 'player_up_move_1_man.png')
player_moveup_2_img = Img_Loader(img,'player_up_move_2_man.png')

player_face_right_img = Img_Loader(img, 'player_face_right_man.png')
player_moveright_1_img = Img_Loader(img, 'player_right_move_1_man.png')
player_moveright_2_img = Img_Loader(img, 'player_right_move_2_man.png')

ANIMATION_DOWN = [player_movedown_1_img,player_face_img,player_movedown_2_img]
ANIMATION_UP = [player_moveup_1_img,player_face_up_img,player_moveup_2_img]
ANIMATION_LEFT = [player_moveleft_1_img,player_face_left_img,player_moveleft_2_img]
ANIMATION_RIGHT = [player_moveright_1_img,player_face_right_img,player_moveright_2_img]
ANIMATION_STAY = [(player_face_img,0.1)]


ANIMATION_DELAY = 0.1 # скорость смены кадров
REPEAT = 25
################ цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
DEL_COLOR = BLUE

class Player(pygame.sprite.Sprite):
    count=0
    ################ в целом аналогия с боксами (BOX.py)
    def __init__(self,x=0,y=0):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.image.set_colorkey(DEL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.topleft=(x,y)

        change_anim = []
        for anim in ANIMATION_DOWN:
            change_anim.append((anim, ANIMATION_DELAY))
        self.change_anim_down = pyganim.PygAnimation(change_anim)
        self.change_anim_down.play()

        change_anim = []
        for anim in ANIMATION_UP:
            change_anim.append((anim, ANIMATION_DELAY))
        self.change_anim_up = pyganim.PygAnimation(change_anim)
        self.change_anim_up.play()

        change_anim = []
        for anim in ANIMATION_LEFT:
            change_anim.append((anim, ANIMATION_DELAY))
        self.change_anim_left = pyganim.PygAnimation(change_anim)
        self.change_anim_left.play()

        change_anim = []
        for anim in ANIMATION_RIGHT:
            change_anim.append((anim, ANIMATION_DELAY))
        self.change_anim_right = pyganim.PygAnimation(change_anim)
        self.change_anim_right.play()

        self.change_anim_stay = pyganim.PygAnimation(ANIMATION_STAY)
        self.change_anim_stay.play()
        self.change_anim_stay.blit(self.image, (0, 0))


    ################ ограничения движения
    ################ если верхняя сторона игрока = нижней стороне стены - мы не двигаемся, если еды-двинаемся.
    ################ если двигаем еду, а перед ней стена, то вот и dist пригодился (длина или ширина прямоуг. игрока).
    ################ если двигаем еду, а перед нейй ещё еда, то снова дист (вторая еда = стена)
    def Constraint(self, box, k, dist=0):
        bool=False
        if (k=='UP' and 
            self.rect.top-dist==box.rect.bottom and self.rect.left==box.rect.left and self.rect.right==box.rect.right 
           ): bool=True
        elif (k=='DOWN' and 
            self.rect.bottom+dist==box.rect.top and self.rect.left==box.rect.left and self.rect.right==box.rect.right
           ): bool=True
        elif (k=='LEFT' and 
            self.rect.left-dist==box.rect.right and self.rect.top==box.rect.top and self.rect.bottom==box.rect.bottom
           ): bool=True
        elif (k=='RIGHT' and 
            self.rect.right+dist==box.rect.left and self.rect.top==box.rect.top and self.rect.bottom==box.rect.bottom
           ): bool=True
        return bool

    def Bool_Check(self,g_box,w_box,k,dist=0):
        flag_wall=False;flag_goods=False;j=0
        for i in range (len(w_box)):
            if flag_goods==False:
                if self.Constraint(w_box[i],k): flag_wall=True; break ############### проверим все стены
                try:
                    if flag_goods==False and self.Constraint(g_box[i],k): ################ всю еду
                        flag_goods=True;j=i
                        for z in range (len(g_box)):
                            if (j!=z and self.Constraint(g_box[z],k,dist)): flag_wall=True; break ################ и еду за едой
                except: pass
            elif (flag_goods==True and 
                self.Constraint(w_box[i],k,dist)): flag_wall=True; break ################ и стену за едой, если еда кончилась
        return flag_goods,flag_wall,j

    ################ понимаем где мы ща в пространстве
    def Check_Box(self,g_box,w_box,k,dist=0):
        check_goods=check_wall='Free';j=0
        flag_goods,flag_wall,j=self.Bool_Check(g_box,w_box,k,dist) 
        if k=='UP':        
            if (flag_goods==True): check_goods='Goods-Top'  ################ если сверху еда, то возвращаем, что еда сверху
            if (flag_wall==True): check_wall='Wall-Top' ################ есди сверху стена, то возр, что стена сверху. Остальное 1 в 1
        elif k=='DOWN':
            if (flag_goods==True): check_goods='Goods-Bottom'
            if (flag_wall==True): check_wall='Wall-Bottom'
        elif k=='LEFT':
            if (flag_goods==True): check_goods='Goods-Left'
            if (flag_wall==True): check_wall='Wall-Left'
        elif k=='RIGHT':
            if (flag_goods==True): check_goods='Goods-Right'
            if (flag_wall==True): check_wall='Wall-Right'
        return check_goods,j,check_wall

    ################ понимаение куда двигаться
    def update(self,g_box,w_box,points,up,down,left,right):
        if up or down or left or right:
            if up: key='UP'
            elif down: key='DOWN'
            elif left: key ='LEFT'
            elif right: key='RIGHT'
            SPEED=2
            global REPEAT
            X=self.rect[2]    ################ ширина и длина
            Y=self.rect[3]
            str=''
        
            if up or down: ################ проверка кнопок
                goods_box,i,wall_box=self.Check_Box(g_box,w_box,key,Y)
                if up: 
                    str='Top'; SPEED=-SPEED 
                    anim=self.change_anim_up;
                ################ верх-верх, но игрек должен быть с минусом. низ-низ. присваем строке, чтою несколько раз не переписывать
                elif down: str='Bottom'; anim=self.change_anim_down

                if goods_box=='Goods-'+str: 
                    if wall_box!='Wall-'+str: 
                        g_box[i].Move(0,SPEED,points)#; g_box[i].Change_Collor(points)
                        self.rect.y+=SPEED; Player.count+=1/REPEAT
                        anim.blit(self.image, (0, 0))
                        ################ двигаемся, с едой, если нет стены впереди (или ещё еды)
                elif wall_box!='Wall-'+str:
                    self.rect.y+=SPEED; Player.count+=1/REPEAT################ если не стена без еды, то идём
                    anim.blit(self.image, (0, 0))

            elif left or right: ################ аналогия с верх-низ, только это лево-право
                goods_box,i,wall_box=self.Check_Box(g_box,w_box,key,X)
                if left: 
                    str='Left'; SPEED=-SPEED 
                    anim=self.change_anim_left
                elif right: str='Right';anim=self.change_anim_right

                if goods_box=='Goods-'+str: 
                    if wall_box!='Wall-'+str: 
                        g_box[i].Move(SPEED,0,points)
                        self.rect.x+=SPEED; Player.count+=1/REPEAT
                        anim.blit(self.image, (0, 0))
                elif wall_box!='Wall-'+str: 
                    self.rect.x+=SPEED; Player.count+=1/REPEAT
                    anim.blit(self.image, (0, 0))
            
        else:
            self.image.fill(DEL_COLOR)
            self.change_anim_stay.blit(self.image, (0, 0))
