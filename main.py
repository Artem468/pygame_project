import pygame
import os
import sys
import random

MAP = ''
pygame.init()
size = width, height = 900, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Танки v.2.0')
clock = pygame.time.Clock()
pygame.mixer.init()

all_sprites = pygame.sprite.Group()
first_preview_sprites = pygame.sprite.Group()
second_preview_sprites = pygame.sprite.Group()
right_st_wall = pygame.sprite.Group()
left_st_wall = pygame.sprite.Group()
up_st_wall = pygame.sprite.Group()
down_st_wall = pygame.sprite.Group()

MUSIC = True
SOUNDS = True
flag_description = False
flag_pause = False
flag_sound = True
first_size = False
second_size = False
flag_finish = ''
flag_tanks = False
first_tp_flag = False
second_tp_flag = False
first_portal_self = ''
second_portal_self = ''
FPS = 60
FIRST_TIME_RELOAD = 1500
SECOND_TIME_RELOAD = 1500
FIRST_SPEED = 1
SECOND_SPEED = 1
FIRST_PLAYER = 'blue'
SECOND_PLAYER = 'red'
FIRST_HP = 100
SECOND_HP = 100
box_sound = pygame.mixer.Sound('data/box_sound.mp3')
box_sound.set_volume(0.4)

first_drive_sound = pygame.mixer.Sound('data/drive_sound.mp3')
second_drive_sound = pygame.mixer.Sound('data/drive_sound.mp3')


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('wooden_box.png'),
    'empty': load_image('sand.png')
}

tile_images2 = {
    'wall': load_image('iron_box.png'),
    'empty': load_image('wood.png')
}

tile_images3 = {
    'wall': load_image('ice_box.png'),
    'empty': load_image('snow.png')
}
tile_width = tile_height = 90
pygame.display.set_icon(load_image('icon.png'))


class ScreenFrame(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


player = None
sprite_group = SpriteGroup()


class Border_hor_up(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__()
        self.add(up_st_wall)
        self.image = pygame.Surface([90, 1])
        self.image.fill((128, 128, 128))
        self.rect = pygame.Rect(x1 * 90, y1 * 90, 90, -1)


class Border_hor_down(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__()
        self.add(down_st_wall)
        self.image = pygame.Surface([90, 1])
        self.image.fill((128, 128, 128))
        self.rect = pygame.Rect(x1 * 90, y1 * 90 + 90, 90, 1)


class Border_ver_left(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__()
        self.add(left_st_wall)
        self.image = pygame.Surface([1, 90])
        self.image.fill((128, 128, 128))
        self.rect = pygame.Rect(x1 * 90 + 90, y1 * 90, 1, 90)


class Border_ver_right(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__()
        self.add(right_st_wall)
        self.image = pygame.Surface([1, 90])
        self.image.fill((128, 128, 128))
        self.rect = pygame.Rect(x1 * 90, y1 * 90, -1, 90)


class Tile(Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        if MAP == 'first_map.map':
            self.image = tile_images[tile_type]
        elif MAP == 'second_map.map':
            self.image = tile_images2[tile_type]
        elif MAP == 'third_map.map':
            self.image = tile_images3[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    global spisok_wall
    spisok_wall = []
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
                Border_hor_up(x, y)
                Border_hor_down(x, y)
                Border_ver_left(x, y)
                Border_ver_right(x, y)
                spisok_wall.append(f'{x} {y}')


def tanks_preview_update():
    global tank1, tank2, flag_tanks
    if flag_tanks:
        tank1.rect.x = -200
        tank2.rect.x = 1100
        tank1 = First_tank_preview(first_preview_sprites)
        tank2 = Second_tank_preview(second_preview_sprites)
        tank1.rect.x = -90
        tank2.rect.x = 900
        im = load_image(f'{FIRST_PLAYER}_tank.png')
        im = pygame.transform.scale(im, (90, 90))
        im = pygame.transform.rotate(im, 270)
        tank1.image = im
        im = load_image(f'{SECOND_PLAYER}_tank.png')
        im = pygame.transform.scale(im, (90, 90))
        im = pygame.transform.rotate(im, 90)
        tank2.image = im
    else:
        tank1 = First_tank_preview(first_preview_sprites)
        tank2 = Second_tank_preview(second_preview_sprites)
        flag_tanks = True


class First_tank_preview(pygame.sprite.Sprite):
    image = load_image(f'{FIRST_PLAYER}_tank.png')
    image = pygame.transform.scale(image, (90, 90))
    image = pygame.transform.rotate(image, -90)

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -90, 600
        self.speed = 5

    def update(self, *args):
        self.rect.x += self.speed
        if self.rect.x >= 1000:
            self.rect.x = -90


class Second_tank_preview(pygame.sprite.Sprite):
    image = load_image(f'{SECOND_PLAYER}_tank.png')
    image = pygame.transform.scale(image, (90, 90))
    image = pygame.transform.rotate(image, 90)

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 900, 700
        self.speed = 5

    def update(self, *args):
        self.rect.x -= self.speed
        if self.rect.x <= -100:
            self.rect.x = 990


def select_skin_update(player):
    fon = pygame.transform.scale(load_image('background.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(r'data\teletactile.ttf', 50)
    text_coord = width // 2
    string_rendered = font.render(player, True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord -= string_rendered.get_width() // 2
    intro_rect.top = 70
    intro_rect.x = text_coord
    pygame.draw.rect(screen, 'green',
                     (intro_rect.x - 5, intro_rect.y - 6, intro_rect.width + 10, intro_rect.height + 8))
    screen.blit(string_rendered, intro_rect)

    pygame.draw.rect(screen, 'grey', (15, 15, 40, 40))
    back = pygame.transform.scale(load_image('back.png'), (40, 40))
    screen.blit(back, (15, 14))

    blue = pygame.transform.scale(load_image('blue_tank.png'), (90, 90))
    red = pygame.transform.scale(load_image('red_tank.png'), (90, 90))
    green = pygame.transform.scale(load_image('green_tank.png'), (90, 90))
    screen.blit(blue, (200, height // 2 - 45))
    screen.blit(red, (400, height // 2 - 45))
    screen.blit(green, (600, height // 2 - 45))


def select_skin(player):
    select_skin_update(player)
    global FIRST_PLAYER, SECOND_PLAYER
    done = pygame.transform.scale(load_image('done.png'), (20, 20))
    if player == '1st player':
        if FIRST_PLAYER == 'blue':
            pygame.draw.rect(screen, 'green', (235, height // 2 + 55, 20, 20))
            screen.blit(done, (234, height // 2 + 55))
        elif FIRST_PLAYER == 'red':
            pygame.draw.rect(screen, 'green', (435, height // 2 + 55, 20, 20))
            screen.blit(done, (434, height // 2 + 55))
        else:
            pygame.draw.rect(screen, 'green', (635, height // 2 + 55, 20, 20))
            screen.blit(done, (634, height // 2 + 55))
    if player == '2nd player':
        if SECOND_PLAYER == 'blue':
            pygame.draw.rect(screen, 'green', (235, height // 2 + 55, 20, 20))
            screen.blit(done, (234, height // 2 + 55))
        elif SECOND_PLAYER == 'red':
            pygame.draw.rect(screen, 'green', (435, height // 2 + 55, 20, 20))
            screen.blit(done, (434, height // 2 + 55))
        else:
            pygame.draw.rect(screen, 'green', (635, height // 2 + 55, 20, 20))
            screen.blit(done, (634, height // 2 + 55))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 15 and event.pos[0] <= 55:
                    if event.pos[1] >= 15 and event.pos[1] <= 55:
                        return
                if event.pos[1] >= height // 2 - 45 and event.pos[1] <= height // 2 + 45:
                    if event.pos[0] >= 200 and event.pos[0] <= 290:
                        select_skin_update(player)
                        pygame.draw.rect(screen, 'green', (235, height // 2 + 55, 20, 20))
                        screen.blit(done, (234, height // 2 + 55))
                        if player == '1st player':
                            FIRST_PLAYER = 'blue'
                        else:
                            SECOND_PLAYER = 'blue'
                    if event.pos[0] >= 400 and event.pos[0] <= 490:
                        select_skin_update(player)
                        pygame.draw.rect(screen, 'green', (435, height // 2 + 55, 20, 20))
                        screen.blit(done, (434, height // 2 + 55))
                        if player == '1st player':
                            FIRST_PLAYER = 'red'
                        else:
                            SECOND_PLAYER = 'red'
                    if event.pos[0] >= 600 and event.pos[0] <= 690:
                        select_skin_update(player)
                        pygame.draw.rect(screen, 'green', (635, height // 2 + 55, 20, 20))
                        screen.blit(done, (634, height // 2 + 55))
                        if player == '1st player':
                            FIRST_PLAYER = 'green'
                        else:
                            SECOND_PLAYER = 'green'
        pygame.display.flip()
        clock.tick(FPS)


def start_screen_update():
    intro_text = ['Tanks v. 2.0']

    fon = pygame.transform.scale(load_image('background.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(r'data\teletactile.ttf', 60)
    text_coord = width // 2
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord -= string_rendered.get_width() // 2
        intro_rect.top = 70
        intro_rect.x = text_coord
        pygame.draw.rect(screen, 'green',
                         (intro_rect.x - 5, intro_rect.y - 6, intro_rect.width + 10, intro_rect.height + 8))
        screen.blit(string_rendered, intro_rect)

    pygame.draw.rect(screen, 'green', (365, 300, 165, 50))
    font = pygame.font.Font(r'data\teletactile.ttf', 50)
    string_rendered = font.render('Play', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = width // 2 - string_rendered.get_width() // 2
    intro_rect.y = 305
    screen.blit(string_rendered, intro_rect)

    pygame.draw.rect(screen, 'green', (180, 400, 260, 35))
    font = pygame.font.Font(r'data\teletactile.ttf', 30)
    string_rendered = font.render('1st player', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = width // 2 - string_rendered.get_width() // 2 - 140
    intro_rect.y = 405
    screen.blit(string_rendered, intro_rect)

    pygame.draw.rect(screen, 'green', (470, 400, 260, 35))
    font = pygame.font.Font(r'data\teletactile.ttf', 30)
    string_rendered = font.render('2nd player', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = width // 2 - string_rendered.get_width() // 2 + 150
    intro_rect.y = 405
    screen.blit(string_rendered, intro_rect)

    pygame.draw.rect(screen, 'grey', (845, 15, 40, 40))
    settings = pygame.transform.scale(load_image('settings.png'), (40, 40))
    screen.blit(settings, (845, 14))

    font = pygame.font.Font(r'data\teletactile.ttf', 25)
    string_rendered = font.render('Description', True, pygame.Color('black'))
    pygame.draw.rect(screen, 'grey', (10, 12, string_rendered.get_width() + 10, string_rendered.get_height() + 3))
    screen.blit(string_rendered, (15, 15))

    return 10, string_rendered.get_width() + 20, 12, string_rendered.get_height() + 15


def start_screen():
    x1, x2, y1, y2 = start_screen_update()
    tanks_preview_update()
    global start_screen_sound, flag_sound, flag_description
    while True:
        if flag_sound:
            if MUSIC:
                start_screen_sound = pygame.mixer.Sound('data/sound_lobby.mp3')
                start_screen_sound.play(-1)
                start_screen_sound.set_volume(0.5)
                flag_sound = False
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= x1 and event.pos[0] <= x2:
                    if event.pos[1] >= y1 and event.pos[1] <= y2:
                        flag_description = not flag_description
                if event.pos[0] >= 845 and event.pos[0] <= 885:
                    if event.pos[1] >= 15 and event.pos[1] <= 55:
                        flag_description = False
                        settings()
                        start_screen_update()
                        tanks_preview_update()
                if event.pos[0] >= 365 and event.pos[0] <= 530:
                    if event.pos[1] >= 300 and event.pos[1] <= 350:
                        flag_description = False
                        tank1.rect.x = -200
                        tank2.rect.x = -200
                        map_select()
                        start_screen_update()
                        tanks_preview_update()
                if event.pos[0] >= 180 and event.pos[0] <= 440:
                    if event.pos[1] >= 400 and event.pos[1] <= 435:
                        flag_description = False
                        select_skin('1st player')
                        start_screen_update()
                        tanks_preview_update()
                if event.pos[0] >= 470 and event.pos[0] <= 730:
                    if event.pos[1] >= 400 and event.pos[1] <= 435:
                        flag_description = False
                        select_skin('2nd player')
                        start_screen_update()
                        tanks_preview_update()
        start_screen_update()
        tank1.update()
        tank2.update()
        first_preview_sprites.draw(screen)
        second_preview_sprites.draw(screen)
        if flag_description:
            description()
        pygame.display.flip()


def map_select():
    global flag_sound
    fon = pygame.transform.scale(load_image('background.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(r'data\teletactile.ttf', 50)
    text_coord = width // 2
    string_rendered = font.render('Map Select', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord -= string_rendered.get_width() // 2
    intro_rect.top = 20
    intro_rect.x = text_coord
    pygame.draw.rect(screen, 'green',
                     (intro_rect.x - 5, intro_rect.y - 6, intro_rect.width + 8, intro_rect.height + 8))
    screen.blit(string_rendered, intro_rect)

    pygame.draw.rect(screen, 'grey', (15, 15, 40, 40))
    back = pygame.transform.scale(load_image('back.png'), (40, 40))
    screen.blit(back, (15, 14))

    map1 = load_image('map1.jpg')
    map1 = pygame.transform.scale(map1, (150, 150))
    screen.blit(map1, (width // 4 - 100, height // 2 - map1.get_height() // 2))

    map2 = load_image('map2.jpg')
    map2 = pygame.transform.scale(map2, (150, 150))
    screen.blit(map2, (width // 2 - map2.get_width() // 2, height // 2 - map2.get_height() // 2))

    map3 = load_image('map3.jpg')
    map3 = pygame.transform.scale(map3, (150, 150))
    screen.blit(map3, (width // 3 + width // 3 - map3.get_width() // 2 + 100, height // 2 - map3.get_height() // 2))

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                global MAP
                if event.pos[0] >= 15 and event.pos[0] <= 55:
                    if event.pos[1] >= 15 and event.pos[1] <= 55:
                        return
                if event.pos[0] >= width // 4 - 100 and event.pos[0] <= (width // 4 - 100) + 150:
                    if event.pos[1] >= height // 2 - map1.get_height() // 2 and event.pos[1] <= (height // 2 - map1.get_height() // 2) + 150:
                        start_screen_sound.stop()
                        MAP = 'first_map.map'
                        flag_sound = True
                        main()
                        return
                if event.pos[0] >= width // 2 - map2.get_width() // 2 and event.pos[0] <= (width // 2 - map2.get_width() // 2) + 150:
                    if event.pos[1] >= height // 2 - map1.get_height() // 2 and event.pos[1] <= (height // 2 - map1.get_height() // 2) + 150:
                        start_screen_sound.stop()
                        MAP = 'second_map.map'
                        flag_sound = True
                        main()
                        return
                if event.pos[0] >= width // 3 + width // 3 - map3.get_width() // 2 + 100 and event.pos[0] <= (width // 3 + width // 3 - map3.get_width() // 2 + 100) + 150:
                    if event.pos[1] >= height // 2 - map1.get_height() // 2 and event.pos[1] <= (height // 2 - map1.get_height() // 2) + 150:
                        start_screen_sound.stop()
                        MAP = 'third_map.map'
                        flag_sound = True
                        main()
                        return
        pygame.display.flip()


def print_health():
    font = pygame.font.Font(r'data\teletactile.ttf', 50)
    text_coord = width // 4
    string_rendered = font.render(str(FIRST_HP), True, pygame.Color(FIRST_PLAYER))
    intro_rect = string_rendered.get_rect()
    text_coord -= string_rendered.get_width() // 2
    intro_rect.top = 20
    intro_rect.x = text_coord
    screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(r'data\teletactile.ttf', 50)
    text_coord = width // 2 + width // 4
    string_rendered = font.render(str(SECOND_HP), True, pygame.Color(SECOND_PLAYER))
    intro_rect = string_rendered.get_rect()
    text_coord -= string_rendered.get_width() // 2
    intro_rect.top = 20
    intro_rect.x = text_coord
    screen.blit(string_rendered, intro_rect)


def finish_screen(player):
    pygame.mouse.set_visible(True)
    screen.fill((0, 0, 0))
    font = pygame.font.Font(r'data\teletactile.ttf', 50)
    text_coord = width // 2
    if player == 'First player':
        string_rendered = font.render(f'Winer: {player}', True, pygame.Color(FIRST_PLAYER))
    else:
        string_rendered = font.render(f'Winer: {player}', True, pygame.Color(SECOND_PLAYER))
    intro_rect = string_rendered.get_rect()
    text_coord -= string_rendered.get_width() // 2
    intro_rect.top = height // 2 - font.get_height() // 2 - 100
    intro_rect.x = text_coord
    screen.blit(string_rendered, intro_rect)

    pygame.draw.rect(screen, 'green', (300, 550, 255, 45))
    font = pygame.font.Font(r'data\teletactile.ttf', 50)
    string_rendered = font.render('Finish', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 305
    intro_rect.y = 553
    screen.blit(string_rendered, intro_rect)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 300 and event.pos[0] <= 600:
                    if event.pos[1] >= 550 and event.pos[1] <= 605:
                        return
        pygame.display.flip()


def settings_update():
    fon = pygame.transform.scale(load_image('background.png'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(r'data\teletactile.ttf', 50)
    text_coord = width // 2
    string_rendered = font.render('Settings', True, pygame.Color('black'))
    intro_rect = string_rendered.get_rect()
    text_coord -= string_rendered.get_width() // 2
    intro_rect.top = 20
    intro_rect.x = text_coord
    pygame.draw.rect(screen, 'green',
                     (intro_rect.x - 5, intro_rect.y - 6, intro_rect.width + 8, intro_rect.height + 8))
    screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(r'data\teletactile.ttf', 50)
    string_rendered = font.render('Music', True, pygame.Color('black'))
    music_text_coord_x = width // 2 - string_rendered.get_width() // 2
    music_text_coord_y = height // 2 - string_rendered.get_height()
    pygame.draw.rect(screen, 'green',
                     (music_text_coord_x - 5, music_text_coord_y - 6, string_rendered.get_width() + 8,
                      string_rendered.get_height() + 8))
    screen.blit(string_rendered, (music_text_coord_x, music_text_coord_y))


    string_rendered = font.render('Sounds', True, pygame.Color('black'))
    sound_text_coord_x = width // 2 - string_rendered.get_width() // 2
    sound_text_coord_y = height // 2 + string_rendered.get_height()
    pygame.draw.rect(screen, 'green',
                     (sound_text_coord_x - 5, sound_text_coord_y - 6, string_rendered.get_width() + 8,
                      string_rendered.get_height() + 8))
    screen.blit(string_rendered, (sound_text_coord_x, sound_text_coord_y))

    pygame.draw.rect(screen, 'grey', (15, 15, 40, 40))
    back = pygame.transform.scale(load_image('back.png'), (40, 40))
    screen.blit(back, (15, 14))

    return music_text_coord_x, music_text_coord_y, sound_text_coord_x, sound_text_coord_y


def settings():
    global MUSIC, SOUNDS, start_screen_sound, flag_sound
    m_x, m_y, s_x, s_y = settings_update()
    toogle_on = load_image('toogle_on.png')
    toogle_off = load_image('toogle_off.png')

    if MUSIC:
        screen.blit(toogle_on, (m_x + 300, m_y - 5))
    else:
        screen.blit(toogle_off, (m_x + 300, m_y - 5))
    if SOUNDS:
        screen.blit(toogle_on, (s_x + 320, s_y - 5))
    else:
        screen.blit(toogle_off, (s_x + 320, s_y - 5))

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 15 and event.pos[0] <= 55:
                    if event.pos[1] >= 15 and event.pos[1] <= 55:
                        return
                if event.pos[0] >= m_x + 300 and event.pos[0] <= m_x + 348:
                    if event.pos[1] >= m_y - 5 and event.pos[1] <= m_y + 43:
                        settings_update()
                        if MUSIC:
                            screen.blit(toogle_off, (m_x + 300, m_y - 5))
                            MUSIC = False
                            start_screen_sound.stop()
                            flag_sound = True
                            if SOUNDS:
                                screen.blit(toogle_on, (s_x + 320, s_y - 5))
                            else:
                                screen.blit(toogle_off, (s_x + 320, s_y - 5))
                        else:
                            screen.blit(toogle_on, (m_x + 300, m_y - 5))
                            MUSIC = True
                            if flag_sound:
                                start_screen_sound.play(-1)
                                flag_sound = False
                            if SOUNDS:
                                screen.blit(toogle_on, (s_x + 320, s_y - 5))
                            else:
                                screen.blit(toogle_off, (s_x + 320, s_y - 5))
                if event.pos[0] >= s_x + 320 and event.pos[0] <= s_x + 368:
                    if event.pos[1] >= s_y - 5 and event.pos[1] <= s_y + 43:
                        settings_update()
                        if SOUNDS:
                            screen.blit(toogle_off, (s_x + 320, s_y - 5))
                            SOUNDS = False
                            if MUSIC:
                                screen.blit(toogle_on, (m_x + 300, m_y - 5))
                            else:
                                screen.blit(toogle_off, (m_x + 300, m_y - 5))
                        else:
                            screen.blit(toogle_on, (s_x + 320, s_y - 5))
                            SOUNDS = True
                            if MUSIC:
                                screen.blit(toogle_on, (m_x + 300, m_y - 5))
                            else:
                                screen.blit(toogle_off, (m_x + 300, m_y - 5))
        pygame.display.flip()


def description():
    color = pygame.Surface((500, 575))
    color.set_alpha(220)
    color.fill((0, 0, 0))
    screen.blit(color, (0, 50))

    med_box = pygame.transform.scale(load_image('med_box.jpg'), (60, 60))
    small_box = pygame.transform.scale(load_image('small_box.jpg'), (60, 60))
    bullet_box = pygame.transform.scale(load_image('bullet_box.jpg'), (60, 60))
    fast_box = pygame.transform.scale(load_image('fast_box.jpg'), (60, 60))
    wasd = pygame.transform.scale(load_image('wasd.png'), (150, 90))
    arrows = pygame.transform.scale(load_image('arrows.png'), (150, 90))
    shift = pygame.transform.scale(load_image('shift.png'), (118, 50))
    font = pygame.font.Font(None, 21)
    font2 = pygame.font.Font(None, 25)
    font3 = pygame.font.Font(None, 120)

    screen.blit(med_box, (100, 80))
    text = font2.render('Аптечка', True, pygame.Color('white'))
    screen.blit(text, (100, 150))
    text = font.render('Подобрав этот бонус,', True, pygame.Color('white'))
    screen.blit(text, (70, 180))
    text = font.render('здоровье Вашего танка', True, pygame.Color('white'))
    screen.blit(text, (65, 195))
    text = font.render('увеличится на 50 единиц!', True, pygame.Color('white'))
    screen.blit(text, (60, 210))

    screen.blit(fast_box, (330, 80))
    text = font2.render('Ускорение', True, pygame.Color('white'))
    screen.blit(text, (315, 150))
    text = font.render('Эта суперспособность', True, pygame.Color('white'))
    screen.blit(text, (285, 180))
    text = font.render('добавляет скорость', True, pygame.Color('white'))
    screen.blit(text, (290, 195))
    text = font.render('Вашему танку на 10 сек.', True, pygame.Color('white'))
    screen.blit(text, (280, 210))

    screen.blit(bullet_box, (100, 260))
    text = font2.render('Скорострельность', True, pygame.Color('white'))
    screen.blit(text, (60, 340))
    text = font.render('С помощью этого', True, pygame.Color('white'))
    screen.blit(text, (75, 370))
    text = font.render('улучшения, скорость', True, pygame.Color('white'))
    screen.blit(text, (65, 385))
    text = font.render('перезарядки у Вашего', True, pygame.Color('white'))
    screen.blit(text, (60, 400))
    text = font.render('танка станет равна 0', True, pygame.Color('white'))
    screen.blit(text, (65, 415))
    text = font.render('на 10 секунд!', True, pygame.Color('white'))
    screen.blit(text, (80, 430))

    screen.blit(small_box, (330, 260))
    text = font2.render('Уменьшение', True, pygame.Color('white'))
    screen.blit(text, (310, 340))
    text = font.render('Данная суперспособность', True, pygame.Color('white'))
    screen.blit(text, (275, 370))
    text = font.render('уменьшает Ваш танк', True, pygame.Color('white'))
    screen.blit(text, (290, 385))
    text = font.render('почти в 2 раза на 10 сек.', True, pygame.Color('white'))
    screen.blit(text, (280, 400))

    screen.blit(wasd, (30, 460))
    text = font3.render('/', True, pygame.Color('white'))
    screen.blit(text, (200, 470))
    screen.blit(arrows, (235, 460))
    text = font2.render('- движение', True, pygame.Color('white'))
    screen.blit(text, (390, 490))
    text = font2.render('танка', True, pygame.Color('white'))
    screen.blit(text, (420, 505))

    screen.blit(shift, (120, 570))
    text = font2.render('- стрельба танка', True, pygame.Color('white'))
    screen.blit(text, (250, 585))


med_box_sprites = pygame.sprite.Group()
fast_box_sprites = pygame.sprite.Group()
small_box_sprites = pygame.sprite.Group()
bullet_box_sprites = pygame.sprite.Group()
portal_sprites = pygame.sprite.Group()


class Portal(pygame.sprite.Sprite):
    image = load_image('portal.png')
    image = pygame.transform.scale(image, (90, 90))

    def __init__(self):
        super(Portal, self).__init__(portal_sprites)
        self.image = Portal.image
        flag = True
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -100, -100
        self.time = pygame.time.get_ticks()
        while flag:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            gg = f'{x} {y}'
            if gg not in spisok_wall:
                flag = False
                self.rect.x = x * 90
                self.rect.y = y * 90

    def update(self):
        global first_size, second_size, first_tp_flag, second_tp_flag, first_portal_self, second_portal_self
        if pygame.time.get_ticks() - self.time >= 20000:
            self.rect.x, self.rect.y = -100, -100
        if pygame.sprite.spritecollideany(self, first_sprites):
            first_size = 'small'
            self.rect.x, self.rect.y = -100, -100
            first_tp_flag = True
            first_portal_self = self
            if SOUNDS:
                teleport_sound = pygame.mixer.Sound("data/teleport.mp3")
                teleport_sound.set_volume(0.6)
                teleport_sound.play()

        elif pygame.sprite.spritecollideany(self, second_sprites):
            second_size = 'small'
            self.rect.x, self.rect.y = -100, -100
            second_tp_flag = True
            second_portal_self = self
            if SOUNDS:
                teleport_sound = pygame.mixer.Sound("data/teleport.mp3")
                teleport_sound.set_volume(0.6)
                teleport_sound.play()


class Med_Box(pygame.sprite.Sprite):
    image = load_image('med_box.jpg')
    image = pygame.transform.scale(image, (45, 45))

    def __init__(self):
        super(Med_Box, self).__init__(med_box_sprites)
        self.image = Med_Box.image
        flag = True
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -100, -100
        while flag:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            gg = f'{x} {y}'
            if gg not in spisok_wall:
                flag = False
                self.rect.x = x * 90 + 22
                self.rect.y = y * 90 + 22

    def update(self):
        global FIRST_HP, SECOND_HP, box_sound
        if pygame.sprite.spritecollideany(self, first_sprites):
            if SOUNDS:
                box_sound.play()
            self.rect.x, self.rect.y = -100, -100
            if FIRST_HP >= 50:
                FIRST_HP = 100
            else:
                FIRST_HP += 50
        elif pygame.sprite.spritecollideany(self, second_sprites):
            if SOUNDS:
                box_sound.play()
            self.rect.x, self.rect.y = -100, -100
            if SECOND_HP >= 50:
                SECOND_HP = 100
            else:
                SECOND_HP += 50


class Fast_Box(pygame.sprite.Sprite):
    image = load_image('fast_box.jpg')
    image = pygame.transform.scale(image, (45, 45))

    def __init__(self):
        super(Fast_Box, self).__init__(fast_box_sprites)
        self.image = Fast_Box.image
        flag = True
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -100, -100
        self.time = 0
        self.player = ''
        while flag:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            gg = f'{x} {y}'
            if gg not in spisok_wall:
                flag = False
                self.rect.x = x * 90 + 22
                self.rect.y = y * 90 + 22

    def update(self):
        global FIRST_SPEED, SECOND_SPEED, box_sound
        if pygame.sprite.spritecollideany(self, first_sprites):
            if not first_selff.box_flag:
                if SOUNDS:
                    box_sound.play()
                first_selff.super = 'fast'
                self.rect.x, self.rect.y = -100, -100
                FIRST_SPEED += 2
                self.time = pygame.time.get_ticks()
                self.player = 'first'
                first_selff.box_flag = True
        elif pygame.sprite.spritecollideany(self, second_sprites):
            if not second_selff.box_flag:
                if SOUNDS:
                    box_sound.play()
                second_selff.super = 'fast'
                self.rect.x, self.rect.y = -100, -100
                SECOND_SPEED += 2
                self.time = pygame.time.get_ticks()
                self.player = 'second'
                second_selff.box_flag = True
        if self.time != 0:
            if pygame.time.get_ticks() - self.time >= 10000:
                if self.player == 'first':
                    first_selff.box_flag = False
                    FIRST_SPEED -= 2
                    self.time = 0
                    first_selff.super = ''
                elif self.player == 'second':
                    second_selff.box_flag = False
                    SECOND_SPEED -= 2
                    self.time = 0
                    second_selff.super = ''


class Small_Box(pygame.sprite.Sprite):
    image = load_image('small_box.jpg')
    image = pygame.transform.scale(image, (45, 45))

    def __init__(self):
        super(Small_Box, self).__init__(small_box_sprites)
        self.image = Small_Box.image
        flag = True
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -100, -100
        self.time = 0
        self.player = ''
        self.flag = True
        while flag:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            gg = f'{x} {y}'
            if gg not in spisok_wall:
                flag = False
                self.rect.x = x * 90 + 22
                self.rect.y = y * 90 + 22

    def update(self):
        global first_size, second_size, FIRST_SPEED, SECOND_SPEED, box_sound, first_selff, second_selff
        if pygame.sprite.spritecollideany(self, first_sprites):
            if not first_selff.box_flag:
                if SOUNDS:
                    box_sound.play()
                self.rect.x, self.rect.y = -100, -100
                self.time = pygame.time.get_ticks()
                self.player = 'first'
                first_selff.super = 'small'
                first_size = 'small'
                first_selff.box_flag = True
        elif pygame.sprite.spritecollideany(self, second_sprites):
            if not second_selff.box_flag:
                if SOUNDS:
                    box_sound.play()
                self.rect.x, self.rect.y = -100, -100
                self.time = pygame.time.get_ticks()
                self.player = 'second'
                second_selff.super = 'small'
                second_size = 'small'
                second_selff.box_flag = True
        if self.time != 0:
            if pygame.time.get_ticks() - self.time >= 10000:
                if self.player == 'first':
                    if first_selff.a != 80:
                        first_selff.box_flag = False
                        first_size = 'big'
                        self.time = 0
                        first_selff.super = ''
                elif self.player == 'second':
                    if second_selff.a != 80:
                        second_selff.box_flag = False
                        second_size = 'big'
                        self.time = 0
                        second_selff.super = ''


class Bullet_Box(pygame.sprite.Sprite):
    image = load_image('bullet_box.jpg')
    image = pygame.transform.scale(image, (45, 45))

    def __init__(self):
        super(Bullet_Box, self).__init__(bullet_box_sprites)
        self.image = Bullet_Box.image
        flag = True
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -100, -100
        self.time = 0
        self.player = ''
        while flag:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            gg = f'{x} {y}'
            if gg not in spisok_wall:
                flag = False
                self.rect.x = x * 90 + 22
                self.rect.y = y * 90 + 22

    def update(self):
        global FIRST_TIME_RELOAD, SECOND_TIME_RELOAD, box_sound
        if pygame.sprite.spritecollideany(self, first_sprites):
            if not first_selff.box_flag:
                if SOUNDS:
                    box_sound.play()
                first_selff.super = 'bullet'
                self.rect.x, self.rect.y = -100, -100
                FIRST_TIME_RELOAD = 0
                self.time = pygame.time.get_ticks()
                self.player = 'first'
                first_selff.box_flag = True
        elif pygame.sprite.spritecollideany(self, second_sprites):
            if not second_selff.box_flag:
                if SOUNDS:
                    box_sound.play()
                second_selff.super = 'bullet'
                self.rect.x, self.rect.y = -100, -100
                SECOND_TIME_RELOAD = 0
                self.time = pygame.time.get_ticks()
                self.player = 'second'
                second_selff.box_flag = True
        if self.time != 0:
            if pygame.time.get_ticks() - self.time >= 10000:
                if self.player == 'first':
                    first_selff.box_flag = False
                    FIRST_TIME_RELOAD = 1500
                    self.time = 0
                    first_selff.super = ''
                elif self.player == 'second':
                    second_selff.box_flag = False
                    SECOND_TIME_RELOAD = 1500
                    self.time = 0
                    second_selff.super = ''


def bullet_move(self):
    if self.timer.get_ticks() - self.time >= 500:
        self.rect.x, self.rect.y = -100, -100
        self.flag = False


def bullet_change_im(self):
    if self.flag_im:
        im = load_image('boom.png')
        im = pygame.transform.scale(im, (50, 40))
        self.image = im
        self.time = self.timer.get_ticks()
        self.flag_im = False
        self.flag_move = False
        self.flag = True


class Bullet(pygame.sprite.Sprite):
    image = load_image('bullet.png', -1)
    image = pygame.transform.scale(image, (12, 30))

    def __init__(self, player, *group):
        super(Bullet, self).__init__(*group)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -100, -100
        self.direction = 'up'
        self.player = player
        self.speed = 6
        self.flag_move = False
        self.timer = pygame.time
        self.flag_im = True
        self.flag = False
        self.x1, self.y1 = 0, 0

    def update(self):
        if self.flag:
            bullet_move(self)
        if self.flag_move:
            global running, flag_finish
            if self.player == 'first':
                if pygame.sprite.spritecollideany(first_selff, right_st_wall) and self.direction == 'right':
                    bullet_change_im(self)
                    self.rect.move_ip(-15, -5)
                elif pygame.sprite.spritecollideany(first_selff, left_st_wall) and self.direction == 'left':
                    bullet_change_im(self)
                    self.rect.move_ip(0, -10)
                elif pygame.sprite.spritecollideany(first_selff, up_st_wall) and self.direction == 'down':
                    bullet_change_im(self)
                    self.rect.move_ip(-3, -25)
                elif pygame.sprite.spritecollideany(first_selff, down_st_wall) and self.direction == 'up':
                    bullet_change_im(self)
                    self.rect.move_ip(-5, 18)
            elif self.player == 'second':
                if pygame.sprite.spritecollideany(second_selff, left_st_wall) and self.direction == 'right':
                    bullet_change_im(self)
                    self.rect.move_ip(-20, -10)
                elif pygame.sprite.spritecollideany(second_selff, right_st_wall) and self.direction == 'left':
                    bullet_change_im(self)
                    self.rect.move_ip(-10, -10)
                elif pygame.sprite.spritecollideany(second_selff, up_st_wall) and self.direction == 'down':
                    bullet_change_im(self)
                    self.rect.move_ip(-15, 15)
                elif pygame.sprite.spritecollideany(second_selff, down_st_wall) and self.direction == 'up':
                    bullet_change_im(self)
                    self.rect.move_ip(-10, -10)
            if not pygame.sprite.spritecollideany(self, left_st_wall):
                if not pygame.sprite.spritecollideany(self, right_st_wall):
                    if not pygame.sprite.spritecollideany(self, up_st_wall):
                        if not pygame.sprite.spritecollideany(self, down_st_wall):
                            if not pygame.sprite.spritecollideany(self, first_sprites):
                                if not pygame.sprite.spritecollideany(self, second_sprites):
                                    if self.direction == 'up':
                                        self.rect.y -= self.speed
                                    elif self.direction == 'down':
                                        self.rect.y += self.speed
                                    elif self.direction == 'left':
                                        self.rect.x -= self.speed
                                    elif self.direction == 'right':
                                        self.rect.x += self.speed
                                else:
                                    if self.flag_im:
                                        if self.direction == 'up' or self.direction == 'down':
                                            cells = round(abs(self.y1 - self.rect.y) / 90)
                                        else:
                                            cells = round(abs(self.x1 - self.rect.x) / 90)
                                        hit_random = random.choice([0, 50, 50, 100])
                                        if hit_random == 100:
                                            if SOUNDS:
                                                popal = pygame.mixer.Sound('data/damage_100.mp3')
                                                popal.play()
                                                popal.set_volume(0.3)
                                            im = load_image('boom.png', -1)
                                            im = pygame.transform.scale(im, (85, 75))
                                            self.image = im
                                            self.time = self.timer.get_ticks()
                                            self.flag_im = False
                                            self.flag_move = False
                                            self.flag = True
                                        elif hit_random == 50:
                                            if SOUNDS:
                                                popal = pygame.mixer.Sound('data/damage_50.mp3')
                                                popal.play()
                                                popal.set_volume(0.3)
                                            im = load_image('boom.png', -1)
                                            im = pygame.transform.scale(im, (50, 40))
                                            self.image = im
                                            self.time = self.timer.get_ticks()
                                            self.flag_im = False
                                            self.flag_move = False
                                            self.flag = True
                                        else:
                                            if SOUNDS:
                                                ricochet_sound = pygame.mixer.Sound('data/ricochet.mp3')
                                                ricochet_sound.play()
                                                ricochet_sound.set_volume(0.3)
                                            if self.direction == 'up':
                                                self.rect.y += 6
                                                self.direction = 'down'
                                                self.image = pygame.transform.rotate(self.image, 180)
                                            elif self.direction == 'down':
                                                self.rect.y -= 6
                                                self.direction = 'up'
                                                self.image = pygame.transform.rotate(self.image, 180)
                                            elif self.direction == 'left':
                                                self.rect.x += 6
                                                self.direction = 'right'
                                                self.image = pygame.transform.rotate(self.image, 180)
                                            elif self.direction == 'right':
                                                self.rect.x -= 6
                                                self.direction = 'left'
                                                self.image = pygame.transform.rotate(self.image, 180)
                                            self.x1, self.y1 = self.rect.x, self.rect.y
                                        hit_hp = 100 - cells * 10
                                        hit_hp = hit_random * hit_hp // 100
                                        global SECOND_HP
                                        SECOND_HP -= hit_hp
                                        if SECOND_HP <= 0:
                                            SECOND_HP = 0
                                            if SOUNDS:
                                                boom_sound = pygame.mixer.Sound('data/boom_tank.mp3')
                                                boom_sound.play()
                                                boom_sound.set_volume(0.4)
                                            flag_finish = 'First player'
                                        if self.direction == 'left':
                                            self.rect.move_ip(-35, -30)
                                        elif self.direction == 'right':
                                            self.rect.move_ip(-30, -25)
                                        elif self.direction == 'up':
                                            self.rect.move_ip(-30, -30)
                                        elif self.direction == 'down':
                                            self.rect.move_ip(-30, 0)
                            else:
                                if self.flag_im:
                                    if self.direction == 'up' or self.direction == 'down':
                                        cells = round(abs(self.y1 - self.rect.y) / 90)
                                    else:
                                        cells = round(abs(self.x1 - self.rect.x) / 90)
                                    hit_random = random.choice([0, 50, 50, 100])
                                    popal = pygame.mixer.Sound('data/damage_100.mp3')
                                    popal.set_volume(0.3)
                                    if hit_random == 100:
                                        if SOUNDS:
                                            popal.play()
                                        im = load_image('boom.png', -1)
                                        im = pygame.transform.scale(im, (85, 75))
                                        self.image = im
                                        self.time = self.timer.get_ticks()
                                        self.flag_im = False
                                        self.flag_move = False
                                        self.flag = True
                                    elif hit_random == 50:
                                        if SOUNDS:
                                            popal.play()
                                        im = load_image('boom.png', -1)
                                        im = pygame.transform.scale(im, (50, 40))
                                        self.image = im
                                        self.time = self.timer.get_ticks()
                                        self.flag_im = False
                                        self.flag_move = False
                                        self.flag = True
                                    else:
                                        if SOUNDS:
                                            ricochet_sound = pygame.mixer.Sound('data/ricochet.mp3')
                                            ricochet_sound.play()
                                            ricochet_sound.set_volume(0.3)
                                        if self.direction == 'up':
                                            self.rect.y += 6
                                            self.direction = 'down'
                                            self.image = pygame.transform.rotate(self.image, 180)
                                        elif self.direction == 'down':
                                            self.rect.y -= 6
                                            self.direction = 'up'
                                            self.image = pygame.transform.rotate(self.image, 180)
                                        elif self.direction == 'left':
                                            self.rect.x += 6
                                            self.direction = 'right'
                                            self.image = pygame.transform.rotate(self.image, 180)
                                        elif self.direction == 'right':
                                            self.rect.x -= 6
                                            self.direction = 'left'
                                            self.image = pygame.transform.rotate(self.image, 180)
                                        self.x1, self.y1 = self.rect.x, self.rect.y
                                    hit_hp = 100 - cells * 10
                                    hit_hp = hit_random * hit_hp // 100
                                    global FIRST_HP
                                    FIRST_HP -= hit_hp
                                    if FIRST_HP <= 0:
                                        FIRST_HP = 0
                                        if SOUNDS:
                                            boom_sound = pygame.mixer.Sound('data/boom_tank.mp3')
                                            boom_sound.play()
                                            boom_sound.set_volume(0.4)
                                        flag_finish = 'Second player'
                                    if self.direction == 'left':
                                        self.rect.move_ip(-35, -30)
                                    elif self.direction == 'right':
                                        self.rect.move_ip(-30, -25)
                                    elif self.direction == 'up':
                                        self.rect.move_ip(-30, -30)
                                    elif self.direction == 'down':
                                        self.rect.move_ip(-30, 0)
                        else:
                            bullet_change_im(self)
                            self.rect.move_ip(-10, -10)
                    else:
                        bullet_change_im(self)
                        self.rect.move_ip(-15, 15)
                else:
                    bullet_change_im(self)
                    self.rect.move_ip(-10, -10)
            else:
                bullet_change_im(self)
                self.rect.move_ip(-20, -10)
        if self.rect.x > 900:
            self.flag_move = False
        elif self.rect.x < -35:
            self.flag_move = False
        elif self.rect.y > 900:
            self.flag_move = False
        elif self.rect.y < -40:
            self.flag_move = False


bullet_sprites = pygame.sprite.Group()
bullet = Bullet(bullet_sprites)


class First_tank(pygame.sprite.Sprite):
    image = load_image(f'{FIRST_PLAYER}_tank.png')
    image = pygame.transform.scale(image, (80, 80))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = First_tank.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 810
        self.direction = 'up'
        self.timer = pygame.time
        self.fire_time = 0
        self.drive_flag = False
        self.box_flag = False
        self.a = 80
        self.time_scale = 0
        self.flag = True
        self.super = ''
        self.speed = FIRST_SPEED
        global first_selff
        first_selff = self

    def update(self, action):
        global first_size, flag_finish, FIRST_SPEED, spisok_walls, first_tp_flag
        if first_size == 'big' and pygame.time.get_ticks() - self.time_scale >= 100:
            if FIRST_SPEED != 0:
                self.speed = FIRST_SPEED
            FIRST_SPEED = 0
            self.time_scale = pygame.time.get_ticks()
            im = load_image(f'{FIRST_PLAYER}_tank.png')
            self.a += 5
            im = pygame.transform.scale(im, (self.a, self.a))
            self.image = im
            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = x // 90 * 90 + 10
            self.rect.y = y // 90 * 90 + 5
            if self.direction == 'down':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'left':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.direction == 'right':
                self.image = pygame.transform.rotate(self.image, 270)
            if self.a == 80:
                first_size = ''
                self.time_scale = 0
                FIRST_SPEED = self.speed
                self.flag = True
                self.box_flag = False
        elif first_size == 'small' and pygame.time.get_ticks() - self.time_scale >= 100:
            if self.a != 50:
                if FIRST_SPEED != 0:
                    self.speed = FIRST_SPEED
                FIRST_SPEED = 0
                self.time_scale = pygame.time.get_ticks()
                im = load_image(f'{FIRST_PLAYER}_tank.png')
                self.a -= 5
                im = pygame.transform.scale(im, (self.a, self.a))
                self.image = im
                x, y = self.rect.x, self.rect.y
                self.rect = self.image.get_rect()
                self.rect.x = x // 90 * 90 + 15
                self.rect.y = y // 90 * 90 + 15
                if self.direction == 'down':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'left':
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.direction == 'right':
                    self.image = pygame.transform.rotate(self.image, 270)
            if self.a == 50:
                if first_tp_flag:
                    first_portal_self.rect.x, first_portal_self.rect.y = -100, -100
                    while self.flag:
                        x = random.randint(0, 9)
                        y = random.randint(0, 9)
                        gg = f'{x} {y}'
                        if gg not in spisok_wall:
                            self.flag = False
                            self.rect.x = x * 90 + 22
                            self.rect.y = y * 90 + 22
                            if self.super != 'small':
                                first_size = 'big'
                            self.time_scale = 0
                            first_tp_flag = False
                else:
                    first_size = ''
                    self.time_scale = 0
                    FIRST_SPEED = self.speed
        else:
            if flag_finish:
                image = load_image(f'{FIRST_PLAYER}_tank.png')
                image = pygame.transform.scale(image, (80, 80))
                self.image = image
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = 0, 810
                self.direction = 'up'
                self.timer = pygame.time
                self.fire_time = 0
                self.drive_flag = False
            if action == 'drive':
                if not self.drive_flag:
                    global first_drive_sound
                    if SOUNDS:
                        first_drive_sound.play(-1)
                        first_drive_sound.set_volume(0.3)
                    self.drive_flag = True
            self.speedx = 0
            self.speedy = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_a]:
                if not pygame.sprite.spritecollideany(self, left_st_wall):
                    self.speedx = -FIRST_SPEED
                    if self.direction == 'right':
                        self.image = pygame.transform.rotate(self.image, 180)
                    elif self.direction == 'up':
                        self.image = pygame.transform.rotate(self.image, 90)
                    elif self.direction == 'down':
                        self.image = pygame.transform.rotate(self.image, 270)
                    self.direction = 'left'
            if keystate[pygame.K_d]:
                if not pygame.sprite.spritecollideany(self, right_st_wall):
                    self.speedx = FIRST_SPEED
                    if self.direction == 'left':
                        self.image = pygame.transform.rotate(self.image, 180)
                    elif self.direction == 'up':
                        self.image = pygame.transform.rotate(self.image, 270)
                    elif self.direction == 'down':
                        self.image = pygame.transform.rotate(self.image, 90)
                    self.direction = 'right'
            if keystate[pygame.K_w]:
                if not pygame.sprite.spritecollideany(self, down_st_wall):
                    self.speedy = -FIRST_SPEED
                    if self.direction == 'down':
                        self.image = pygame.transform.rotate(self.image, 180)
                    elif self.direction == 'left':
                        self.image = pygame.transform.rotate(self.image, 270)
                    elif self.direction == 'right':
                        self.image = pygame.transform.rotate(self.image, 90)
                    self.direction = 'up'
            if keystate[pygame.K_s]:
                if not pygame.sprite.spritecollideany(self, up_st_wall):
                    self.speedy = FIRST_SPEED
                    if self.direction == 'up':
                        self.image = pygame.transform.rotate(self.image, 180)
                    elif self.direction == 'left':
                        self.image = pygame.transform.rotate(self.image, 90)
                    elif self.direction == 'right':
                        self.image = pygame.transform.rotate(self.image, 270)
                    self.direction = 'down'
            if action == 'fire':
                if self.timer.get_ticks() - self.fire_time >= FIRST_TIME_RELOAD:
                    self.fire_time = self.timer.get_ticks()
                    bullet = Bullet('first', bullet_sprites)
                    all_sprites.add(bullet_sprites)
                    if SOUNDS:
                        fire_sound = pygame.mixer.Sound('data/fire_sound.mp3')
                        fire_sound.play()
                        fire_sound.set_volume(0.4)
                    if self.direction == 'left':
                        if bullet.direction == 'right':
                            bullet.image = pygame.transform.rotate(bullet.image, 180)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'up':
                            bullet.image = pygame.transform.rotate(bullet.image, 90)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'down':
                            bullet.image = pygame.transform.rotate(bullet.image, 270)
                            bullet.rect = bullet.image.get_rect()
                        bullet.direction = 'left'
                        bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 71
                        bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 5
                        bullet.x1 = self.rect.x + self.image.get_width() // 2 - 70
                        bullet.y1 = self.rect.y + self.image.get_height() // 2 - 5
                    if self.direction == 'right':
                        if bullet.direction == 'left':
                            bullet.image = pygame.transform.rotate(bullet.image, 180)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'up':
                            bullet.image = pygame.transform.rotate(bullet.image, 270)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'down':
                            bullet.image = pygame.transform.rotate(bullet.image, 90)
                            bullet.rect = bullet.image.get_rect()
                        bullet.direction = 'right'
                        bullet.rect.x = self.rect.x + self.image.get_width() // 2 + 45
                        bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 7
                        bullet.x1 = self.rect.x + self.image.get_width() // 2 + 45
                        bullet.y1 = self.rect.y + self.image.get_height() // 2 - 7
                    if self.direction == 'up':
                        if bullet.direction == 'down':
                            bullet.image = pygame.transform.rotate(bullet.image, 180)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'left':
                            bullet.image = pygame.transform.rotate(bullet.image, 270)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'right':
                            bullet.image = pygame.transform.rotate(bullet.image, 90)
                            bullet.rect = bullet.image.get_rect()
                        bullet.direction = 'up'
                        bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 6
                        bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 78
                        bullet.x1 = self.rect.x + self.image.get_width() // 2 - 6
                        bullet.y1 = self.rect.y + self.image.get_height() // 2 - 78
                    if self.direction == 'down':
                        if bullet.direction == 'up':
                            bullet.image = pygame.transform.rotate(bullet.image, 180)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'left':
                            bullet.image = pygame.transform.rotate(bullet.image, 90)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'right':
                            bullet.image = pygame.transform.rotate(bullet.image, 270)
                            bullet.rect = bullet.image.get_rect()
                        bullet.direction = 'down'
                        bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 7
                        bullet.rect.y = self.rect.y + self.image.get_height() // 2 + 45
                        bullet.x1 = self.rect.x + self.image.get_width() // 2 - 7
                        bullet.y1 = self.rect.y + self.image.get_height() // 2 + 45
                    bullet.flag_move = True
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if FIRST_SPEED == 3:
                if pygame.sprite.spritecollideany(self, left_st_wall):
                    self.rect.x += 3
                if pygame.sprite.spritecollideany(self, right_st_wall):
                    self.rect.x -= 3
                if pygame.sprite.spritecollideany(self, down_st_wall):
                    self.rect.y += 3
                if pygame.sprite.spritecollideany(self, up_st_wall):
                    self.rect.y -= 3
            if self.rect.right > 900:
                self.rect.right = 900
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > 900:
                self.rect.bottom = 900


class Second_tank(pygame.sprite.Sprite):
    image = load_image(f'{SECOND_PLAYER}_tank.png')
    image = pygame.transform.scale(image, (80, 80))
    image = pygame.transform.rotate(image, 180)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Second_tank.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 810, 0
        self.direction = 'down'
        self.timer = pygame.time
        self.fire_time = 0
        self.drive_flag = False
        self.box_flag = False
        self.a = 80
        self.time_scale = 0
        self.flag = True
        self.super = ''
        self.speed = FIRST_SPEED
        global second_selff
        second_selff = self

    def update(self, action):
        global second_size, flag_finish, SECOND_SPEED, second_tp_flag, second_portal_self
        if second_size == 'big' and pygame.time.get_ticks() - self.time_scale >= 100:
            if SECOND_SPEED != 0:
                self.speed = SECOND_SPEED
            SECOND_SPEED = 0
            self.time_scale = pygame.time.get_ticks()
            im = load_image(f'{SECOND_PLAYER}_tank.png')
            self.a += 5
            im = pygame.transform.scale(im, (self.a, self.a))
            self.image = im
            x, y = self.rect.x, self.rect.y
            self.rect = self.image.get_rect()
            self.rect.x = x // 90 * 90 + 10
            self.rect.y = y // 90 * 90 + 5
            if self.direction == 'down':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'left':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.direction == 'right':
                self.image = pygame.transform.rotate(self.image, 270)
            if self.a == 80:
                second_size = ''
                self.time_scale = 0
                SECOND_SPEED = self.speed
                self.flag = True
        elif second_size == 'small' and pygame.time.get_ticks() - self.time_scale >= 100:
            if self.a != 50:
                if SECOND_SPEED != 0:
                    self.speed = SECOND_SPEED
                SECOND_SPEED = 0
                self.time_scale = pygame.time.get_ticks()
                im = load_image(f'{SECOND_PLAYER}_tank.png')
                self.a -= 5
                im = pygame.transform.scale(im, (self.a, self.a))
                self.image = im
                x, y = self.rect.x, self.rect.y
                self.rect = self.image.get_rect()
                self.rect.x = x // 90 * 90 + 15
                self.rect.y = y // 90 * 90 + 15
                if self.direction == 'down':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'left':
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.direction == 'right':
                    self.image = pygame.transform.rotate(self.image, 270)
            if self.a == 50:
                if second_tp_flag:
                    second_portal_self.rect.x, second_portal_self.rect.y = -100, -100
                    while self.flag:
                        x = random.randint(0, 9)
                        y = random.randint(0, 9)
                        gg = f'{x} {y}'
                        if gg not in spisok_wall:
                            self.flag = False
                            self.rect.x = x * 90 + 22
                            self.rect.y = y * 90 + 22
                            if self.super != 'small':
                                second_size = 'big'
                            self.time_scale = 0
                            second_tp_flag = False
                else:
                    second_size = ''
                    self.time_scale = 0
                    SECOND_SPEED = self.speed
        else:
            if flag_finish:
                image = load_image(f'{SECOND_PLAYER}_tank.png')
                image = pygame.transform.scale(image, (80, 80))
                image = pygame.transform.rotate(image, 180)
                self.image = image
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.y = 810, 0
                self.direction = 'down'
                self.timer = pygame.time
                self.fire_time = 0
                self.drive_flag = False
            if action == 'drive':
                if not self.drive_flag:
                    global second_drive_sound
                    if SOUNDS:
                        second_drive_sound.play(-1)
                        second_drive_sound.set_volume(0.3)
                    self.drive_flag = True
            self.speedx = 0
            self.speedy = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                if not pygame.sprite.spritecollideany(self, left_st_wall):
                    self.speedx = -SECOND_SPEED
                    if self.direction == 'right':
                        self.image = pygame.transform.rotate(self.image, 180)
                    elif self.direction == 'up':
                        self.image = pygame.transform.rotate(self.image, 90)
                    elif self.direction == 'down':
                        self.image = pygame.transform.rotate(self.image, 270)
                    self.direction = 'left'
            if keystate[pygame.K_RIGHT]:
                if not pygame.sprite.spritecollideany(self, right_st_wall):
                    self.speedx = SECOND_SPEED
                    if self.direction == 'left':
                        self.image = pygame.transform.rotate(self.image, 180)
                    elif self.direction == 'up':
                        self.image = pygame.transform.rotate(self.image, 270)
                    elif self.direction == 'down':
                        self.image = pygame.transform.rotate(self.image, 90)
                    self.direction = 'right'
            if keystate[pygame.K_UP]:
                if not pygame.sprite.spritecollideany(self, down_st_wall):
                    self.speedy = -SECOND_SPEED
                    if self.direction == 'down':
                        self.image = pygame.transform.rotate(self.image, 180)
                    elif self.direction == 'left':
                        self.image = pygame.transform.rotate(self.image, 270)
                    elif self.direction == 'right':
                        self.image = pygame.transform.rotate(self.image, 90)
                    self.direction = 'up'
            if keystate[pygame.K_DOWN]:
                if not pygame.sprite.spritecollideany(self, up_st_wall):
                    self.speedy = SECOND_SPEED
                    if self.direction == 'up':
                        self.image = pygame.transform.rotate(self.image, 180)
                    elif self.direction == 'left':
                        self.image = pygame.transform.rotate(self.image, 90)
                    elif self.direction == 'right':
                        self.image = pygame.transform.rotate(self.image, 270)
                    self.direction = 'down'
            if action == 'fire':
                if self.timer.get_ticks() - self.fire_time >= SECOND_TIME_RELOAD:
                    self.fire_time = self.timer.get_ticks()
                    bullet = Bullet('second', bullet_sprites)
                    all_sprites.add(bullet_sprites)
                    if SOUNDS:
                        fire_sound = pygame.mixer.Sound('data/fire_sound.mp3')
                        fire_sound.play()
                        fire_sound.set_volume(0.4)
                    if self.direction == 'left':
                        if bullet.direction == 'right':
                            bullet.image = pygame.transform.rotate(bullet.image, 180)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'up':
                            bullet.image = pygame.transform.rotate(bullet.image, 90)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'down':
                            bullet.image = pygame.transform.rotate(bullet.image, 270)
                            bullet.rect = bullet.image.get_rect()
                        bullet.direction = 'left'
                        bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 71
                        bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 5
                        bullet.x1 = self.rect.x + self.image.get_width() // 2 - 67
                        bullet.y1 = self.rect.y + self.image.get_height() // 2 - 5
                    if self.direction == 'right':
                        if bullet.direction == 'left':
                            bullet.image = pygame.transform.rotate(bullet.image, 180)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'up':
                            bullet.image = pygame.transform.rotate(bullet.image, 270)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'down':
                            bullet.image = pygame.transform.rotate(bullet.image, 90)
                            bullet.rect = bullet.image.get_rect()
                        bullet.direction = 'right'
                        bullet.rect.x = self.rect.x + self.image.get_width() // 2 + 45
                        bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 7
                        bullet.x1 = self.rect.x + self.image.get_width() // 2 + 45
                        bullet.y1 = self.rect.y + self.image.get_height() // 2 - 7
                    if self.direction == 'up':
                        if bullet.direction == 'down':
                            bullet.image = pygame.transform.rotate(bullet.image, 180)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'left':
                            bullet.image = pygame.transform.rotate(bullet.image, 270)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'right':
                            bullet.image = pygame.transform.rotate(bullet.image, 90)
                            bullet.rect = bullet.image.get_rect()
                        bullet.direction = 'up'
                        bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 6
                        bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 78
                        bullet.x1 = self.rect.x + self.image.get_width() // 2 - 6
                        bullet.y1 = self.rect.y + self.image.get_height() // 2 - 78
                    if self.direction == 'down':
                        if bullet.direction == 'up':
                            bullet.image = pygame.transform.rotate(bullet.image, 180)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'left':
                            bullet.image = pygame.transform.rotate(bullet.image, 90)
                            bullet.rect = bullet.image.get_rect()
                        elif bullet.direction == 'right':
                            bullet.image = pygame.transform.rotate(bullet.image, 270)
                            bullet.rect = bullet.image.get_rect()
                        bullet.direction = 'down'
                        bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 7
                        bullet.rect.y = self.rect.y + self.image.get_height() // 2 + 45
                        bullet.x1 = self.rect.x + self.image.get_width() // 2 - 7
                        bullet.y1 = self.rect.y + self.image.get_height() // 2 + 45
                    bullet.flag_move = True
            self.rect.y += self.speedy
            self.rect.x += self.speedx
            if SECOND_SPEED == 3:
                if pygame.sprite.spritecollideany(self, left_st_wall):
                    self.rect.x += 3
                if pygame.sprite.spritecollideany(self, right_st_wall):
                    self.rect.x -= 3
                if pygame.sprite.spritecollideany(self, down_st_wall):
                    self.rect.y += 3
                if pygame.sprite.spritecollideany(self, up_st_wall):
                    self.rect.y -= 3
            if self.rect.right > 900:
                self.rect.right = 900
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > 900:
                self.rect.bottom = 900


def fight_screen_update():
    level_map = load_level(MAP)
    generate_level(level_map)
    spisok_wall.append('2 0')
    spisok_wall.append('7 0')


def main():
    global first_sprites, second_sprites, flag_pause, FIRST_SPEED, SECOND_SPEED, med_box_sprites, bullet_sprites
    global first_drive_sound, second_drive_sound, first_selff, second_selff, fast_box_sprites, bullet_box_sprites
    global running, flag_finish, FIRST_HP, SECOND_HP, first_size, second_size, small_box_sprites, portal_sprites
    global up_st_wall, down_st_wall, left_st_wall, right_st_wall, FIRST_TIME_RELOAD, SECOND_TIME_RELOAD
    first_sprites = pygame.sprite.Group()
    first_tank = First_tank(first_sprites)
    im = load_image(f'{FIRST_PLAYER}_tank.png')
    im = pygame.transform.scale(im, (80, 80))
    first_tank.image = im
    second_sprites = pygame.sprite.Group()
    second_tank = Second_tank(second_sprites)
    im = load_image(f'{SECOND_PLAYER}_tank.png')
    im = pygame.transform.scale(im, (80, 80))
    im = pygame.transform.rotate(im, 180)
    second_tank.image = im
    fight_screen_update()
    time_box = pygame.time.get_ticks()
    time_portal = pygame.time.get_ticks()

    all_sprites.add(sprite_group)
    all_sprites.add(first_sprites)
    all_sprites.add(second_sprites)
    all_sprites.add(up_st_wall)
    all_sprites.add(down_st_wall)
    all_sprites.add(right_st_wall)
    all_sprites.add(left_st_wall)

    first_pushed_buttons = 0
    second_pushed_buttons = 0
    running = True
    while running:
        pygame.mouse.set_visible(False)
        clock.tick(FPS)
        if pygame.time.get_ticks() - time_portal >= 20000:
            Portal()
            all_sprites.add(portal_sprites)
            time_portal = pygame.time.get_ticks()
        if pygame.time.get_ticks() - time_box >= 15000:
            box = random.choice(['Fast_Box', 'Med_Box', 'Bullet_Box', 'Small_Box'])
            if box == 'Med_Box':
                Med_Box()
                all_sprites.add(med_box_sprites)
                time_box = pygame.time.get_ticks()
            elif box == 'Bullet_Box':
                Bullet_Box()
                all_sprites.add(bullet_box_sprites)
                time_box = pygame.time.get_ticks()
            elif box == 'Small_Box':
                Small_Box()
                all_sprites.add(small_box_sprites)
                time_box = pygame.time.get_ticks()
            else:
                Fast_Box()
                all_sprites.add(fast_box_sprites)
                time_box = pygame.time.get_ticks()
        if flag_finish:
            first_drive_sound.stop()
            second_drive_sound.stop()
            finish_screen(flag_finish)
            flag_finish = ''
            FIRST_TIME_RELOAD = 1500
            SECOND_TIME_RELOAD = 1500
            FIRST_SPEED = 1
            SECOND_SPEED = 1
            FIRST_HP = 100
            SECOND_HP = 100
            first_selff.a = 80
            second_selff.a = 80
            first_size = ''
            second_size = ''
            first_selff.time_scale = 0
            second_selff.time_scale = 0
            up_st_wall = pygame.sprite.Group()
            down_st_wall = pygame.sprite.Group()
            left_st_wall = pygame.sprite.Group()
            right_st_wall = pygame.sprite.Group()
            med_box_sprites = pygame.sprite.Group()
            fast_box_sprites = pygame.sprite.Group()
            small_box_sprites = pygame.sprite.Group()
            bullet_box_sprites = pygame.sprite.Group()
            portal_sprites = pygame.sprite.Group()
            bullet_sprites = pygame.sprite.Group()
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(True)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    flag_pause = not flag_pause
                    color = pygame.Surface((900, 900))
                    color.set_alpha(200)
                    color.fill((0, 0, 0))
                    screen.blit(color, (0, 0))
                if not flag_pause:
                    if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a or event.key == pygame.K_d:
                        first_sprites.update('drive')
                        first_selff.drive_flag = True
                        first_pushed_buttons += 1
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        second_sprites.update('drive')
                        second_selff.drive_flag = True
                        second_pushed_buttons += 1
                    if event.key == pygame.K_LSHIFT:
                        first_sprites.update('fire')
                    if event.key == pygame.K_RSHIFT:
                        second_sprites.update('fire')
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a or event.key == pygame.K_d:
                    first_pushed_buttons -= 1
                    if first_pushed_buttons == 0:
                        first_drive_sound.stop()
                        first_selff.drive_flag = False
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    second_pushed_buttons -= 1
                    if second_pushed_buttons == 0:
                        second_drive_sound.stop()
                        second_selff.drive_flag = False
        if not flag_pause:
            bullet_sprites.update()
            med_box_sprites.update()
            fast_box_sprites.update()
            bullet_box_sprites.update()
            small_box_sprites.update()
            portal_sprites.update()
            first_sprites.update(None)
            second_sprites.update(None)
            all_sprites.draw(screen)
            first_sprites.draw(screen)
            second_sprites.draw(screen)
            bullet_sprites.draw(screen)
            print_health()
        pygame.display.flip()
    terminate()


start_screen()
