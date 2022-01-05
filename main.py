import pygame
import os
import sys

pygame.init()
size = width, height = 900, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyGame project')
FPS = 60
TIME_RELOAD = 3000
SPEED = 5

first_player = 'blue'
second_player = 'red'
all_sprites = pygame.sprite.Group()
flag_tanks = False

right_st_wall = pygame.sprite.Group()
left_st_wall = pygame.sprite.Group()
up_st_wall = pygame.sprite.Group()
down_st_wall = pygame.sprite.Group()


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
running = True
clock = pygame.time.Clock()
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


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
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


def tanks_preview_update():
    global tank1, tank2, flag_tanks
    if flag_tanks:
        tank1.rect.x = -200
        tank2.rect.x = 1100
        tank1 = First_tank_preview(all_sprites)
        tank1.rect.x = -90
        tank2.rect.x = 900
        print(first_player, second_player)
        im = load_image(f'{first_player}_tank.png')
        im = pygame.transform.scale(im, (90, 90))
        im = pygame.transform.rotate(im, 270)
        tank1.image = im
        im = load_image(f'{second_player}_tank.png')
        im = pygame.transform.scale(im, (90, 90))
        im = pygame.transform.rotate(im, 90)
        tank2.image = im
    else:
        tank1 = First_tank_preview(all_sprites)
        tank2 = Second_tank_preview(all_sprites)
        flag_tanks = True


class First_tank_preview(pygame.sprite.Sprite):
    image = load_image(f'{first_player}_tank.png')
    if first_player == 'blue':
        image = pygame.transform.scale(image, (80, 70))
    elif second_player == 'green':
        image = pygame.transform.scale(image, (80, 80))
    else:
        image = pygame.transform.scale(image, (70, 80))
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
    image = load_image(f'{second_player}_tank.png')
    if second_player == 'blue':
        image = pygame.transform.scale(image, (80, 70))
    elif second_player == 'green':
        image = pygame.transform.scale(image, (80, 80))
    else:
        image = pygame.transform.scale(image, (70, 80))
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

    blue = pygame.transform.scale(load_image('blue_tank.png'), (90, 80))
    red = pygame.transform.scale(load_image('red_tank.png'), (80, 90))
    green = pygame.transform.scale(load_image('green_tank.png'), (90, 90))
    screen.blit(blue, (200, height // 2 - 45))
    screen.blit(red, (400, height // 2 - 45))
    screen.blit(green, (600, height // 2 - 45))


def select_skin(player):
    select_skin_update(player)
    global first_player, second_player
    done = pygame.transform.scale(load_image('done.png'), (20, 20))
    if player == '1st player':
        if first_player == 'blue':
            pygame.draw.rect(screen, 'green', (235, height // 2 + 55, 20, 20))
            screen.blit(done, (234, height // 2 + 55))
        elif first_player == 'red':
            pygame.draw.rect(screen, 'green', (435, height // 2 + 55, 20, 20))
            screen.blit(done, (434, height // 2 + 55))
        else:
            pygame.draw.rect(screen, 'green', (635, height // 2 + 55, 20, 20))
            screen.blit(done, (634, height // 2 + 55))
    if player == '2nd player':
        if second_player == 'blue':
            pygame.draw.rect(screen, 'green', (235, height // 2 + 55, 20, 20))
            screen.blit(done, (234, height // 2 + 55))
        elif second_player == 'red':
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
                            first_player = 'blue'
                        else:
                            second_player = 'blue'
                    if event.pos[0] >= 400 and event.pos[0] <= 490:
                        select_skin_update(player)
                        pygame.draw.rect(screen, 'green', (435, height // 2 + 55, 20, 20))
                        screen.blit(done, (434, height // 2 + 55))
                        if player == '1st player':
                            first_player = 'red'
                        else:
                            second_player = 'red'
                    if event.pos[0] >= 600 and event.pos[0] <= 690:
                        select_skin_update(player)
                        pygame.draw.rect(screen, 'green', (635, height // 2 + 55, 20, 20))
                        screen.blit(done, (634, height // 2 + 55))
                        if player == '1st player':
                            first_player = 'green'
                        else:
                            second_player = 'green'
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
                        return
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
        all_sprites.draw(screen)
        pygame.display.flip()



clock = pygame.time.Clock()
start_screen()


class Bullet(pygame.sprite.Sprite):
    image = load_image('bullet.png')
    image = pygame.transform.scale(image, (15, 35))

    def __init__(self, *group):
        super(Bullet, self).__init__(*group)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -100, -100
        self.direction = 'up'
        self.speed = 5
        self.flag = False

    def update(self):
        if self.flag:
            if self.direction == 'up':
                self.rect.y -= self.speed
            elif self.direction == 'down':
                self.rect.y += self.speed
            elif self.direction == 'left':
                self.rect.x -= self.speed
            elif self.direction == 'right':
                self.rect.x += self.speed
        if self.rect.x > 900:
            self.flag = False
        elif self.rect.x < -35:
            self.flag = False
        elif self.rect.y > 900:
            self.flag = False
        elif self.rect.y < -40:
            self.flag = False


bullet_sprites = pygame.sprite.Group()
bullet = Bullet(bullet_sprites)


class First_tank(pygame.sprite.Sprite):
    image = load_image(f'{first_player}_tank.png')
    if first_player == 'blue':
        image = pygame.transform.scale(image, (80, 70))
    elif second_player == 'green':
        image = pygame.transform.scale(image, (80, 80))
    else:
        image = pygame.transform.scale(image, (70, 80))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = First_tank.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 810
        self.direction = 'up'
        self.timer = pygame.time
        self.fire_time = 0

    def update(self, action):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            if not pygame.sprite.spritecollideany(self, left_st_wall):
                self.speedx = -SPEED
                if self.direction == 'right':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'up':
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.direction == 'down':
                    self.image = pygame.transform.rotate(self.image, 270)
                self.direction = 'left'
        if keystate[pygame.K_d]:
            if not pygame.sprite.spritecollideany(self, right_st_wall):
                self.speedx = SPEED
                if self.direction == 'left':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'up':
                    self.image = pygame.transform.rotate(self.image, 270)
                elif self.direction == 'down':
                    self.image = pygame.transform.rotate(self.image, 90)
                self.direction = 'right'
        if keystate[pygame.K_w]:
            if not pygame.sprite.spritecollideany(self, down_st_wall):
                self.speedy = -SPEED
                if self.direction == 'down':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'left':
                    self.image = pygame.transform.rotate(self.image, 270)
                elif self.direction == 'right':
                    self.image = pygame.transform.rotate(self.image, 90)
                self.direction = 'up'
        if keystate[pygame.K_s]:
            if not pygame.sprite.spritecollideany(self, up_st_wall):
                self.speedy = SPEED
                if self.direction == 'up':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'left':
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.direction == 'right':
                    self.image = pygame.transform.rotate(self.image, 270)
                self.direction = 'down'
        if action == 'fire':
            if self.timer.get_ticks() - self.fire_time >= TIME_RELOAD:
                self.fire_time = self.timer.get_ticks()
                bullet = Bullet(bullet_sprites)
                all_sprites.add(bullet_sprites)
                if self.direction == 'left':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 70
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 5
                    if bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    elif bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    bullet.direction = 'left'
                if self.direction == 'right':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 + 40
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 5
                    if bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    elif bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    bullet.direction = 'right'
                if self.direction == 'up':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 7
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 70
                    if bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    elif bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    bullet.direction = 'up'
                if self.direction == 'down':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 7
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 + 40
                    if bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    elif bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    bullet.direction = 'down'
                bullet.flag = True
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
    image = load_image(f'{second_player}_tank.png')
    if second_player == 'blue':
        image = pygame.transform.scale(image, (80, 70))
    elif second_player == 'green':
        image = pygame.transform.scale(image, (80, 80))
    else:
        image = pygame.transform.scale(image, (70, 80))
    image = pygame.transform.rotate(image, 180)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Second_tank.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 810, 0
        self.direction = 'down'
        self.timer = pygame.time
        self.fire_time = 0

    def update(self, action):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            if not pygame.sprite.spritecollideany(self, left_st_wall):
                self.speedx = -SPEED
                if self.direction == 'right':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'up':
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.direction == 'down':
                    self.image = pygame.transform.rotate(self.image, 270)
                self.direction = 'left'
        if keystate[pygame.K_RIGHT]:
            if not pygame.sprite.spritecollideany(self, right_st_wall):
                self.speedx = SPEED
                if self.direction == 'left':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'up':
                    self.image = pygame.transform.rotate(self.image, 270)
                elif self.direction == 'down':
                    self.image = pygame.transform.rotate(self.image, 90)
                self.direction = 'right'
        if keystate[pygame.K_UP]:
            if not pygame.sprite.spritecollideany(self, down_st_wall):
                self.speedy = -SPEED
                if self.direction == 'down':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'left':
                    self.image = pygame.transform.rotate(self.image, 270)
                elif self.direction == 'right':
                    self.image = pygame.transform.rotate(self.image, 90)
                self.direction = 'up'
        if keystate[pygame.K_DOWN]:
            if not pygame.sprite.spritecollideany(self, up_st_wall):
                self.speedy = SPEED
                if self.direction == 'up':
                    self.image = pygame.transform.rotate(self.image, 180)
                elif self.direction == 'left':
                    self.image = pygame.transform.rotate(self.image, 90)
                elif self.direction == 'right':
                    self.image = pygame.transform.rotate(self.image, 270)
                self.direction = 'down'
        if action == 'fire':
            if self.timer.get_ticks() - self.fire_time >= TIME_RELOAD:
                self.fire_time = self.timer.get_ticks()
                bullet = Bullet(bullet_sprites)
                all_sprites.add(bullet_sprites)
                if self.direction == 'left':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 70
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 5
                    if bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    elif bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    bullet.direction = 'left'
                if self.direction == 'right':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 + 40
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 5
                    if bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    elif bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    bullet.direction = 'right'
                if self.direction == 'up':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 7
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 - 70
                    if bullet.direction == 'down':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    elif bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    bullet.direction = 'up'
                if self.direction == 'down':
                    bullet.rect.x = self.rect.x + self.image.get_width() // 2 - 7
                    bullet.rect.y = self.rect.y + self.image.get_height() // 2 + 40
                    if bullet.direction == 'up':
                        bullet.image = pygame.transform.rotate(bullet.image, 180)
                    elif bullet.direction == 'left':
                        bullet.image = pygame.transform.rotate(bullet.image, 90)
                    elif bullet.direction == 'right':
                        bullet.image = pygame.transform.rotate(bullet.image, 270)
                    bullet.direction = 'down'
                bullet.flag = True
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


level_map = load_level("map.map")
generate_level(level_map)

first_sprites = pygame.sprite.Group()
First_tank(first_sprites)
second_sprites = pygame.sprite.Group()
Second_tank(second_sprites)
all_sprites.add(sprite_group)
all_sprites.add(first_sprites)
all_sprites.add(second_sprites)
all_sprites.add(up_st_wall)
all_sprites.add(down_st_wall)
all_sprites.add(right_st_wall)
all_sprites.add(left_st_wall)


running = True
while running:
    clock.tick(FPS)
    first_sprites.update(None)
    second_sprites.update(None)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                first_sprites.update('up')
            elif event.key == pygame.K_UP:
                second_sprites.update('up')
            elif event.key == pygame.K_s:
                first_sprites.update('down')
            elif event.key == pygame.K_DOWN:
                second_sprites.update('down')
            elif event.key == pygame.K_a:
                first_sprites.update('left')
            elif event.key == pygame.K_LEFT:
                second_sprites.update('left')
            elif event.key == pygame.K_d:
                first_sprites.update('right')
            elif event.key == pygame.K_RIGHT:
                second_sprites.update('right')
            elif event.key == pygame.K_LSHIFT:
                first_sprites.update('fire')
            elif event.key == pygame.K_RSHIFT:
                second_sprites.update('fire')
    bullet_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip()
pygame.quit()
