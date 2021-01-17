import os
import sys
import pygame_gui
import random
import pygame

TIMER_EVENT_TYPE = pygame.USEREVENT + 1
running = False
is_paused = False
count = 0
f = open('best_count', encoding="utf8")
BEST_COUNT = int(f.read())
f.close()


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


class Button:
    def __init__(self):
        self.width = 200
        self.height = 60
        self.x = 300
        self.y = 340

    def render(self):
        font = pygame.font.Font(None, 30)
        text = font.render('Играть заново', True, (0, 0, 0))
        pygame.draw.rect(screen, (114, 51, 119),
                         (self.x, self.y, self.width, self.height), 0)
        screen.blit(text,
                    (self.x + (self.width - text.get_width()) // 2,
                     self.y + (self.height - text.get_height()) // 2))

    def check_click(self, pos):
        if self.x <= pos[0] <= self.width + self.x and \
                self.y <= pos[1] <= self.height + self.y:
            global running
            running = True
            enemys.empty()
            bullets.empty()
            meteorits.empty()
            main()


class ButtonOut:
    def __init__(self):
        self.width = 200
        self.height = 60
        self.x = 300
        self.y = 220

    def render(self):
        font = pygame.font.Font(None, 30)
        text = font.render('Выйти из игры', True, (0, 0, 0))
        pygame.draw.rect(screen, (114, 51, 119),
                         (self.x, self.y, self.width, self.height), 0)
        screen.blit(text,
                    (self.x + (self.width - text.get_width()) // 2,
                     self.y + (self.height - text.get_height()) // 2))

    def check_click(self, pos):
        if self.x <= pos[0] <= self.width + self.x and \
                self.y <= pos[1] <= self.height + self.y:
            terminate()


class ButtonPause:
    def __init__(self):
        self.width = 100
        self.height = 50
        self.x = 700
        self.y = 0

    def render(self):
        font = pygame.font.Font(None, 30)
        text = font.render('Пауза', True, (0, 0, 0))
        pygame.draw.rect(screen, (114, 51, 119),
                         (self.x, self.y, self.width, self.height), 0)
        screen.blit(text,
                    (self.x + (self.width - text.get_width()) // 2,
                     self.y + (self.height - text.get_height()) // 2))

    def check_click(self, pos):
        if self.x <= pos[0] <= self.width + self.x and \
                self.y <= pos[1] <= self.height + self.y:
            global is_paused
            is_paused = not is_paused
            pygame.time.set_timer(TIMER_EVENT_TYPE, 0 if is_paused else 20)

    def render2(self):
        font = pygame.font.Font(None, 20)
        text = font.render('Продолжить', True, (0, 0, 0))
        pygame.draw.rect(screen, (114, 51, 119),
                         (self.x, self.y, self.width, self.height), 0)
        screen.blit(text,
                    (self.x + (self.width - text.get_width()) // 2,
                     self.y + (self.height - text.get_height()) // 2))


pygame.init()
fl = False
size = WIDTH, HEIGHT = 800, 600
pygame.time.set_timer(TIMER_EVENT_TYPE, 20)
screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager((800, 600), 'buttons.json')
clock = pygame.time.Clock()
delay = 1000
FPS = 60


class Player(pygame.sprite.Sprite):
    image = load_image("player.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Player.image
        self.move = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 325
        self.rect.y = 450

    def update(self):
        self.move = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.move = -5
        if key[pygame.K_RIGHT]:
            self.move = 5
        if key[pygame.K_a]:
            self.move = -5
        if key[pygame.K_d]:
            self.move = 5
        self.rect.x += self.move
        if self.rect.x + 150 > 800:
            self.rect.x = 650
        if self.rect.x < 0:
            self.rect.x = 0


sprites = pygame.sprite.Group()
enemys = pygame.sprite.Group()
bullets = pygame.sprite.Group()
meteorits = pygame.sprite.Group()


class Meteorite(pygame.sprite.Sprite):
    image = load_image("meteor.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Meteorite.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(800 - 180)
        self.rect.y = random.randrange(-100, -40)
        self.y = random.randrange(2, 7)
        self.x = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.y
        self.rect.x += self.x
        if self.rect.y > 600 or self.rect.x < -180 or \
                self.rect.x > 980:
            self.rect.x = random.randrange(800 - 180)
            self.rect.y = random.randrange(-100, -40)
            self.y = random.randrange(2, 7)
        if pygame.sprite.collide_mask(self, player):
            pygame.time.set_timer(TIMER_EVENT_TYPE, 0)
            you_lose()
        a = pygame.sprite.groupcollide(bullets, meteorits, True, False)


class Enemy(pygame.sprite.Sprite):
    image = load_image("enemy.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Enemy.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(800 - 180)
        self.rect.y = random.randrange(-100, -40)
        self.y = random.randrange(2, 7)
        self.x = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.y
        self.rect.x += self.x
        if self.rect.y > 600 or self.rect.x < -180 or \
                self.rect.x > 980:
            self.rect.x = random.randrange(800 - 180)
            self.rect.y = random.randrange(-100, -40)
            self.y = random.randrange(2, 7)
        if pygame.sprite.collide_mask(self, meteor):
            self.rect.x = random.randrange(800 - 180)
            self.rect.y = random.randrange(-100, -40)
            self.y = random.randrange(2, 7)


class Bullet(pygame.sprite.Sprite):
    image = load_image("boom.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bullet.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 55
        self.rect.y = 535
        self.move = -10

    def update(self):
        self.rect.y += self.move
        if pygame.sprite.groupcollide(bullets, enemys, True, True):
            Enemy(enemys)
            global count
            count += 1


class Cursor(pygame.sprite.Sprite):
    image = load_image("cur.png")

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Cursor.image
        self.rect = self.image.get_rect()

    def update(self, coord):
        self.rect.x = coord[0]
        self.rect.y = coord[1]


all_sprites = pygame.sprite.Group()
Cursor(all_sprites)


def main_game():
    fon = pygame.transform.scale(
        load_image('fon2.jpg'),
        (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    sprites.draw(screen)
    enemys.draw(screen)
    bullets.draw(screen)
    meteorits.draw(screen)


def write_count(count):
    font = pygame.font.Font(None, 30)
    text = font.render(f'Текущий счет: {count}', True, (255, 255, 255))
    screen.blit(text, (5, 5))


def you_lose():
    sprites.empty()
    global running
    running = False


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
        flag = False
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                all_sprites.update(pygame.mouse.get_pos())
                all_sprites.draw(screen)
                pygame.display.flip()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play1.play:
                        screen.fill((101, 86, 120))
                        pygame.mouse.set_visible(False)
                        all_sprites.update(pygame.mouse.get_pos())
                        pygame.display.flip()
                        all_sprites.draw(screen)
                        pygame.display.flip()
                        return True
                    if event.ui_element == rul.rules:
                        flag = True
                        rul.show_rules()
                    if event.ui_element == rul.back:
                        flag = False
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
        if flag:
            intro_text = []
        else:
            intro_text = ["WAR OF THE WORLDS", "",
                          "",
                          "Добро пожаловать в WAR OF "
                          "THE WORLDS",
                          "Нажмите PLAY для начала игры"]
        fon = pygame.transform.scale(
            load_image('fon.jpg'),
            (WIDTH, HEIGHT))
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
        manager.update(time_delta)
        manager.draw_ui(screen)
        # pygame.display.flip()
        clock.tick(FPS)


button_pause = ButtonPause()


def main():
    global player
    player = Player(sprites)
    pygame.time.set_timer(TIMER_EVENT_TYPE, 20)
    for _ in range(2):
        global enemy
        enemy = Enemy(enemys)
    for _ in range(3):
        global meteor
        meteor = Meteorite(meteorits)
    global running
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                all_sprites.update(pygame.mouse.get_pos())
                all_sprites.draw(screen)
                pygame.display.flip()
            else:
                pygame.display.flip()
                main_game()
                if is_paused:
                    button_pause.render2()
                else:
                    button_pause.render()
                write_count(count)
            if event.type == TIMER_EVENT_TYPE:
                sprites.update()
                enemys.update()
                bullets.update()
                meteorits.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_pause.check_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(bullets)
                    bullet.move = -10
        main_game()
        button_pause.render()
        if is_paused:
            button_pause.render2()
        write_count(count)
        pygame.display.flip()


button = Button()
button_out = ButtonOut()
if start_screen():
    count = 0
    running = True
    main()
if not running:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                all_sprites.update(pygame.mouse.get_pos())
                all_sprites.draw(screen)
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:
                button.check_click(event.pos)
                button_out.check_click(event.pos)
        fon = pygame.transform.scale(
            load_image('fon2.jpg'),
            (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        pygame.draw.rect(screen, (134, 85, 235), (100, 100, 600, 400),
                         0)
        font = pygame.font.Font(None, 30)
        text = font.render(f'Ваш счет: {count}', True, (0, 0, 0))
        if count > BEST_COUNT:
            BEST_COUNT = count
            f = open("best_count", mode='w')
            f.write(f'{count}')
            f.close()
        textBC = font.render(f'Лучший счет: {BEST_COUNT}', True, (0, 0, 0))
        screen.blit(text, (300, 125))
        screen.blit(textBC, (300, 165))
        button.render()
        button_out.render()
        all_sprites.update(pygame.mouse.get_pos())
        all_sprites.draw(screen)
        pygame.display.flip()
pygame.quit()
