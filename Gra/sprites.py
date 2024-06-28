from enum import Enum
from os.path import join

import pygame

from player import CollisionType
from math import atan2, degrees

from usefull_methods import read_settings


class Sprite(pygame.sprite.Sprite):
    """A basic sprite class for displaying images."""
    def __init__(self, pos, surf, groups):
        """Initialize the sprite.

        Args:
            pos (tuple): The position to place the sprite.
            surf (pygame.Surface): The surface to display for the sprite.
            groups (list): The sprite groups this sprite belongs to.
        """
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True


class CollisionSprite(pygame.sprite.Sprite):
    """A sprite class specifically for handling collisions."""
    def __init__(self, pos, surf, groups):
        """Initialize the collision sprite.

        Args:
            pos (tuple): The position to place the sprite.
            surf (pygame.Surface): The surface to display for the sprite.
            groups (list): The sprite groups this sprite belongs to.
        """
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class DifficultyLevel(Enum):
    """An enumeration of different difficulty levels with associated attributes."""
    # image | dmg | bullet_speed | reload_cooldown | max player hp
    pistol = ('gun.png', 10, 500, 300, 150)
    ak = ('ak.png', 15, 600, 200, 200)
    m4 = ('m4.png', 10, 800, 100, 250)
    shotgun = ('shotgun.png', 30, 500, 800, 100)
    minigun = ('minigun.png', 50, 800, 50, 300)

class Gun(pygame.sprite.Sprite):
    """A sprite class representing a gun."""
    def __init__(self, player, groups, difficulty_level):
        """Initialize the gun.

        Args:
            player (Player): The player using the gun.
            groups (list): The sprite groups this sprite belongs to.
            difficulty_level (DifficultyLevel): The difficulty level of the gun.
        """
        self.player = player
        self.distance = 70
        self.player_direction = pygame.Vector2(1, 0)

        super().__init__(groups)
        self.gun_surf = pygame.transform.scale(pygame.image.load(join('images', 'gun', difficulty_level.value[0])).convert_alpha(),
                                               (100, 50))
        self.image = self.gun_surf
        self.rect = self.image.get_frect(center=self.player.rect.center + self.player_direction * self.distance)

    # ustawia kierunek do myszki
    def get_direction(self):
        """Update the direction of the gun to point towards the mouse."""
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        player_pos = pygame.Vector2(read_settings("WIDTH") / 2, read_settings("HEIGHT") / 2)
        self.player_direction = (mouse_pos - player_pos).normalize() if self.player_direction else self.player_direction

    #obraca obrazek broni
    def rotate_gun(self):
        """Rotate the gun image based on the player's direction."""
        angle = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pygame.transform.rotozoom(self.gun_surf, angle, 1)
        else:
            self.image = pygame.transform.rotozoom(self.gun_surf, abs(angle), 1)
            self.image = pygame.transform.flip(self.image, False, True)

    def update(self, _):
        """Update the gun's direction and position."""
        self.get_direction()
        self.rotate_gun()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance


class Bullet(pygame.sprite.Sprite):
    """A sprite class representing a bullet."""
    def __init__(self, surf, pos, direction, groups, gun_type):
        """Initialize the bullet.

        Args:
            surf (pygame.Surface): The surface to display for the bullet.
            pos (tuple): The position to place the bullet.
            direction (pygame.Vector2): The direction the bullet will travel.
            groups (list): The sprite groups this sprite belongs to.
            gun_type (DifficultyLevel): The type of gun firing the bullet.
        """
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.direction = direction
        self.speed = gun_type.value[2]
        self.spawn_time = pygame.time.get_ticks()
        self.life_time = 1000
        self.dmg = gun_type.value[1]

    def update(self, delta_time):
        """Update the bullet's position and check its lifetime.

        Args:
            delta_time (float): The time since the last update.
        """
        self.rect.center += self.direction * self.speed * delta_time
        if pygame.time.get_ticks() - self.spawn_time >= self.life_time:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """A sprite class representing an enemy."""
    def __init__(self, pos, frames, groups, player, collision_sprites):
        """Initialize the enemy.

         Args:
             pos (tuple): The position to place the enemy.
             frames (dict): The animation frames for the enemy.
             groups (list): The sprite groups this sprite belongs to.
             player (Player): The player the enemy is targeting.
             collision_sprites (list): The sprites to check for collisions.
         """
        super().__init__(groups)
        self.player = player
        self.frames = frames
        self.walk_frame_index = 0
        self.attack_frame_index = 0
        self.image = self.frames['walk'][self.walk_frame_index]
        self.animation_speed = 5
        self.rect = self.image.get_frect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 100

        self.direction = pygame.Vector2(player.rect.center[0] - self.rect.center[0],
                                        player.rect.center[1] - self.rect.center[1])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.image_direction = -1 if self.rect.centerx < player.rect.centerx else 1  # 1 to patrzy w prowa -1 to w lewo
        if self.image_direction == 1:  # defaultowa png patrzy w lewo wiec jesli chcemy zeby bylo w prawo musimy obrocic
            self.image = pygame.transform.flip(self.image, True, False)
        self.hp = 25
        self.can_attack = True
        self.last_time_attack = 0
        self.attack_cooldown = 500
        self.dmg = 10

    def move(self, delta_time):
        """Move the enemy towards the player.

        Args:
            delta_time (float): The time since the last update.
        """
        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        self.direction = (player_pos - enemy_pos).normalize() if self.direction else (player_pos - enemy_pos)
        self.hitbox_rect.x += self.direction.x * self.speed * delta_time
        self.collision(CollisionType.Horizontal)
        self.hitbox_rect.y += self.direction.y * self.speed * delta_time
        self.collision(CollisionType.Vertical)
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        """Handle collisions with other sprites.

        Args:
            direction (CollisionType): The direction of the collision.
        """
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == CollisionType.Horizontal:
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def update_attack(self, delta_time):
        """Update the enemy's attack state.

        Args:
            delta_time (float): The time since the last update.
        """
        if not self.can_attack:
            self.update_attack_frames(delta_time)
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time_attack >= self.attack_cooldown:
                self.can_attack = True

    # ustawia poprawny kierunek do playera (zeby patrzyli na niego)
    def check_direction(self):
        """Check and update the enemy's direction to face the player."""
        if self.direction.x < 0 < self.image_direction:
            self.image_direction = -1
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.direction.x > 0 > self.image_direction:
            self.image_direction = 1
            self.image = pygame.transform.flip(self.image, True, False)

    # animuje chodzenie
    def update_walk(self, delta_time):
        """Animate the enemy's walking state.

        Args:
            delta_time (float): The time since the last update.
        """
        self.walk_frame_index += self.animation_speed * delta_time
        self.image = self.frames['walk'][int(self.walk_frame_index) % len(self.frames['walk'])]
        if self.image_direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    # animuje atak
    def update_attack_frames(self, delta_time):
        """Animate the enemy's attack state.

        Args:
            delta_time (float): The time since the last update.
        """
        self.attack_frame_index += self.animation_speed * delta_time
        self.image = self.frames['attack'][int(self.attack_frame_index) % len(self.frames['attack'])]
        if self.image_direction == 1:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, delta_time):
        """Update the enemy's state.

        Args:
            delta_time (float): The time since the last update.
        """
        self.hp += 1 * delta_time if pygame.time.get_ticks() > 500 else 0
        self.move(delta_time)
        self.update_walk(delta_time)
        self.check_direction()
        self.update_attack(delta_time)


class ActionType(Enum):
    """An enumeration of different action types for animations."""
    Appear = 1
    Walk = 2
    Attack = 3
    Die = 4


class AnimatedAction(pygame.sprite.Sprite):
    """A sprite class for animated actions."""
    def __init__(self, frames, pos, change_direction, action_type, groups):
        """Initialize the animated action.

        Args:
            frames (list): The frames for the animation.
            pos (tuple): The position to place the animation.
            change_direction (bool): Whether the animation should change direction.
            action_type (ActionType): The type of action being animated.
            groups (list): The sprite groups this sprite belongs to.
        """
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

    # animuje podane frejmy
    def update(self, delta_time):
        """Animate the frames.

        Args:
            delta_time (float): The time since the last update.
        """
        self.frame_index += self.update_speed * delta_time
        if self.frame_index < len(self.frames):
            if self.change_direction:
                self.image = pygame.transform.flip(self.frames[int(self.frame_index)], True, False)
            else:
                self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()


class DefaultEnemy(Enemy):
    """A default enemy class."""
    def __init__(self, pos, frames, groups, player, collision_sprites):
        """Initialize the default enemy.

        Args:
            pos (tuple): The position to place the enemy.
            frames (dict): The animation frames for the enemy.
            groups (list): The sprite groups this sprite belongs to.
            player (Player): The player the enemy is targeting.
            collision_sprites (list): The sprites to check for collisions.
        """
        super().__init__(pos, frames, groups, player, collision_sprites)


class FastEnemy(Enemy):
    """A fast enemy class with higher speed and lower health."""
    def __init__(self, pos, frames, groups, player, collision_sprites):
        """Initialize the fast enemy.

        Args:
            pos (tuple): The position to place the enemy.
            frames (dict): The animation frames for the enemy.
            groups (list): The sprite groups this sprite belongs to.
            player (Player): The player the enemy is targeting.
            collision_sprites (list): The sprites to check for collisions.
        """
        super().__init__(pos, frames, groups, player, collision_sprites)
        self.speed = 200
        self.hp = 15
        self.attack_cooldown = 200
        self.dmg = 4


class BigEnemy(Enemy):
    """A big enemy class with lower speed and higher health."""
    def __init__(self, pos, frames, groups, player, collision_sprites):
        """Initialize the big enemy.

        Args:
            pos (tuple): The position to place the enemy.
            frames (dict): The animation frames for the enemy.
            groups (list): The sprite groups this sprite belongs to.
            player (Player): The player the enemy is targeting.
            collision_sprites (list): The sprites to check for collisions.
        """
        super().__init__(pos, frames, groups, player, collision_sprites)
        self.speed = 50
        self.hp = 55
        self.attack_cooldown = 800
        self.dmg = 22


class DamageIndicator(pygame.sprite.Sprite):
    """A sprite class for displaying damage indicators."""
    def __init__(self, pos, damage, font, groups):
        """Initialize the damage indicator.

        Args:
            pos (tuple): The position to place the indicator.
            damage (int): The amount of damage to display.
            font (pygame.font.Font): The font to use for the indicator.
            groups (list): The sprite groups this sprite belongs to.
        """
        super().__init__(groups)
        self.image = font.render(str(damage), True, (255, 0, 0))
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.duration = 1000
        self.indicator_sprite = True

    def update(self, delta_time):
        """Update the position of the damage indicator.

        Args:
            delta_time (float): The time since the last update.
        """
        # Przesuwaj wskaźnik w górę
        self.rect.y -= 1

    def is_expired(self):
        """Check if the indicator has expired.

        Returns:
            bool: True if the indicator has expired, False otherwise.
        """
        return pygame.time.get_ticks() - self.start_time > self.duration
