import os
import sys
import random
import pygame_gui

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


class Rules():
    def __init__(self):
        self.text = None
        self.rules = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((20, 140), (120, 50)),
            text='Правила игры',
            manager=manager
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
                      'предстоит спасти Землю от ужасного Таноса! '
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


pygame.init()
fl = False
size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager((800, 600))
clock = pygame.time.Clock()

FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["WAR OF THE WORLDS", "",
                  "",
                  "Нажмите PLAY для начала игры",
                  "Восстановите игру"]

    fon = pygame.transform.scale(load_image('fon.jpg'),
                                 (WIDTH, HEIGHT))
    rul = Rules()
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return True
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == rul.rules:
                        rul.show_rules()
                    if event.ui_element == rul.back:
                        rul.hide_text()
                        start_screen()
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


running = False
if start_screen():
    running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((235, 195, 155))
    # pygame.draw.rect(screen, (0, 0, 0), (20, 20, 50, 50), 1)
    pygame.display.flip()
pygame.quit()
