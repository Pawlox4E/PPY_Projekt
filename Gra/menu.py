import random
import pygame
import sys
import math
from game_main import main_game
from settings_menu import settings_menu
from Button import Button
from usefull_methods import read_settings

pygame.init()


WINDOW_WIDTH = read_settings( "WIDTH")
WINDOW_HEIGHT = read_settings("HEIGHT")
FPS = read_settings("FPS")
FontS= [0.0,0.01, 0.02, 0.04, 0.06]
FontSize = read_settings("FONT_SIZE")

#font settings
font_size = int(math.sqrt(WINDOW_WIDTH * WINDOW_HEIGHT) * FontS[FontSize])
fontColor = (255, 255, 255)
font = pygame.font.Font("fonts/GloriousChristmas-BLWWB.ttf", font_size)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("PPYPTG")
clock = pygame.time.Clock()

menubackground = f"images/menu/menubackground{random.randint(1, 5)}.png"
background_image = pygame.image.load(menubackground).convert()
background_rect = background_image.get_rect()
background_rect.right = WINDOW_WIDTH

button_background = pygame.image.load("images/menu/button_background1.png").convert_alpha()

title_image = pygame.image.load("images/Tittle.png").convert_alpha()
tittle_rect = title_image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT/3-WINDOW_HEIGHT/12),size=(WINDOW_WIDTH/3, WINDOW_HEIGHT/3))

#latwiej by bylo w liscie - i obslugiwac eventy / rysowanie przez petle
#ale trzeba ogarnac dodanie funkcji np w kostruktorze przycisku  - przez 1 petle na liscie nie obsluzy sie klikniec
buttons = []
startButton = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.55,  WINDOW_WIDTH * 0.2, WINDOW_HEIGHT * 0.1, "START", font, fontColor, button_background)
settingButton = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.65,  WINDOW_WIDTH * 0.2, WINDOW_HEIGHT * 0.1, "SETTINGS", font, fontColor, button_background)
dummyButton = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.75,  WINDOW_WIDTH * 0.2, WINDOW_HEIGHT * 0.1, "SAVES", font, fontColor, button_background)
quitButton = Button(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 0.85,  WINDOW_WIDTH * 0.2, WINDOW_HEIGHT * 0.1, "QUIT", font, fontColor, button_background)

def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def main_menu():
    running = True
    move_left = True

    while running:
        screen.fill((0, 0, 0))

        if move_left:
            background_rect.x -= 1
            if background_rect.right <= WINDOW_WIDTH:
                move_left = False
        else:
            background_rect.x += 1
            if background_rect.left >= 0:
                move_left = True

        screen.blit(background_image, background_rect)
        screen.blit(title_image, tittle_rect)

        #pozyczyłem licznik fps
        fps = font.render(str(int(clock.get_fps())), True, (255, 0, 0))
        screen.blit(fps, (WINDOW_WIDTH - 60*FontSize, 0))

        startButton.draw(screen)
        settingButton.draw(screen)
        dummyButton.draw(screen)
        quitButton.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if startButton.check_click(mousePos):
                    main_game()
                if settingButton.check_click(mousePos):
                    settings_menu(screen, font,background_image,background_rect,WINDOW_WIDTH,WINDOW_HEIGHT)
                if dummyButton.check_click(mousePos):
                    print("DUMMYBUTTON")
                if quitButton.check_click(mousePos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)



if __name__ == "__main__":
    main_menu()