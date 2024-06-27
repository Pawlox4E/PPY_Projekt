import random
import pygame
from enum import Enum
from os.path import join
from player import Player
from sprites import *
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.Vector2(0, 0)
        self.image_direction = 1  # right(1) or left(-1) direction
        self.speed = 300
        self.can_shoot = True
        self.last_time_shoot = 0
        self.cooldown_duration = 50
        self.hp = 100
        self.score = 0

    def update_shoot(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time_shoot >= self.cooldown_duration:
                self.can_shoot = True

    def check_direction(self):
        if self.direction.x < 0 < self.image_direction:
            self.image_direction = -1
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.direction.x > 0 > self.image_direction:
            self.image_direction = 1
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = (keys[pygame.K_d] - keys[pygame.K_a]) + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        self.direction.y = (keys[pygame.K_s] - keys[pygame.K_w]) + (keys[pygame.K_DOWN] - keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * delta_time
        self.check_direction()
        recent_keys = pygame.key.get_pressed()
        if (recent_keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and self.can_shoot:
            Shuriken(shuriken_image, self.rect.center, (all_sprites, shuriken_sprites))
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
        self.dmg = 10

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        if (WINDOW_HEIGHT < self.rect.bottom or self.rect.bottom < 0
                or WINDOW_WIDTH < self.rect.left or self.rect.left < 0):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.walk_frames = frames[0]
        self.walk_frame_index = 0
        self.attack_frames = frames[1]
        self.attack_frame_index = 0
        self.image = self.walk_frames[self.walk_frame_index]
        self.update_animation_speed = 5
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2(player.rect.center[0] - self.rect.center[0],
                                        player.rect.center[1] - self.rect.center[1])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.image_direction = -1 if self.rect.centerx < player.rect.centerx else 1  # 1 to patrzy w prowa -1 to w lewo
        if self.image_direction == 1:  # defaultowa png patrzy w lewo wiec jesli chcemy zeby bylo w prawo musimy obrocic
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed = 10
        self.hp = 20
        self.can_attack = True
        self.last_time_attack = 0
        self.attack_cooldown = 500
        self.dmg = 10

    def update_attack(self):
        if not self.can_attack:
            self.update_attack_frames(delta_time)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time_attack >= self.attack_cooldown:
                self.can_attack = True

    def check_direction(self):
        if self.direction.x < 0 < self.image_direction:
            self.image_direction = -1
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.direction.x > 0 > self.image_direction:
            self.image_direction = 1
            self.image = pygame.transform.flip(self.image, True, False)

    def update_walk(self, delta_time):
        self.walk_frame_index += self.update_animation_speed * delta_time
        self.image = self.walk_frames[int(self.walk_frame_index) % len(self.walk_frames)]
        if self.image_direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update_attack_frames(self, delta_time):
        self.attack_frame_index += self.update_animation_speed * delta_time
        self.image = self.attack_frames[int(self.attack_frame_index) % len(self.attack_frames)]
        if self.image_direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        self.direction.x = player.rect.center[0] - self.rect.center[0]
        self.direction.y = player.rect.center[1] - self.rect.center[1]
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.update_walk(delta_time)
        self.check_direction()
        self.update_attack()


class ActionType(Enum):
    Appear = 1
    Walk = 2
    Attack = 3
    Die = 4


class AnimatedAction(pygame.sprite.Sprite):
    def __init__(self, frames, pos, change_direction, action_type, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.action_type = action_type
        self.change_direction = change_direction
        if self.change_direction:
            self.image = pygame.transform.flip(self.frames[self.frame_index], True, False)
        self.rect = self.image.get_frect(center=pos)
        self.update_speed = 5

    def update(self, delta_time):
        self.frame_index += self.update_speed * delta_time
        if self.frame_index < len(self.frames):
            if self.change_direction:
                self.image = pygame.transform.flip(self.frames[int(self.frame_index)], True, False)
            else:
                self.image = self.frames[int(self.frame_index)]
        else:
            if self.action_type == ActionType.Appear:
                Enemy([walk_frames, attack_frames], self.rect.center, (all_sprites, enemy_sprites))
            self.kill()


# class Game:
#     def __init__(self):
#         pygame.init()
#         pygame.font.init()
#         self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#         pygame.display.set_caption('Our game')
#         self.clock = pygame.time.Clock()
#         self.running = True
#         self.fps = FPS
#
#         self.all_sprites = pygame.sprite.Group()
#         self.collision_sprites = pygame.sprite.Group()
#
#         self.player = Player((400, 300), self.all_sprites)
#
#     def run(self):
#         while self.running:
#             delta_time = clock.tick(self.fps) / 1000
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 if event.type == spawn_event:
#                     x, y = random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)
#                     AnimatedAction(appear_frames, (x, y), x < player.rect.centerx, ActionType.Appear, all_sprites)
#
#             self.all_sprites.update(delta_time)
#
#             self.screen.fill('#3a2e3f')
#             self.all_sprites.draw(self.screen)
#             pygame.display.update()
#
#         pygame.quit()


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

enemy_image_size = (50, 70)

shuriken_image = pygame.image.load(join('images', 'shuriken.png')).convert_alpha()
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
# enemy_surf = pygame.transform.scale(pygame.image.load(join('images', 'zombie.png')).convert_alpha(), enemy_image_size)

appear_frames_number = 11
walk_frames_number = 10
attack_frames_number = 7
die_frames_number = 8

die_frames = [
    pygame.transform.scale(pygame.image.load(join('images', 'die', f"die_{i}.png")).convert_alpha(), enemy_image_size)
    for i in range(1, die_frames_number + 1)
]
appear_frames = [
    pygame.transform.scale(pygame.image.load(join('images', 'appear', f"appear_{i}.png")).convert_alpha(),
                           enemy_image_size)
    for i in range(1, appear_frames_number + 1)
]
walk_frames = [
    pygame.transform.scale(pygame.image.load(join('images', 'walk', f"go_{i}.png")).convert_alpha(), enemy_image_size)
    for i in range(1, walk_frames_number + 1)
]
attack_frames = [
    pygame.transform.scale(pygame.image.load(join('images', 'attack', f"hit_{i}.png")).convert_alpha(),
                           enemy_image_size)
    for i in range(1, attack_frames_number + 1)
]


def check_collisions():
    global running
    enemy_collision = pygame.sprite.spritecollide(player, enemy_sprites, False, pygame.sprite.collide_mask)
    if enemy_collision:
        for enemy in enemy_collision:
            if enemy.can_attack:
                enemy.can_attack = False
                enemy.last_time_attack = pygame.time.get_ticks()
                player.hp -= enemy.dmg
                if player.hp <= 0:
                    running = False

    for shuriken in shuriken_sprites:
        shuriken_collision = pygame.sprite.spritecollide(shuriken, enemy_sprites, False, pygame.sprite.collide_mask)
        if shuriken_collision:
            enemy = shuriken_collision[0]
            enemy.hp -= shuriken.dmg
            shuriken.kill()
            if enemy.hp <= 0:
                player.score += 10
                enemy.kill()
                AnimatedAction(die_frames, enemy.rect.center, enemy.image_direction > 0, ActionType.Die, all_sprites)


while running:
    delta_time = clock.tick(120) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == spawn_event:
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)
            AnimatedAction(appear_frames, (x, y), x < player.rect.centerx, ActionType.Appear, all_sprites)

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

# if __name__ == '__main__':
#     game = Game()
#     game.run()
