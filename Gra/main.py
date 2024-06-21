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
        self.hp = 100
        self.score = 0

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

        recent_keys = pygame.key.get_pressed()
        if (recent_keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and self.can_shoot:
            Shuriken(shuriken_image, self.rect.midtop, (all_sprites, shuriken_sprites))
            self.can_shoot = False
            self.last_time_shoot = pygame.time.get_ticks()

        self.update_shoot()


class Shuriken(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        mouse_pos = pygame.mouse.get_pos()
        self.direction = pygame.Vector2(mouse_pos[0] - player.rect.center[0], mouse_pos[1] - player.rect.center[1])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.speed = 300

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        if (WINDOW_HEIGHT < self.rect.bottom or self.rect.bottom < 0
                or WINDOW_WIDTH < self.rect.left or self.rect.left < 0):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2(player.rect[0] - self.rect.center[0], player.rect[1] - self.rect.center[1])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.speed = 100
        self.hp = 100
        self.can_attack = True
        self.last_time_attack = 0
        self.attack_cooldown = 500
        self.dmg = 10

    def update_attack(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time_attack >= self.attack_cooldown:
                self.can_attack = True

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        self.direction.x = player.rect[0] - self.rect.center[0]
        self.direction.y = player.rect[1] - self.rect.center[1]
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.update_attack()


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Our game')
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont('Verdana', 15)

spawn_event = pygame.event.custom_type()
pygame.time.set_timer(spawn_event, 1000)

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
shuriken_sprites = pygame.sprite.Group()

player = Player(all_sprites)

shuriken_image = pygame.image.load(join('images', 'shuriken.png')).convert_alpha()
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
enemy_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()


def check_collisions():
    global running
    for enemy in enemy_sprites:

        enemy_collision = enemy.rect.colliderect(player)
        if enemy_collision and enemy.can_attack:
            enemy.can_attack = False
            enemy.last_time_attack = pygame.time.get_ticks()
            player.hp -= enemy.dmg
            if player.hp <= 0:
                running = False

    for shuriken in shuriken_sprites:
        shuriken_collision = pygame.sprite.spritecollide(shuriken, enemy_sprites, False)
        if shuriken_collision:
            player.score += 10
            shuriken_collision[0].kill()
            shuriken.kill()


while running:
    delta_time = clock.tick(120) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_event:
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)
            Enemy(enemy_surf, (x, y), (all_sprites, enemy_sprites))

    screen.fill('#3a2e3f')

    all_sprites.update(delta_time)

    check_collisions()

    all_sprites.draw(screen)
    fps = font.render(str(int(clock.get_fps())), True, (255, 0, 0))
    score = font.render(f'score:{player.score}', True, (0, 0, 255))
    hp = font.render(f'hp:{player.hp}', True, (255, 0, 0))
    screen.blit(fps, (WINDOW_WIDTH - 60, 0))
    screen.blit(score, (WINDOW_WIDTH / 2 - 50, 0))
    screen.blit(hp, (WINDOW_WIDTH / 2 - 50, 25))
    pygame.display.update()

pygame.quit()
