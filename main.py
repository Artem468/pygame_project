import pygame
import os
import sys

pygame.init()
size = width, height = 900, 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('PyGame project')
FPS = 60

first_player = 'blue'
second_player = 'red'
all_sprites = pygame.sprite.Group()


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


class First_tank_preview(pygame.sprite.Sprite):
    image = load_image(f'{first_player}_tank.png')
    image = pygame.transform.scale(image, (90, 90))
    image = pygame.transform.rotate(image, -90)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = First_tank_preview.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 600
        self.speed = 10

    def update(self, *args):
        self.rect.x += self.speed
        if self.rect.x == 1000:
            self.rect.x = 0


class Second_tank_preview(pygame.sprite.Sprite):
    image = load_image(f'{second_player}_tank.png')
    image = pygame.transform.scale(image, (90, 90))
    image = pygame.transform.rotate(image, 90)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Second_tank_preview.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 900, 700
        self.speed = 10

    def update(self, *args):
        self.rect.x -= self.speed
        if self.rect.x == -100:
            self.rect.x = 900 + self.rect.width


def select_skin_update(player):
    fon = pygame.transform.scale(load_image('fon.png'), size)
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
    pygame.draw.rect(screen, 'white', (200, height // 2 - 45, 90, 90))
    pygame.draw.rect(screen, 'white', (400, height // 2 - 45, 90, 90))
    pygame.draw.rect(screen, 'white', (600, height // 2 - 45, 90, 90))
    screen.blit(blue, (200, height // 2 - 45))
    screen.blit(red, (400, height // 2 - 45))
    screen.blit(green, (600, height // 2 - 45))


def select_skin(player):
    select_skin_update(player)

    done = pygame.transform.scale(load_image('done.png'), (20, 20))
    if player == '1st player':
        pygame.draw.rect(screen, 'green', (235, height // 2 + 55, 20, 20))
        screen.blit(done, (234, height // 2 + 55))
    if player == '2nd player':
        pygame.draw.rect(screen, 'green', (435, height // 2 + 55, 20, 20))
        screen.blit(done, (434, height // 2 + 55))
    global first_player, second_player
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 15 and event.pos[0] <= 55:
                    if event.pos[1] >= 15 and event.pos[1] <= 55:
                        print(first_player, second_player)
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

    fon = pygame.transform.scale(load_image('fon.png'), size)
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
    tank1 = First_tank_preview(all_sprites)
    tank2 = Second_tank_preview(all_sprites)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] >= 365 and event.pos[0] <= 530:
                    if event.pos[1] >= 300 and event.pos[1] <= 350:
                        return
                if event.pos[0] >= 180 and event.pos[0] <= 440:
                    if event.pos[1] >= 400 and event.pos[1] <= 435:
                        select_skin('1st player')
                        start_screen_update()
                if event.pos[0] >= 470 and event.pos[0] <= 730:
                    if event.pos[1] >= 400 and event.pos[1] <= 435:
                        select_skin('2nd player')
                        start_screen_update()
        start_screen_update()
        tank1.update()
        tank2.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


clock = pygame.time.Clock()
start_screen()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 5
        self.top = 5
        self.cell_size = 10

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(0, 82, 33), (
                    x * self.cell_size + self.left,
                    y * self.cell_size + self.top,
                    self.cell_size,
                    self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        x1 = (mouse_pos[0] - self.left) // self.cell_size
        y1 = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= x1 < self.width and 0 <= y1 < self.height:
            print((x1, y1))
        else:
            print(None)

    def on_click(self, cell_coords):
        ...


class First_tank(pygame.sprite.Sprite):
    image = load_image(f'{first_player}_tank.png')
    image = pygame.transform.scale(image, (90, 90))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = First_tank.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 810
        self.direction = 'up'

    def update(self, direction):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -1
            if self.direction == 'right':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'up':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.direction == 'down':
                self.image = pygame.transform.rotate(self.image, 270)
            self.direction = 'left'
        if keystate[pygame.K_d]:
            self.speedx = 1
            if self.direction == 'left':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'up':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.direction == 'down':
                self.image = pygame.transform.rotate(self.image, 90)
            self.direction = 'right'
        if keystate[pygame.K_w]:
            self.speedy = -1
            if self.direction == 'down':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'left':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.direction == 'right':
                self.image = pygame.transform.rotate(self.image, 90)
            self.direction = 'up'
        if keystate[pygame.K_s]:
            self.speedy = 1
            if self.direction == 'up':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'left':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.direction == 'right':
                self.image = pygame.transform.rotate(self.image, 270)
            self.direction = 'down'
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
    image = pygame.transform.scale(image, (90, 90))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Second_tank.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 810, 0
        self.direction = 'up'

    def update(self, direction):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -1
            if self.direction == 'right':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'up':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.direction == 'down':
                self.image = pygame.transform.rotate(self.image, 270)
            self.direction = 'left'
        if keystate[pygame.K_RIGHT]:
            self.speedx = 1
            if self.direction == 'left':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'up':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.direction == 'down':
                self.image = pygame.transform.rotate(self.image, 90)
            self.direction = 'right'
        if keystate[pygame.K_UP]:
            self.speedy = -1
            if self.direction == 'down':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'left':
                self.image = pygame.transform.rotate(self.image, 270)
            elif self.direction == 'right':
                self.image = pygame.transform.rotate(self.image, 90)
            self.direction = 'up'
        if keystate[pygame.K_DOWN]:
            self.speedy = 1
            if self.direction == 'up':
                self.image = pygame.transform.rotate(self.image, 180)
            elif self.direction == 'left':
                self.image = pygame.transform.rotate(self.image, 90)
            elif self.direction == 'right':
                self.image = pygame.transform.rotate(self.image, 270)
            self.direction = 'down'
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


first_sprites = pygame.sprite.Group()
First_tank(first_sprites)
second_sprites = pygame.sprite.Group()
Second_tank(second_sprites)
all_sprites.add(first_sprites)
all_sprites.add(second_sprites)
board = Board(10, 10)
board.set_view(0, 0, 90)
running = True
while running:
    clock.tick(FPS)
    first_sprites.update(None)
    second_sprites.update(None)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
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
    screen.fill((26, 148, 49))
    all_sprites.draw(screen)
    board.render(screen)
    pygame.display.flip()
pygame.quit()
