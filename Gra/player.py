# from enum import Enum
# from os.path import join
#
# import pygame
#
# from settings import *
#
#
# class ColllisionType(Enum):
#     Horizontal = 1
#     Vertical = 2
#
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, pos, groups, collision_sprites):
#         super().__init__(groups)
#         self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
#         self.rect = self.image.get_frect(center=pos)
#         self.direction = pygame.Vector2(0, 0)
#         self.image_direction = 1  # right(1) or left(-1) direction
#         self.speed = 300
#         self.collision_sprites = collision_sprites
#         self.can_shoot = True
#         self.last_time_shoot = 0
#         self.cooldown_duration = 50
#         self.hp = 100
#         self.score = 0
#
#     def input(self):
#         keys = pygame.key.get_pressed()
#         self.direction.x = (keys[pygame.K_d] - keys[pygame.K_a]) + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
#         self.direction.y = (keys[pygame.K_s] - keys[pygame.K_w]) + (keys[pygame.K_DOWN] - keys[pygame.K_UP])
#         self.direction = self.direction.normalize() if self.direction else self.direction
#         if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and self.can_shoot:
#             Shuriken(shuriken_image, self.rect.center, (all_sprites, shuriken_sprites))
#             self.can_shoot = False
#             self.last_time_shoot = pygame.time.get_ticks()
#
#     def move(self, delta_time):
#         self.rect.x += self.direction.x * self.speed * delta_time
#         self.collision(ColllisionType.Horizontal)
#         self.rect.y += self.direction.y * self.speed * delta_time
#         self.collision(ColllisionType.Vertical)
#
#     def collision(self, direction):
#         for sprite in self.collision_sprites:
#             if sprite.rect.colliderect(self.rect)
#
#     def update(self, delta_time):
#         self.input()
#         self.move(delta_time)
#         self.check_direction()
#         self.update_shoot()
#
#     def check_direction(self):
#         if self.direction.x < 0 < self.image_direction:
#             self.image_direction = -1
#             self.image = pygame.transform.flip(self.image, True, False)
#         elif self.direction.x > 0 > self.image_direction:
#             self.image_direction = 1
#             self.image = pygame.transform.flip(self.image, True, False)
#
#     def update_shoot(self):
#         if not self.can_shoot:
#             current_time = pygame.time.get_ticks()
#             if current_time - self.last_time_shoot >= self.cooldown_duration:
#                 self.can_shoot = True
