import random
import pygame
from enum import Enum
from os.path import join

from groups import AllSprites
from player import Player
from sprites import *
from settings import *
from pytmx.util_pygame import load_pygame


# class Player(pygame.sprite.Sprite):
#     def __init__(self, groups):
#         super().__init__(groups)
#         self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
#         self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
#         self.direction = pygame.Vector2(0, 0)
#         self.image_direction = 1  # right(1) or left(-1) direction
#         self.speed = 300
#         self.can_shoot = True
#         self.last_time_shoot = 0
#         self.cooldown_duration = 50
#         self.hp = 100
#         self.score = 0
#
#     def update_shoot(self):
#         if not self.can_shoot:
#             current_time = pygame.time.get_ticks()
#             if current_time - self.last_time_shoot >= self.cooldown_duration:
#                 self.can_shoot = True
#
#     def check_direction(self):
#         if self.direction.x < 0 < self.image_direction:
#             self.image_direction = -1
#             self.image = pygame.transform.flip(self.image, True, False)
#         elif self.direction.x > 0 > self.image_direction:
#             self.image_direction = 1
#             self.image = pygame.transform.flip(self.image, True, False)
#
#     def update(self, delta_time):
#         keys = pygame.key.get_pressed()
#         self.direction.x = (keys[pygame.K_d] - keys[pygame.K_a]) + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
#         self.direction.y = (keys[pygame.K_s] - keys[pygame.K_w]) + (keys[pygame.K_DOWN] - keys[pygame.K_UP])
#         self.direction = self.direction.normalize() if self.direction else self.direction
#         self.rect.center += self.direction * self.speed * delta_time
#         self.check_direction()
#         recent_keys = pygame.key.get_pressed()
#         if (recent_keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and self.can_shoot:
#             Shuriken(shuriken_image, self.rect.center, (all_sprites, shuriken_sprites))
#             self.can_shoot = False
#             self.last_time_shoot = pygame.time.get_ticks()
#
#         self.update_shoot()
#
#
# class Shuriken(pygame.sprite.Sprite):
#     def __init__(self, surf, pos, groups):
#         super().__init__(groups)
#         self.image = surf
#         self.rect = self.image.get_frect(center=pos)
#         mouse_pos = pygame.mouse.get_pos()
#         self.direction = pygame.Vector2(mouse_pos[0] - player.rect.center[0], mouse_pos[1] - player.rect.center[1])
#         self.direction = self.direction.normalize() if self.direction else self.direction
#         self.speed = 300
#         self.dmg = 10
#
#     def update(self, delta_time):
#         self.rect.center += self.direction * self.speed * delta_time
#         if (WINDOW_HEIGHT < self.rect.bottom or self.rect.bottom < 0
#                 or WINDOW_WIDTH < self.rect.left or self.rect.left < 0):
#             self.kill()
#
#
# class Enemy(pygame.sprite.Sprite):
#     def __init__(self, frames, pos, groups):
#         super().__init__(groups)
#         self.walk_frames = frames[0]
#         self.walk_frame_index = 0
#         self.attack_frames = frames[1]
#         self.attack_frame_index = 0
#         self.image = self.walk_frames[self.walk_frame_index]
#         self.update_animation_speed = 5
#         self.rect = self.image.get_frect(center=pos)
#         self.direction = pygame.Vector2(player.rect.center[0] - self.rect.center[0],
#                                         player.rect.center[1] - self.rect.center[1])
#         self.direction = self.direction.normalize() if self.direction else self.direction
#         self.image_direction = -1 if self.rect.centerx < player.rect.centerx else 1  # 1 to patrzy w prowa -1 to w lewo
#         if self.image_direction == 1:  # defaultowa png patrzy w lewo wiec jesli chcemy zeby bylo w prawo musimy obrocic
#             self.image = pygame.transform.flip(self.image, True, False)
#         self.speed = 10
#         self.hp = 20
#         self.can_attack = True
#         self.last_time_attack = 0
#         self.attack_cooldown = 500
#         self.dmg = 10
#
#     a
#
#
# class ActionType(Enum):
#     Appear = 1
#     Walk = 2
#     Attack = 3
#     Die = 4
#
#
# class AnimatedAction(pygame.sprite.Sprite):
#     def __init__(self, frames, pos, change_direction, action_type, groups):
#         super().__init__(groups)
#         self.frames = frames
#         self.frame_index = 0
#         self.image = self.frames[self.frame_index]
#         self.action_type = action_type
#         self.change_direction = change_direction
#         if self.change_direction:
#             self.image = pygame.transform.flip(self.frames[self.frame_index], True, False)
#         self.rect = self.image.get_frect(center=pos)
#         self.update_speed = 5
#
#     def update(self, delta_time):
#         self.frame_index += self.update_speed * delta_time
#         if self.frame_index < len(self.frames):
#             if self.change_direction:
#                 self.image = pygame.transform.flip(self.frames[int(self.frame_index)], True, False)
#             else:
#                 self.image = self.frames[int(self.frame_index)]
#         else:
#             if self.action_type == ActionType.Appear:
#                 Enemy([walk_frames, attack_frames], self.rect.center, (all_sprites, enemy_sprites))
#             self.kill()


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Our game')
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = FPS
        self.font = pygame.font.SysFont('Verdana', 15)
        self.max_enemies_on_map = 20

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # enemies spwn
        self.enemy_spawn_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_spawn_event, 300)
        self.spawn_positions = []
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.transform.scale(
            pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha(), (15, 15))
        folders = list(walk(join('images', 'enemies')))[0][1]
        enemy_image_size = (70, 100)
        self.enemy_frames = {}
        for folder in folders:
            self.enemy_frames[folder] = {}
            for folder_path, subfolders, _ in walk(join('images', 'enemies', folder)):
                for subfolder in subfolders:
                    for subfolder_path, _, files in walk(join('images', 'enemies', folder, subfolder)):
                        self.enemy_frames[folder][subfolder] = []
                        for file in sorted(files, key=lambda name: name.split('.')[0]):
                            full_path = join(subfolder_path, file)
                            surf = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(),
                                                          enemy_image_size)
                            self.enemy_frames[folder][subfolder].append(surf)


    def player_collision(self):
        player_collision = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False,
                                                       pygame.sprite.collide_mask)
        if player_collision:
            for enemy in player_collision:
                if enemy.can_attack:
                    enemy.can_attack = False
                    enemy.last_time_attack = pygame.time.get_ticks()
                    self.player.hp -= enemy.dmg
                    if self.player.hp <= 0:
                        self.running = False

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False,
                                                                pygame.sprite.collide_mask)
                if collision_sprites:
                    bullet.kill()
                    enemy = collision_sprites[0]
                    enemy.hp -= bullet.dmg
                    if enemy.hp <= 0:
                        self.player.score += 10
                        enemy.kill()
                        AnimatedAction(self.enemy_frames['zombie']['die'], enemy.rect.center, enemy.image_direction > 0,
                                       ActionType.Die, self.all_sprites)

    def input(self):
        mouse_pressed = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or mouse_pressed[0]) and self.player.can_shoot:
            pos = self.gun.rect.center + self.gun.player_direction
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites))
            self.player.can_shoot = False
            self.player.last_time_shoot = pygame.time.get_ticks()

    def update_shoot(self):
        if not self.player.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.player.last_time_shoot >= self.player.shoot_cooldown_duration:
                self.player.can_shoot = True

    def setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                self.gun = Gun(self.player, self.all_sprites)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def run(self):
        while self.running:
            delta_time = self.clock.tick(self.fps) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == self.enemy_spawn_event and len(self.enemy_sprites) <= self.max_enemies_on_map:
                    Enemy(random.choice(self.spawn_positions), self.enemy_frames['zombie'],
                          (self.all_sprites, self.enemy_sprites),
                          self.player, self.collision_sprites)

            self.update_shoot()
            self.input()
            self.all_sprites.update(delta_time)
            self.bullet_collision()
            self.player_collision()

            self.screen.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            fps = self.font.render(str(int(self.clock.get_fps())), True, (255, 0, 0))
            score = self.font.render(f'score:{self.player.score}', True, (0, 0, 255))
            hp = self.font.render(f'hp:{self.player.hp}', True, (255, 0, 0))
            self.screen.blit(fps, (WINDOW_WIDTH - 60, 0))
            self.screen.blit(score, (WINDOW_WIDTH / 2 - 50, 0))
            self.screen.blit(hp, (WINDOW_WIDTH / 2 - 50, 25))
            pygame.display.update()

        pygame.quit()


#
#
# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption('Our game')
# running = True
# clock = pygame.time.Clock()
# font = pygame.font.SysFont('Verdana', 15)
#
# spawn_event = pygame.event.custom_type()
# pygame.time.set_timer(spawn_event, 1000)
#
# all_sprites = pygame.sprite.Group()
# enemy_sprites = pygame.sprite.Group()
# shuriken_sprites = pygame.sprite.Group()
#
# player = Player(all_sprites)
#
# enemy_image_size = (50, 70)
#
# shuriken_image = pygame.image.load(join('images', 'shuriken.png')).convert_alpha()
# player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
# # enemy_surf = pygame.transform.scale(pygame.image.load(join('images', 'zombie.png')).convert_alpha(), enemy_image_size)
#
# appear_frames_number = 11
# walk_frames_number = 10
# attack_frames_number = 7
# die_frames_number = 8
#
# die_frames = [
#     pygame.transform.scale(pygame.image.load(join('images', 'die', f"die_{i}.png")).convert_alpha(), enemy_image_size)
#     for i in range(1, die_frames_number + 1)
# ]
# appear_frames = [
#     pygame.transform.scale(pygame.image.load(join('images', 'appear', f"appear_{i}.png")).convert_alpha(),
#                            enemy_image_size)
#     for i in range(1, appear_frames_number + 1)
# ]
# walk_frames = [
#     pygame.transform.scale(pygame.image.load(join('images', 'walk', f"go_{i}.png")).convert_alpha(), enemy_image_size)
#     for i in range(1, walk_frames_number + 1)
# ]
# attack_frames = [
#     pygame.transform.scale(pygame.image.load(join('images', 'attack', f"hit_{i}.png")).convert_alpha(),
#                            enemy_image_size)
#     for i in range(1, attack_frames_number + 1)
# ]
#
#
# def check_collisions():
#     global running
#     enemy_collision = pygame.sprite.spritecollide(player, enemy_sprites, False, pygame.sprite.collide_mask)
#     if enemy_collision:
#         for enemies in enemy_collision:
#             if enemies.can_attack:
#                 enemies.can_attack = False
#                 enemies.last_time_attack = pygame.time.get_ticks()
#                 player.hp -= enemies.dmg
#                 if player.hp <= 0:
#                     running = False
#
#     for shuriken in shuriken_sprites:
#         shuriken_collision = pygame.sprite.spritecollide(shuriken, enemy_sprites, False, pygame.sprite.collide_mask)
#         if shuriken_collision:
#             enemies = shuriken_collision[0]
#             enemies.hp -= shuriken.dmg
#             shuriken.kill()
#             if enemies.hp <= 0:
#                 player.score += 10
#                 enemies.kill()
#                 AnimatedAction(die_frames, enemies.rect.center, enemies.image_direction > 0, ActionType.Die, all_sprites)
#
#
# while running:
#     delta_time = clock.tick(120) / 1000
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == spawn_event:
#             x, y = random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)
#             AnimatedAction(appear_frames, (x, y), x < player.rect.centerx, ActionType.Appear, all_sprites)
#
#     screen.fill('#3a2e3f')
#     all_sprites.update(delta_time)
#     check_collisions()
#     all_sprites.draw(screen)
#
#     fps = font.render(str(int(clock.get_fps())), True, (255, 0, 0))
#     score = font.render(f'score:{player.score}', True, (0, 0, 255))
#     hp = font.render(f'hp:{player.hp}', True, (255, 0, 0))
#     screen.blit(fps, (WINDOW_WIDTH - 60, 0))
#     screen.blit(score, (WINDOW_WIDTH / 2 - 50, 0))
#     screen.blit(hp, (WINDOW_WIDTH / 2 - 50, 25))
#     pygame.display.update()
#
# pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
