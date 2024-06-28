import os
from enum import Enum
from os.path import join
import pygame


class CollisionType(Enum):
    """
    Enum to represent the type of collision.
    """
    Horizontal = 1
    Vertical = 2


class Player(pygame.sprite.Sprite):
    """
    Class to represent the player character.
    """
    def __init__(self, pos, groups, collision_sprites, difficulty_level):
        """
        Initialize the player.

        Parameters:
            - pos (tuple): The initial position of the player.
            - groups (list): The sprite groups the player belongs to.
            - collision_sprites (pygame.sprite.Group): The group of sprites that the player can collide with.
            - difficulty_level (DifficultyLevel): The difficulty level of the gun.
        """
        super().__init__(groups)
        self.load_imgaes()
        self.state = 'down'
        self.frame_index = 0
        self.image = pygame.image.load(join('images', 'player', 'down', '0.png')).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-60, -60)
        self.direction = pygame.Vector2(0, 0)
        self.speed = 600
        self.collision_sprites = collision_sprites
        self.hp = difficulty_level.value[4]
        self.score = 0
        self.can_shoot = True
        self.last_time_shoot = 0
        self.shoot_cooldown_duration = difficulty_level.value[3]

    def load_imgaes(self):
        """
        Load player images for different states.
        """
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        for state in self.frames.keys():
            for folder_path, subfolders, files in os.walk(join('images', 'player', state)):
                if files:
                    for file_name in sorted(files, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path)
                        self.frames[state].append(surf)

    def input(self):
        """
        Handle player input for movement.
        """
        keys = pygame.key.get_pressed()
        self.direction.x = (keys[pygame.K_d] - keys[pygame.K_a]) + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        self.direction.y = (keys[pygame.K_s] - keys[pygame.K_w]) + (keys[pygame.K_DOWN] - keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self, delta_time):
        """
        Move the player and handle collisions.

        Parameters:
        - delta_time (float): The time elapsed since the last frame.
            """
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision(CollisionType.Horizontal)
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collision(CollisionType.Vertical)
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        """
        Handle collisions with other sprites.

            Parameters:
            - direction (CollisionType): The type of collision (Horizontal or Vertical).
        """
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == CollisionType.Horizontal:
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def update(self, delta_time):
        """
        Update the player's state.

            Parameters:
            - delta_time (float): The time elapsed since the last frame.
        """
        self.input()
        self.move(delta_time)
        self.animate(delta_time)
        self.update_shoot()

    def check_direction(self):
        """
        Check and update the player's image direction based on movement.
        """
        if self.direction.x < 0 < self.image_direction:
            self.image_direction = -1
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.direction.x > 0 > self.image_direction:
            self.image_direction = 1
            self.image = pygame.transform.flip(self.image, True, False)

    def update_shoot(self):
        """
        Update the shooting cooldown.
        """
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time_shoot >= self.shoot_cooldown_duration:
                self.can_shoot = True

    def animate(self, delta_time):
        """
        Animate the player's movement.

            Parameters:
            - delta_time (float): The time elapsed since the last frame.
        """
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        self.frame_index += 5 * delta_time if self.direction else 0
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
