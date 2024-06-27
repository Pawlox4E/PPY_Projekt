import math
import random
import sys
from os import walk

from endscreen import endscreen
from groups import AllSprites
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame

from usefull_methods import read_settings


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        WINDOW_WIDTH = read_settings("WIDTH")
        WINDOW_HEIGHT = read_settings("HEIGHT")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('PyZombie')
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = read_settings("FPS")
        FontS = [0.0, 0.01, 0.02, 0.04, 0.06]
        self.font = pygame.font.Font("fonts/GloriousChristmas-BLWWB.ttf",
                                     int(math.sqrt(WINDOW_WIDTH * WINDOW_HEIGHT) * FontS[read_settings("FONT_SIZE")]))

        self.shoot_sound = pygame.mixer.Sound(join('sounds', 'shoot.wav'))
        volume = read_settings("VOLUME") / 100
        self.shoot_sound.set_volume(volume)
        self.hit_sound = pygame.mixer.Sound(join('sounds', 'impact.ogg'))
        self.hit_sound.set_volume(volume)

        difficulty = read_settings("DIFFICULTY")
        self.max_enemies_on_map = 20
        self.damage_indicators = []
        match difficulty:
            case 0: self.difficulty_level = DifficultyLevel.minigun
            case 1: self.difficulty_level = DifficultyLevel.m4
            case 2: self.difficulty_level = DifficultyLevel.ak
            case 3: self.difficulty_level = DifficultyLevel.pistol
            case 4: self.difficulty_level = DifficultyLevel.shotgun

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        self.enemy_spawn_event = pygame.event.custom_type()
        self.fast_enemy_spawn_event = pygame.event.custom_type()
        self.big_enemy_spawn_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_spawn_event, 300)
        pygame.time.set_timer(self.fast_enemy_spawn_event, 3000)
        pygame.time.set_timer(self.big_enemy_spawn_event, random.randint(5000, 10000))
        self.spawn_positions = []
        self.load_images()
        self.setup()

    def load_images(self):
        self.bullet_surf = pygame.transform.scale(
            pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha(), (10, 10))
        folders = list(walk(join('images', 'enemies')))[0][1]
        enemy_image_size = {
            'bigzombie': (100, 160),
            'fastzombie': (50, 80),
            'zombie': (70, 100)
        }
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
                                                          enemy_image_size[folder])
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
                        endscreen(self.player.score)

    def bullet_collision(self):
        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False,
                                                                pygame.sprite.collide_mask)
                if collision_sprites:
                    bullet.kill()
                    enemy = collision_sprites[0]
                    hit_dmg = bullet.dmg + bullet.dmg * random.uniform(-0.5, 0.5)
                    enemy.hp -= hit_dmg
                    self.hit_sound.play()
                    self.damage_indicators.append(
                        DamageIndicator(enemy.rect.center, int(hit_dmg), self.font, self.all_sprites))
                    if enemy.hp <= 0:
                        enemy.kill()
                        self.player.score += 15
                        if isinstance(enemy, BigEnemy):
                            AnimatedAction([pygame.transform.scale(frame, [100, 150]) for frame in
                                            self.enemy_frames['bigzombie']['die']], enemy.rect.center,
                                           enemy.image_direction > 0,
                                           ActionType.Die, self.all_sprites)
                            self.player.score += 15
                        elif isinstance(enemy, FastEnemy):
                            AnimatedAction([pygame.transform.scale(frame, [30, 50]) for frame in
                                            self.enemy_frames['fastzombie']['die']],
                                           enemy.rect.center,
                                           enemy.image_direction > 0,
                                           ActionType.Die, self.all_sprites)
                            self.player.score += 15
                        elif isinstance(enemy, Enemy):
                            AnimatedAction(self.enemy_frames['zombie']['die'], enemy.rect.center,
                                           enemy.image_direction > 0,
                                           ActionType.Die, self.all_sprites)

    def update_indicators(self, delta_time):
        for indicator in self.damage_indicators:
            indicator.update(delta_time)
            if indicator.is_expired():
                self.damage_indicators.remove(indicator)
                indicator.kill()

    def input(self):
        mouse_pressed = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or mouse_pressed[0]) and self.player.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites), self.difficulty_level)
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
            Sprite((x * read_settings("TILE_SIZE"), y * read_settings("TILE_SIZE")), image, self.all_sprites)

        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.difficulty_level)
                self.gun = Gun(self.player, self.all_sprites, self.difficulty_level)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def run(self):
        while self.running:
            delta_time = self.clock.tick(self.fps) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == self.enemy_spawn_event and len(self.enemy_sprites) <= self.max_enemies_on_map:
                    Enemy(random.choice(self.spawn_positions), self.enemy_frames['zombie'],
                          (self.all_sprites, self.enemy_sprites),
                          self.player, self.collision_sprites)
                if event.type == self.fast_enemy_spawn_event and len(self.enemy_sprites) <= self.max_enemies_on_map:
                    FastEnemy(random.choice(self.spawn_positions), self.enemy_frames['fastzombie'],
                              (self.all_sprites, self.enemy_sprites),
                              self.player, self.collision_sprites)
                if event.type == self.big_enemy_spawn_event:
                    BigEnemy(random.choice(self.spawn_positions), self.enemy_frames['bigzombie'],
                             (self.all_sprites, self.enemy_sprites),
                             self.player, self.collision_sprites)

            self.update_shoot()
            self.input()
            self.all_sprites.update(delta_time)
            self.bullet_collision()
            self.player_collision()
            self.update_indicators(delta_time)

            self.screen.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            fps = self.font.render(str(int(self.clock.get_fps())), True, (255, 0, 0))
            score = self.font.render(f'score:{self.player.score}', True, (0, 0, 255))
            hp = self.font.render(f'hp:{self.player.hp}', True, (255, 0, 0))
            WINDOW_WIDTH = read_settings("WIDTH")
            self.screen.blit(fps, (WINDOW_WIDTH - 60, 0))
            self.screen.blit(score, (WINDOW_WIDTH / 2 - 50, 0))
            self.screen.blit(hp, (WINDOW_WIDTH / 2 - 50, 25))
            pygame.display.update()
