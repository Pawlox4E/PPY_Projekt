import pygame
import sys
from Button import Button
from usefull_methods import read_settings, save_settings_to_file, write_score


class TextInputBox:
    def __init__(self, x, y, w, h, font, initial_text=''):
        self.rect = pygame.Rect(x-w/2, y+h/2, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = initial_text
        self.font = font
        self.txt_surface = self.font.render(initial_text, True, self.color)
        self.active = False
        self.background_color = pygame.Color(0, 0, 0, 128)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def draw(self, screen):
        bg_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        bg_surface.fill(self.background_color)
        screen.blit(bg_surface, self.rect.topleft)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def endscreen(screen, font, background_image, background_rect, WINDOW_WIDTH, WINDOW_HEIGHT, score):
    running = True
    move_left = True
    clock = pygame.time.Clock()
    background = pygame.image.load("images/menu/button_background1.png").convert_alpha()

    quitButton = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.85, WINDOW_WIDTH * 0.2, WINDOW_HEIGHT * 0.1, "QUIT", font, (255, 255, 255), background)
    title_image = pygame.image.load("images/Tittle.png").convert_alpha()
    tittle_rect = title_image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3 - WINDOW_HEIGHT / 12),
                                       size=(WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3))

    input_box = TextInputBox(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WINDOW_WIDTH // 4, WINDOW_HEIGHT // 12, font)

    while running:
        screen.fill((0, 0, 0))
        screen.blit(background_image, background_rect)
        screen.blit(title_image, tittle_rect)

        if move_left:
            background_rect.x -= 1
            if background_rect.right <= WINDOW_WIDTH:
                move_left = False
        else:
            background_rect.x += 1
            if background_rect.left >= 0:
                move_left = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if quitButton.check_click(mouse_pos):
                    player = input_box.text
                    write_score(player,score)
                    running = False
            input_box.handle_event(event)

        quitButton.draw(screen)
        input_box.draw(screen)

        pygame.display.update()
        clock.tick(60)