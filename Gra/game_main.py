import pygame
from os.path import join

pygame.init()
pygame.font.init()

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Our game')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Verdana', 15)

player_surf_path = join('images', 'player.png')
player_surf = pygame.image.load(player_surf_path).convert_alpha()
player_rect = player_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
player_direction = pygame.math.Vector2(1, 1)
player_speed = 200

def main_game():
    running = True
    while running:
        delta_time = clock.tick(120) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        screen.fill('white')
        fps = font.render(str(int(clock.get_fps())), True, (255, 0, 0))
        screen.blit(fps, (WINDOW_WIDTH - 60, 0))

        if player_rect.right >= WINDOW_WIDTH:
            player_rect.right = WINDOW_WIDTH
            player_direction.x *= -1
        if player_rect.left < 0:
            player_rect.left = 0
            player_direction.x *= -1
        if player_rect.bottom > WINDOW_HEIGHT:
            player_rect.bottom = WINDOW_HEIGHT
            player_direction.y *= -1
        if player_rect.top < 0:
            player_rect.top = 0
            player_direction.y *= -1

        player_rect.center += player_speed * player_direction * delta_time
        screen.blit(player_surf, player_rect)

        pygame.display.update()