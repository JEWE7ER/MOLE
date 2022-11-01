import pygame
from POINT import *
from BOX import *
from PLAYER import *
pygame.init()

WIDTH_BLOCKS_1 = 23
HEIGHT_BLOCKS_1 = 11
LEVEL_1 = [
    "    -----              ",
    "    -   -              ",
    "    -   -              ",
    "  ---   ---            ",
    "  -       -            ",
    "--- - --- -     -------",
    "-   - --- -------     -",
    "-                 +  *-",
    "----- ---- -=----     -",
    "    -      ---  -------",
    "    --------           ",
]

WIDTH_BLOCKS_2 = 14
HEIGHT_BLOCKS_2 = 10
LEVEL_2 = [
    "------------  ",
    "-*   -     ---",
    "-+   -       -",
    "-    - ----  -",
    "-      = --  -",
    "-    - -    --",
    "------ --    -",
    "  -          -",
    "  -    -     -",
    "  ------------",
]

WIDTH_BLOCKS_3 = 17
HEIGHT_BLOCKS_3 = 10
LEVEL_3 = [
    "        -------- ",
    "        -     =- ",
    "        -  -  -- ",
    "        -     -  ",
    "        --    -  ",
    "---------   - ---",
    "-      --       -",
    "--*      +      -",
    "-      ----------",
    "--------",
]

LEVELES=[(LEVEL_1,WIDTH_BLOCKS_1,HEIGHT_BLOCKS_1),(LEVEL_2,WIDTH_BLOCKS_2,HEIGHT_BLOCKS_2),(LEVEL_3,WIDTH_BLOCKS_3,HEIGHT_BLOCKS_3)]
OBJECT_WIDTH=width #из PLAYER
OBJECT_HEIGHT=height
def load_level(level,WIDTH_SCREEN,HEIGHT_SCREEN):
    lvl=level[0]
    w_blocks=level[1];h_blocks=level[2]
    el_width = w_blocks * width
    el_height = h_blocks * height
    start_x = (WIDTH_SCREEN - el_width) / 2
    start_y = (HEIGHT_SCREEN - el_height) / 2
    sprite = pygame.sprite.Group()
    walls=[] # то, во что мы будем врезаться или опираться
    goods=[] # то, во что мы будем врезаться или опираться
    points=[] # то, во что мы будем врезаться или опираться
    x=start_x
    y=start_y# координаты
    for row in lvl: # вся строка
        for col in row: # каждый символ
            if col == "-":
                w = Wall_Box(x,y,wall_img)
                walls.append(w)
            elif col == "+":
                g = Goods_Box(x,y,goods_close_img)
                goods.append(g)
            elif col == "*":
                p = Point(x+width/2,y+height/2,points_img)
                points.append(p)
            elif col == "=":
                player = Player(x,y)
            x += OBJECT_WIDTH #блоки платформы ставятся на ширине блоков
        y += OBJECT_HEIGHT    #то же самое и с высотой
        x = start_x                   #на каждой новой строчке начинаем с нуля
    
    sprite.add(points)
    sprite.add(player)
    sprite.add(walls)
    sprite.add(goods)
    return player,goods,walls,points,sprite
        