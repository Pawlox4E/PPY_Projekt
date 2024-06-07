import random
from os.path import join

import pygame

pygame.init()
pygame.font.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2(0, 0)
        self.speed = 500
        self.can_shoot = True
        self.last_time_shoot = 0
        self.cooldown_duration = 500

    def update_shoot(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time_shoot >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        self.direction.y = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * delta_time

        recent_keys = pygame.key.get_just_pressed()
        if (recent_keys[pygame.K_SPACE] or pygame.mouse.get_just_pressed()[0]) and self.can_shoot:
            Shuriken(shuriken_image, self.rect.midtop, all_sprites)
            self.can_shoot = False
            self.last_time_shoot = pygame.time.get_ticks()

        self.update_shoot()


class Shuriken(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        # self.direction = direction.normalize() if direction else direction

    def update(self, delta_time):
        self.rect.centery -= delta_time * 300
        # self.rect.center += delta_time * self.direction
        if self.rect.bottom < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=pos)

    def update(self, delta_time):
        self.rect.center 

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Our game')
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont('Verdana', 15)

spawn_event = pygame.event.custom_type()
pygame.time.set_timer(spawn_event, 1000)

shuriken_image = pygame.image.load(join('images', 'shuriken.png')).convert_alpha()
all_sprites = pygame.sprite.Group()
player = Player(all_sprites)
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
while running:
    delta_time = clock.tick(120) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_event:
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)
            Enemy(player_surf, (x, y), all_sprites)

    screen.fill('white')

    all_sprites.update(delta_time)
    all_sprites.draw(screen)

    fps = font.render(str(int(clock.get_fps())), True, (255, 0, 0))
    screen.blit(fps, (WINDOW_WIDTH - 60, 0))
    pygame.display.update()
pygame.quit()
