import random
import pygame
import sys

pygame.init()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS = 60

WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Our Game(menu)")
clock = pygame.time.Clock()

menubackground = f"images/menu/menubackground{random.randint(1, 5)}.png"
background_image = pygame.image.load(menubackground).convert()
background_rect = background_image.get_rect()
background_rect.right = WINDOW_WIDTH

button_background = pygame.image.load("images/menu/button_background1.png").convert_alpha()
button_background = pygame.transform.scale(button_background, (600, 100))

my_font = pygame.font.Font("fonts/GloriousChristmas-BLWWB.ttf", 40)

def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


# Funkcja główna menu
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

        button_rect = button_background.get_rect()
        button_rect.center = (WINDOW_WIDTH // 2, 275)
        screen.blit(button_background, button_rect)

        button_rect.center = (WINDOW_WIDTH // 2, 375)
        screen.blit(button_background, button_rect)

        button_rect.center = (WINDOW_WIDTH // 2, 475)
        screen.blit(button_background, button_rect)

        button_rect.center = (WINDOW_WIDTH // 2, 575)
        screen.blit(button_background, button_rect)

        # Rysowanie tekstu na przyciskach
        draw_text(screen, "START", my_font, WHITE, WINDOW_WIDTH // 2, 255)
        draw_text(screen, "SETTTINGS", my_font, WHITE, WINDOW_WIDTH // 2, 355)
        draw_text(screen, "DUMMYBUTTON", my_font, WHITE, WINDOW_WIDTH // 2, 455)
        draw_text(screen, "EXIT", my_font, WHITE, WINDOW_WIDTH // 2, 555)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #hujowe - do przerobki odczytwyanie klikniecia
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                #print(mouse_pos)
                if 685 <= mouse_pos[0] <= 1230 and 245 <= mouse_pos[1] <= 305:
                    print("START")
                if 685 <= mouse_pos[0] <= 1230 and 345 <= mouse_pos[1] <= 405:
                    print("SETTTINGS")
                if 685 <= mouse_pos[0] <= 1230 and 445 <= mouse_pos[1] <= 505 :
                    print("DUMMYBUTTON")
                if 685 <= mouse_pos[0] <= 1230 and 545 <= mouse_pos[1] <= 605:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()