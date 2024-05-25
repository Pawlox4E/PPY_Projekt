import pygame

pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_HEIGHT))
pygame.display.set_caption('Our game')
running = True

surf = pygame.Surface((200, 100))
surf.fill('purple')
surf_x = 100
surf_y = 150

player_surf = pygame.image.load('images/player.png')

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    surf_x += 0.1
    screen.fill('white')
    screen.blit(surf, (surf_y, surf_x))
    screen.blit(player_surf, (surf_y, surf_x))

    pygame.display.update()

pygame.quit()
