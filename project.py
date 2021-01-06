import os
import sys
import pygame_gui
import random
import pygame


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


class Rules:
    def __init__(self):
        self.text = None
        self.rules = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 140), (120, 50)),
            text='Правила игры',
            manager=manager,
        )
        self.back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 20), (50, 25)),
            text='Назад',
            manager=manager
        )
        self.back.hide()

    def show_rules(self):
        fon = pygame.transform.scale(load_image('fon.jpg'),
                                     (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        self.rules.hide()
        self.text = pygame_gui.elements.ui_text_box.UITextBox(
            html_text='О нет! Земле угрожает опасность! Танос снова '
                      'решил напасть на наш народ! Именно Вам '
                      'предстоит спасти Землю от ужасного злодея! '
                      'Вперед! <br>Перед Вами'
                      ' стоит 5 препядствий, которые нужно выполнить.'
                      'Для паузы нажмите <u>Enter</u>, для сохранения'
                      ' игры <u>Ctrl+S</u>.',
            relative_rect=pygame.Rect((150, 100), (500, 400)),
            manager=manager
        )
        self.back.show()

    def hide_text(self):
        self.text.hide()
        self.back.hide()


class Play:
    def __init__(self):
        self.play = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 410), (100, 50)),
            text='PLAY',
            manager=manager,
        )
        self.play.show()


pygame.init()
fl = False
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager((800, 600), 'buttons.json')
clock = pygame.time.Clock()

FPS = 50


class Cursor(pygame.sprite.Sprite):
    image = load_image("cur.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.image
        self.rect = self.image.get_rect()

    def update(self, coord):
        self.rect.x = coord[0]
        self.rect.y = coord[1]

clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
sprites = pygame.sprite.Group()


def levels():
    level1 = pygame.sprite.Sprite()
    level1.image = load_image("planet.png")
    level1.rect = level1.image.get_rect()
    all_sprites.add(level1)
    level1.rect.x = 70
    level1.rect.y = 450
    level2 = pygame.sprite.Sprite()
    level2.image = load_image("planet2.png")
    level2.rect = level2.image.get_rect()
    all_sprites.add(level2)
    level2.rect.x = 630
    level2.rect.y = 350
    level3 = pygame.sprite.Sprite()
    level3.image = load_image("planet3.png")
    level3.rect = level3.image.get_rect()
    all_sprites.add(level3)
    level3.rect.x = 70
    level3.rect.y = 250
    level4 = pygame.sprite.Sprite()
    level4.image = load_image("planet4.png")
    level4.rect = level4.image.get_rect()
    all_sprites.add(level4)
    level4.rect.x = 630
    level4.rect.y = 150
    level5 = pygame.sprite.Sprite()
    level5.image = load_image("planet5.png")
    level5.rect = level5.image.get_rect()
    all_sprites.add(level5)
    level5.rect.x = 70
    level5.rect.y = 50


class Star(pygame.sprite.Sprite):
    image = load_image("star.png")

    def __init__(self, x, y, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Star.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.i = 2

    def update(self):
        self.i = self.i * (-1)
        self.rect = self.rect.move(self.i, self.i)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["WAR OF THE WORLDS", "",
                  "",
                  "Добро пожаловать в WAR OF THE WORLDS",
                  "Нажмите PLAY для начала игры"]

    fon = pygame.transform.scale(load_image('fon.jpg'),
                                 (WIDTH, HEIGHT))
    rul = Rules()
    play1 = Play()
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, True,
                                      pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 15
        intro_rect.top = text_coord
        intro_rect.x = 15
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play1.play:
                        screen.fill((101, 86, 120))
                        levels()
                        pygame.mouse.set_visible(False)
                        all_sprites.update(pygame.mouse.get_pos())
                        all_sprites.draw(screen)
                        pygame.display.flip()
                        return True
                    if event.ui_element == rul.rules:
                        rul.show_rules()
                    if event.ui_element == rul.back:
                        rul.hide_text()
                        intro_text = ["WAR OF THE WORLDS", "",
                                      "",
                                      "Добро пожаловать в WAR OF "
                                      "THE WORLDS",
                                      "Нажмите PLAY для начала игры"]

                        fon = pygame.transform.scale(
                            load_image('fon.jpg'),
                            (WIDTH, HEIGHT))
                        rul = Rules()
                        screen.blit(fon, (0, 0))
                        font = pygame.font.Font(None, 30)
                        text_coord = 100
                        for line in intro_text:
                            string_rendered = font.render(line, True,
                                                          pygame.Color
                                                          ('whi'
                                                           'te'))
                            intro_rect = string_rendered.get_rect()
                            text_coord += 15
                            intro_rect.top = text_coord
                            intro_rect.x = 15
                            text_coord += intro_rect.height
                            screen.blit(string_rendered, intro_rect)
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


running = False
if start_screen():
    running = True

for i in range(8):
    for j in range(6):
        Star(i*100, j*100, sprites)
levels()
Cursor(all_sprites)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            all_sprites.update(pygame.mouse.get_pos())
            all_sprites.draw(screen)
            pygame.display.flip()
        else:
            pygame.display.flip()
            screen.fill((101, 86, 120))
            all_sprites.draw(screen)
    screen.fill((101, 86, 120))
    sprites.draw(screen)
    #sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
