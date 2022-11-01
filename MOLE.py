################ инит
import os, sys, pygame, pygame.freetype
pygame.init();pygame.freetype.init()
#import time
#successes, failures = pygame.init()
#print("{} successes and {} failures".format(successes, failures)) ################ ПРОВЕРКА УДАВШЕГОСЯ ИНИТА ПАЙГЕЙМА
################ база настроек
WIDTH = 1200 #длина
HEIGHT = 800 #высота
screen = pygame.display.set_mode((WIDTH,HEIGHT)) #сет окна
pygame.display.set_caption("Mole") # навзание окна
clock = pygame.time.Clock()
FPS = 60
################ цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
################ для чтения картинки фона
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'App')
background_img = pygame.image.load(os.path.join(img_folder, 'background.png')).convert()
background_img=pygame.transform.scale(background_img,(WIDTH,HEIGHT))
background_rect = background_img.get_rect()
################ импорт доков
from LEVELES import *
from PLAYER import *
from BOX import *
################
def Tranparent():
    global WIDTH,HEIGHT,screen
    transparent_screen = pygame.Surface((WIDTH,HEIGHT-50), pygame.SRCALPHA) 
    transparent_screen.fill((0,0,0,200))                        
    screen.blit(transparent_screen, (0,20))
################ текст каунтера и победный
def render_multi_line(text, x, y):
    #pygame.event.wait()
    global WHITE,BLACK
    Tranparent()
    fsize=16
    font = pygame.freetype.SysFont('freesansbold.ttf', fsize)
    lines = text.splitlines()
    for i, l in enumerate(lines):
        label, rect_label =font.render(l, WHITE)
        #rect_label=label.get_rect()
        rect_label.topleft=(x, y + 5+fsize*i)
        #rect_label.set_alpha(128)
        screen.blit(label,rect_label)

fontObj = pygame.freetype.SysFont('freesansbold.ttf', 16)
exit_label,rect = fontObj.render("ESC - EXIT", WHITE)
reset_label,rect = fontObj.render("F1 - СПРАВКА", WHITE)
game_label,rect = fontObj.render("ИГРА", WHITE)
status_label,rect = fontObj.render("НЕ ПРОЙДЕНА", RED)
#player_counter = fontObj.render('Количество ходов: {}'.format(Player.count), True, WHITE, BLACK)
#box_counter = fontObj.render('Количесво ходов с грузом: {}'.format(Goods_Box.count), True, WHITE, BLACK)

fontWin = pygame.freetype.SysFont('freesansbold.ttf', 32)
win_label, rect_win = fontWin.render('ИГРА ПРОЙДЕНА!', GREEN)
rect_win.center = (WIDTH//2,HEIGHT//2)

finish_label, rect_finish = fontWin.render('ЛАБИРИНТ ПРОЙДЕН!', GREEN)
rect_finish.center = (WIDTH//2,HEIGHT//2)

enter_label,rect_enter = fontObj.render('Нажмите Enter для продожения', WHITE)
rect_enter.center = (WIDTH//2,HEIGHT//2+50)

help="Клавиша ESC - выход из игры.\nКлавиша R - перезапуск уровня\n\n\
        \nПравила:\n1. Задача игрока перетащить все коробки в отмеченную зону.\n2. Коробоки можно передвигать только перед собой\
        \n3. Игрок не может ходить сквозь стены и коробки.\n4. Коробки скозь стены передвигать тоже нельзя.\n5. Двигать 2 коробки одновременно игрок не может.\
        \n\n\nУдачи!\n\n\nНажмите Enter для продожения..."
################
def Reset_Count():
    Player.count=0
    Goods_Box.count=0
    Goods_Box.recollor_count=0

def Blit_Text(p_count,b_count):
    global player_counter,box_counter,reset_label,exit_label,game_label,status_label,lvl_numb_label,fontObj
    pygame.draw.line(screen,BLACK,(0,0),(WIDTH,0),50)
    pygame.draw.line(screen,BLACK,(0,HEIGHT-10),(WIDTH,HEIGHT-10),50)
    player_counter,rect = fontObj.render('Количество ходов: {:g}'.format(p_count), WHITE) ################ перезаписываем текст для актальной информации счёта
    screen.blit(game_label,(50,5))
    screen.blit(status_label,(102,2))
    screen.blit(player_counter,(320,5)) ################ отображаем его
    box_counter,rect = fontObj.render('Количесво ходов с грузом: {:g}'.format(b_count), WHITE)
    screen.blit(box_counter,(570,5))
    lvl_numb_label,rect = fontObj.render("Лабиринт {}".format(numb+1), WHITE)
    screen.blit(lvl_numb_label,(1000,5))
    screen.blit(reset_label,(175,HEIGHT-25))
    screen.blit(exit_label,(50,HEIGHT-25))
################ в прорисовку элементов
def ANIMATION_ON_SCREEN(all_sprites,player,g_box,up,down,left,right):
    global screen,BLACK,WHITE,FPS,clock,w_box
    screen.fill(WHITE)  ################ заполнить чёрным
    p_count=Player.count
    b_count=Goods_Box.count
    if up or down or left or right: tick=25
    else: tick=1
    for i in range (tick):
        screen.blit(background_img, background_rect) ################ кидаем изобр
        Blit_Text(p_count,b_count)
        player.update(g_box,w_box,points,up,down,left,right)
        all_sprites.draw(screen) ################ все элементы рисуем
        pygame.display.update() # Or pygame.display.flip() ################ обновляем экран
        clock.tick(FPS) ################ ограничиваем по кадрам

def Clear_Screen(lvl,all_sprites,player,g_box,up,down,left,right):
    global WIDTH,HEIGHT
    Reset_Count()
    player,g_box,w_box,points,all_sprites=load_level(lvl,WIDTH,HEIGHT)
    ANIMATION_ON_SCREEN(all_sprites,player,g_box,up,down,left,right)
    return player,g_box,w_box,points,all_sprites

def Press_Bool():
    press=False
    while press==False:
        for event in pygame.event.get(): ################ ждём какое-то собитие (клавитура-мышь)
            if event.type == pygame.KEYDOWN: 
                if event.key==pygame.K_RETURN: press=True

################
up=down=left=right=False
tick=None
keysatate=None
numb=0
################ loop
running = True
player,g_box,w_box,points,all_sprites=load_level(LEVELES[numb],WIDTH,HEIGHT)
while running:
    pygame.event.clear()
    keystate=pygame.key.get_pressed()
    if keystate[pygame.K_r]:
        player,g_box,w_box,points,all_sprites=Clear_Screen(LEVELES[numb],all_sprites,player,g_box,up,down,left,right)
    elif keystate[pygame.K_F1]: 
        render_multi_line(help,50,25); pygame.display.update()
        Press_Bool()
    elif keystate[pygame.K_ESCAPE]: running=False
    else:
        finish_level=False
        if not finish_level: ################ цикл чтоб потом не двигаться
            ################ отображение
            ANIMATION_ON_SCREEN(all_sprites,player,g_box,up,down,left,right)
            ################ условие конца лвла
            if(Goods_Box.recollor_count==len(g_box)): finish_level=True; numb+=1; Reset_Count()
            
            for event in pygame.event.get(): ################ ждём какое-то собитие (клавитура-мышь)
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:################ если кнопка нажата
                    ################start_time = time.time()
                    ################ какая та из стрелок
                    if event.key==pygame.K_UP: up=True
                    elif event.key==pygame.K_DOWN: down=True
                    elif event.key==pygame.K_LEFT: left=True
                    elif event.key==pygame.K_RIGHT: right=True
                elif event.type == pygame.KEYUP:
                    if event.key==pygame.K_UP: up=False
                    elif event.key==pygame.K_DOWN: down=False
                    elif event.key==pygame.K_LEFT: left=False
                    elif event.key==pygame.K_RIGHT: right=False

        if finish_level:
            Tranparent()
            if numb==len(LEVELES): 
                pygame.draw.line(screen,BLACK,(100,0),(300,0),50)
                game_label,rect = fontObj.render("ПРОЙДЕНА", GREEN)
                screen.blit(game_label, (102,2))
                enter_label,rect = fontObj.render('Нажмите любую клавишу для выхода', WHITE)
                screen.blit(enter_label,rect_enter)
                screen.blit(win_label,rect_win); pygame.display.update()
                pygame.event.wait(); running=False
            else:
                screen.blit(finish_label,rect_finish) ################ выводим победителя
                screen.blit(enter_label,rect_enter)
                pygame.display.update() ################ обновляем
                Press_Bool()
                player,g_box,w_box,points,all_sprites=Clear_Screen(LEVELES[numb],all_sprites,player,g_box,up,down,left,right)    
                
print("Exited the game loop. Game will quit...")
pygame.quit() ################ выход