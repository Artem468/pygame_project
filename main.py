import pygame
import os
import sys
import random

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
# border_sprite = pygame.sprite.Group()


flag_finish = ''
flag_tanks = False
FPS = 60
FIRST_TIME_RELOAD = 1500
SECOND_TIME_RELOAD = 1500
FIRST_SPEED = 1
SECOND_SPEED = 1
FIRST_PLAYER = 'blue'
SECOND_PLAYER = 'red'
FIRST_HP = 100
SECOND_HP = 100

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
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
tile_width = tile_height = 90


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
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# class Border(pygame.sprite.Sprite):
#     def __init__(self, x1, y1):
#         super().__init__()
#         self.add(border_sprite)
#         self.image = pygame.Surface([90, 90])
#         self.image.fill((128, 128, 128))
#         self.rect = pygame.Rect(x1 * 90, y1 * 90, 90, 90)


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
                # Border(x, y)
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
        self.speed = 15

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
        self.speed = 15

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


def start_screen():
    start_screen_update()
    tanks_preview_update()
    start_screen_sound = pygame.mixer.Sound('data/sound_lobby.mp3')
    start_screen_sound.play(-1)
    start_screen_sound.set_volume(0.5)
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 365 and event.pos[0] <= 530:
                    if event.pos[1] >= 300 and event.pos[1] <= 350:
                        tank1.rect.x = -200
                        tank2.rect.x = -200
                        start_screen_sound.stop()
                        main()
                        start_screen_update()
                        tanks_preview_update()
                        start_screen_sound = pygame.mixer.Sound('data/sound_lobby.mp3')
                        start_screen_sound.play(-1)
                        start_screen_sound.set_volume(0.5)
                if event.pos[0] >= 180 and event.pos[0] <= 440:
                    if event.pos[1] >= 400 and event.pos[1] <= 435:
                        select_skin('1st player')
                        start_screen_update()
                        tanks_preview_update()
                if event.pos[0] >= 470 and event.pos[0] <= 730:
                    if event.pos[1] >= 400 and event.pos[1] <= 435:
                        select_skin('2nd player')
                        start_screen_update()
                        tanks_preview_update()
        start_screen_update()
        tank1.update()
        tank2.update()
        first_preview_sprites.draw(screen)
        second_preview_sprites.draw(screen)
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


med_box_sprites = pygame.sprite.Group()
fast_box_sprites = pygame.sprite.Group()
small_box_sprites = pygame.sprite.Group()
bullet_box_sprites = pygame.sprite.Group()


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
        global FIRST_HP, SECOND_HP
        if pygame.sprite.spritecollideany(self, first_sprites):
            self.rect.x, self.rect.y = -100, -100
            FIRST_HP = 100
        elif pygame.sprite.spritecollideany(self, second_sprites):
            self.rect.x, self.rect.y = -100, -100
            SECOND_HP = 100


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
        global FIRST_SPEED, SECOND_SPEED
        if pygame.sprite.spritecollideany(self, first_sprites):
            self.rect.x, self.rect.y = -100, -100
            FIRST_SPEED = 3
            self.time = pygame.time.get_ticks()
            self.player = 'first'
        elif pygame.sprite.spritecollideany(self, second_sprites):
            self.rect.x, self.rect.y = -100, -100
            SECOND_SPEED = 3
            self.time = pygame.time.get_ticks()
            self.player = 'second'
        if self.time != 0:
            if pygame.time.get_ticks() - self.time >= 10000:
                if self.player == 'first':
                    FIRST_SPEED = 1
                elif self.player == 'second':
                    SECOND_SPEED = 1


class Small_Box(pygame.sprite.Sprite):
    image = load_image('small_box.jpg')
    image = pygame.transform.scale(image, (45, 45))

    def __init__(self):
        super(Small_Box, self).__init__(small_box_sprites)
        self.image = Small_Box.image
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
        global FIRST_TIME_RELOAD, SECOND_TIME_RELOAD
        if pygame.sprite.spritecollideany(self, first_sprites):
            self.rect.x, self.rect.y = -100, -100
            FIRST_TIME_RELOAD = 0
            self.time = pygame.time.get_ticks()
            self.player = 'first'
        elif pygame.sprite.spritecollideany(self, second_sprites):
            self.rect.x, self.rect.y = -100, -100
            SECOND_TIME_RELOAD = 0
            self.time = pygame.time.get_ticks()
            self.player = 'second'
        if self.time != 0:
            if pygame.time.get_ticks() - self.time >= 10000:
                if self.player == 'first':
                    FIRST_TIME_RELOAD = 1500
                elif self.player == 'second':
                    SECOND_TIME_RELOAD = 1500


def bullet_move(self):
    if self.timer.get_ticks() - self.time >= 500:
        self.rect.x, self.rect.y = -100, -100
        self.flag = False


class Bullet(pygame.sprite.Sprite):
    image = load_image('bullet.png')
    image = pygame.transform.scale(image, (15, 35))

    def __init__(self, *group):
        super(Bullet, self).__init__(*group)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -100, -100
        self.direction = 'up'
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
                                            im = load_image('boom.png', -1)
                                            im = pygame.transform.scale(im, (85, 75))
                                            self.image = im
                                            self.time = self.timer.get_ticks()
                                            self.flag_im = False
                                            self.flag_move = False
                                            self.flag = True
                                        elif hit_random == 50:
                                            im = load_image('boom.png', -1)
                                            im = pygame.transform.scale(im, (50, 40))
                                            self.image = im
                                            self.time = self.timer.get_ticks()
                                            self.flag_im = False
                                            self.flag_move = False
                                            self.flag = True
                                        else:
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
                                        hit_hp = 100 - cells * 10
                                        hit_hp = hit_random * hit_hp // 100
                                        global SECOND_HP
                                        SECOND_HP -= hit_hp
                                        if SECOND_HP <= 0:
                                            SECOND_HP = 0
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
                                    if hit_random == 100:
                                        im = load_image('boom.png', -1)
                                        im = pygame.transform.scale(im, (85, 75))
                                        self.image = im
                                        self.time = self.timer.get_ticks()
                                        self.flag_im = False
                                        self.flag_move = False
                                        self.flag = True
                                    elif hit_random == 50:
                                        im = load_image('boom.png', -1)
                                        im = pygame.transform.scale(im, (50, 40))
                                        self.image = im
                                        self.time = self.timer.get_ticks()
                                        self.flag_im = False
                                        self.flag_move = False
                                        self.flag = True
                                    else:
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
                                    hit_hp = 100 - cells * 10
                                    hit_hp = hit_random * hit_hp // 100
                                    global FIRST_HP
                                    FIRST_HP -= hit_hp
                                    if FIRST_HP <= 0:
                                        FIRST_HP = 0
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
                            if self.flag_im:
                                im = load_image('boom.png')
                                im = pygame.transform.scale(im, (50, 40))
                                self.image = im
                                self.time = self.timer.get_ticks()
                                self.flag_im = False
                                self.flag_move = False
                                self.flag = True
                                self.rect.move_ip(-10, -10)
                    else:
                        if self.flag_im:
                            im = load_image('boom.png')
                            im = pygame.transform.scale(im, (50, 40))
                            self.image = im
                            self.time = self.timer.get_ticks()
                            self.flag_im = False
                            self.flag_move = False
                            self.flag = True
                            self.rect.move_ip(-15, 15)
                else:
                    if self.flag_im:
                        im = load_image('boom.png')
                        im = pygame.transform.scale(im, (50, 40))
                        self.image = im
                        self.time = self.timer.get_ticks()
                        self.flag_im = False
                        self.flag_move = False
                        self.flag = True
                        self.rect.move_ip(-10, -10)
            else:
                if self.flag_im:
                    im = load_image('boom.png')
                    im = pygame.transform.scale(im, (50, 40))
                    self.image = im
                    self.time = self.timer.get_ticks()
                    self.flag_im = False
                    self.flag_move = False
                    self.flag = True
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
        global first_selff
        first_selff = self

    def update(self, action):
        if action == 'drive':
            if not self.drive_flag:
                global first_drive_sound

                first_drive_sound.play()
                first_drive_sound.set_volume(0.3)
                drive_flag = True
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
                bullet = Bullet(bullet_sprites)
                all_sprites.add(bullet_sprites)
                fire_sound = pygame.mixer.Sound('data/fire_sound.mp3')
                fire_sound.play()
                fire_sound.set_volume(0.4)
                if self.direction == 'left':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 67
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 5
                    bullet.x1 = self.rect.x + self.image.get_width() // 2 - 67
                    bullet.y1 = self.rect.y + self.image.get_height() // 2 - 5
                    if bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    elif bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    bullet.direction = 'left'
                if self.direction == 'right':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 + 45
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 7
                    bullet.x1 = self.rect.x + self.image.get_width() // 2 + 45
                    bullet.y1 = self.rect.y + self.image.get_height() // 2 - 7
                    if bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    elif bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    bullet.direction = 'right'
                if self.direction == 'up':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 6
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 78
                    bullet.x1 = self.rect.x + self.image.get_width() // 2 - 6
                    bullet.y1 = self.rect.y + self.image.get_height() // 2 - 78
                    if bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    elif bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    bullet.direction = 'up'
                if self.direction == 'down':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 7
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 + 45
                    bullet.x1 = self.rect.x + self.image.get_width() // 2 - 7
                    bullet.y1 = self.rect.y + self.image.get_height() // 2 + 45
                    if bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    elif bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    bullet.direction = 'down'
                bullet.flag_move = True
        self.rect.y += self.speedy
        self.rect.x += self.speedx
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
        global second_selff
        second_selff = self

    def update(self, action):
        if action == 'drive':
            if not self.drive_flag:
                global second_drive_sound
                second_drive_sound.play()
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
                bullet = Bullet(bullet_sprites)
                all_sprites.add(bullet_sprites)
                fire_sound = pygame.mixer.Sound('data/fire_sound.mp3')
                fire_sound.play()
                fire_sound.set_volume(0.4)
                if self.direction == 'left':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 67
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 5
                    bullet.x1 = self.rect.x + self.image.get_width() // 2 - 67
                    bullet.y1 = self.rect.y + self.image.get_height() // 2 - 5
                    if bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    elif bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    bullet.direction = 'left'
                if self.direction == 'right':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 + 45
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 7
                    bullet.x1 = self.rect.x + self.image.get_width() // 2 + 45
                    bullet.y1 = self.rect.y + self.image.get_height() // 2 - 7
                    if bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    elif bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    bullet.direction = 'right'
                if self.direction == 'up':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 6
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 78
                    bullet.x1 = self.rect.x + self.image.get_width() // 2 - 6
                    bullet.y1 = self.rect.y + self.image.get_height() // 2 - 78
                    if bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    elif bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    bullet.direction = 'up'
                if self.direction == 'down':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 7
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 + 45
                    bullet.x1 = self.rect.x + self.image.get_width() // 2 - 7
                    bullet.y1 = self.rect.y + self.image.get_height() // 2 + 45
                    if bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    elif bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    bullet.direction = 'down'
                bullet.flag_move = True
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right > 900:
            self.rect.right = 900
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 900:
            self.rect.bottom = 900


def fight_screen_update():
    level_map = load_level("map.map")
    generate_level(level_map)


def main():
    global first_sprites, second_sprites
    global first_drive_sound, second_drive_sound
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
    time = pygame.time.get_ticks()

    all_sprites.add(sprite_group)
    all_sprites.add(first_sprites)
    all_sprites.add(second_sprites)
    all_sprites.add(up_st_wall)
    all_sprites.add(down_st_wall)
    all_sprites.add(right_st_wall)
    all_sprites.add(left_st_wall)

    first_pushed_buttons = 0
    second_pushed_buttons = 0
    global running, flag_finish, FIRST_HP, SECOND_HP
    running = True
    while running:
        clock.tick(FPS)
        if pygame.time.get_ticks() - time >= 15000:
            box = random.choice(['Med_Box', 'Bullet_Box', 'Small_Box', 'Fast_Box'])
            if box == 'Med_Box':
                Med_Box()
                all_sprites.add(med_box_sprites)
                time = pygame.time.get_ticks()
            elif box == 'Bullet_Box':
                Bullet_Box()
                all_sprites.add(bullet_box_sprites)
                time = pygame.time.get_ticks()
            elif box == 'Small_Box':
                Small_Box()
                all_sprites.add(small_box_sprites)
                time = pygame.time.get_ticks()
            else:
                Fast_Box()
                all_sprites.add(fast_box_sprites)
                time = pygame.time.get_ticks()
        if flag_finish:
            first_drive_sound.stop()
            second_drive_sound.stop()
            finish_screen(flag_finish)
            flag_finish = ''
            FIRST_HP = 100
            SECOND_HP = 100
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 15 and event.pos[0] <= 55:
                    if event.pos[1] >= 15 and event.pos[1] <= 55:
                        return
            if event.type == pygame.KEYDOWN:
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
        first_sprites.update(None)
        second_sprites.update(None)
        bullet_sprites.update()
        med_box_sprites.update()
        fast_box_sprites.update()
        bullet_box_sprites.update()
        small_box_sprites.update()
        all_sprites.draw(screen)
        print_health()
        pygame.draw.rect(screen, 'grey', (15, 15, 40, 40))
        back = pygame.transform.scale(load_image('back.png'), (40, 40))
        screen.blit(back, (15, 14))
        pygame.display.flip()
    terminate()


start_screen()
