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
    """
    Main game class for PyZombie.
    """
    def __init__(self):
        """
        Initialize the game.
        """
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        # Initialize window size and other settings from settings file
        self.WINDOW_WIDTH = read_settings("WIDTH")
        self.WINDOW_HEIGHT = read_settings("HEIGHT")
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('PyZombie')
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = read_settings("FPS")
        FontS = [0.0, 0.01, 0.02, 0.04, 0.06]
        self.font = pygame.font.Font("fonts/GloriousChristmas-BLWWB.ttf",
                                     int(math.sqrt(self.WINDOW_WIDTH * self.WINDOW_HEIGHT) * FontS[read_settings("FONT_SIZE")]))

        # Load sounds and set volumes based on settings
        self.shoot_sound = pygame.mixer.Sound(join('sounds', 'shoot.wav'))
        self.hit_sound = pygame.mixer.Sound(join('sounds', 'impact.ogg'))
        self.game_music = pygame.mixer.Sound(join('sounds', 'music.wav'))
        volume = read_settings("VOLUME") / 100
        self.game_music.set_volume(volume)
        self.shoot_sound.set_volume(volume)
        self.hit_sound.set_volume(volume)

        # Determine game difficulty level from settings
        difficulty = read_settings("DIFFICULTY")
        self.max_enemies_on_map = 20
        self.damage_indicators = []
        match difficulty:
            case 0: self.difficulty_level = DifficultyLevel.minigun
            case 1: self.difficulty_level = DifficultyLevel.m4
            case 2: self.difficulty_level = DifficultyLevel.ak
            case 3: self.difficulty_level = DifficultyLevel.pistol
            case 4: self.difficulty_level = DifficultyLevel.shotgun

        # Initialize sprite groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Initialize spawn events
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
        """
        Load images for bullets and enemies.
        """
        self.bullet_surf = pygame.transform.scale(
            pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha(), (10, 10))
        folders = list(walk(join('images', 'enemies')))[0][1] # zwraca liste podfolderow
        self.enemy_image_size = {
            'bigzombie': (100, 160),
            'fastzombie': (50, 80),
            'zombie': (70, 100)
        }
        self.enemy_frames = {}
        #przechodzi po wszystkich mozliwych enemy i laduje obrazy ich dzialan (np. walk, attack, die)
        for enemy in folders:
            self.enemy_frames[enemy] = {}
            for _, enemy_actions, _ in walk(join('images', 'enemies', enemy)):
                for action in enemy_actions:
                    for action_path, _, action_files in walk(join('images', 'enemies', enemy, action)):
                        self.enemy_frames[enemy][action] = []
                        for file in sorted(action_files, key=lambda name: name.split('.')[0]):
                            full_path = join(action_path, file)
                            surf = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(),
                                                          self.enemy_image_size[enemy])
                            self.enemy_frames[enemy][action].append(surf)

    def player_collision(self):
        """
        Handle collisions between player and enemies.
        """

        #pobiera wszystkie kolizje playera z enemy
        player_collision = pygame.sprite.spritecollide(self.player, self.enemy_sprites, False,
                                                       pygame.sprite.collide_mask)
        #jesli jest kolizja to atakujemy playera
        if player_collision:
            for enemy in player_collision:
                if enemy.can_attack:
                    enemy.can_attack = False
                    enemy.last_time_attack = pygame.time.get_ticks()
                    self.player.hp -= enemy.dmg
                    if self.player.hp <= 0: #koniec gry
                        self.running = False
                        endscreen(self.player.score)

    def bullet_collision(self):
        """
        Handle collisions between bullets and enemies.
        """

        if self.bullet_sprites:
            for bullet in self.bullet_sprites:
                collision_sprites = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False,
                                                                pygame.sprite.collide_mask)
                if collision_sprites:
                    bullet.kill()
                    enemy = collision_sprites[0] #pobiera pierwszego w ktorego trafi
                    hit_dmg = bullet.dmg + bullet.dmg * random.uniform(-0.2, 0.5) #rozrzut ataku
                    enemy.hp -= hit_dmg
                    self.hit_sound.play()
                    # dodawanie wyswietlenia ataku
                    self.damage_indicators.append(
                        DamageIndicator(enemy.rect.center, int(hit_dmg), self.font, self.all_sprites))
                    if enemy.hp <= 0:
                        enemy.kill()
                        self.player.score += 15
                        #rozne animacje umirania
                        if isinstance(enemy, BigEnemy):
                            AnimatedAction([pygame.transform.scale(frame, self.enemy_image_size['bigzombie']) for frame in
                                            self.enemy_frames['bigzombie']['die']], enemy.rect.center,
                                           enemy.image_direction > 0,
                                           ActionType.Die, self.all_sprites)
                            self.player.score += 30
                        elif isinstance(enemy, FastEnemy):
                            AnimatedAction([pygame.transform.scale(frame, self.enemy_image_size['fastzombie']) for frame in
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
        """
        Update damage indicators on screen.
        """
        for indicator in self.damage_indicators:
            indicator.update(delta_time)
            if indicator.is_expired():
                self.damage_indicators.remove(indicator)
                indicator.kill()

    # sprawdza czy jest nacisnienta spacja czy lewy przycisk myszy, jesli tak to strzela
    def input(self):
        """
        Handle player input for shooting.
        """
        mouse_pressed = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or mouse_pressed[0]) and self.player.can_shoot:
            self.shoot_sound.play()
            pos = self.gun.rect.center + self.gun.player_direction
            Bullet(self.bullet_surf, pos, self.gun.player_direction, (self.all_sprites, self.bullet_sprites), self.difficulty_level)
            self.player.can_shoot = False
            self.player.last_time_shoot = pygame.time.get_ticks()

    def update_shoot(self):
        """
        Update shooting cooldown for the player.
        """
        if not self.player.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.player.last_time_shoot >= self.player.shoot_cooldown_duration:
                self.player.can_shoot = True

    def setup(self):
        """
        Setup the game world and entities.
        """

        #Load map
        map = load_pygame(join("data", "maps", "world.tmx"))

        # Load ground tiles
        for x, y, image in map.get_layer_by_name("Ground").tiles():
            Sprite((x * read_settings("TILE_SIZE"), y * read_settings("TILE_SIZE")), image, self.all_sprites)

        # Load objects like trees and rocks
        for obj in map.get_layer_by_name("Objects"):
            CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        # Load invisible collision objects
        for obj in map.get_layer_by_name("Collisions"):
            CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        # Load entities like player and spawn positions
        for obj in map.get_layer_by_name("Entities"):
            if obj.name == "Player":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.difficulty_level)
                self.gun = Gun(self.player, self.all_sprites, self.difficulty_level)
            else:
                self.spawn_positions.append((obj.x, obj.y))

    def run(self):
        """
        Main game loop.
        """
        self.game_music.play()
        while self.running:
            delta_time = self.clock.tick(self.fps) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                #default enemy spawn
                if event.type == self.enemy_spawn_event and len(self.enemy_sprites) <= self.max_enemies_on_map:
                    Enemy(random.choice(self.spawn_positions), self.enemy_frames['zombie'],
                          (self.all_sprites, self.enemy_sprites),
                          self.player, self.collision_sprites)
                #fast enemy spawn
                if event.type == self.fast_enemy_spawn_event and len(self.enemy_sprites) <= self.max_enemies_on_map:
                    FastEnemy(random.choice(self.spawn_positions), self.enemy_frames['fastzombie'],
                              (self.all_sprites, self.enemy_sprites),
                              self.player, self.collision_sprites)
                #big enemy spawn
                if event.type == self.big_enemy_spawn_event:
                    BigEnemy(random.choice(self.spawn_positions), self.enemy_frames['bigzombie'],
                             (self.all_sprites, self.enemy_sprites),
                             self.player, self.collision_sprites)

            #updates
            self.update_shoot()
            self.input()
            self.all_sprites.update(delta_time)
            self.bullet_collision()
            self.player_collision()
            self.update_indicators(delta_time)

            #hud(fps,hp,score)
            self.screen.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            fps = self.font.render(str(int(self.clock.get_fps())), True, (255, 0, 0))
            score = self.font.render(f'score:{self.player.score}', True, (0, 0, 255))
            hp = self.font.render(f'hp:{self.player.hp}', True, (255, 0, 0))
            # max_hp = self.difficulty_level.value[4]
            # ratio = max_hp / self.player.hp
            # scale_to_100 = max_hp / 100
            # pygame.draw.rect(self.screen, "red", (self.WINDOW_WIDTH / 2 - 50, self.WINDOW_HEIGHT / 2 + 60, max_hp / scale_to_100, 20))
            # pygame.draw.rect(self.screen, "green", (self.WINDOW_WIDTH / 2 - 50, self.WINDOW_HEIGHT / 2 + 60, max_hp / scale_to_100 * ratio, 20))
            self.screen.blit(fps, (self.WINDOW_WIDTH - 60, 0))
            self.screen.blit(score, (self.WINDOW_WIDTH / 2 - 50, 0))
            self.screen.blit(hp, (self.WINDOW_WIDTH / 2 - 50, 25))
            pygame.display.update()
        self.game_music.stop()