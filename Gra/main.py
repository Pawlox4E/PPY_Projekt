import random

from groups import AllSprites
from player import Player
from sprites import *
from settings import *
from pytmx.util_pygame import load_pygame


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
        self.damage_indicators = []

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

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
                    hit_dmg = bullet.dmg + bullet.dmg * random.uniform(-0.5, 0.5)
                    enemy.hp -= hit_dmg
                    self.damage_indicators.append(DamageIndicator(enemy.rect.center, int(hit_dmg), self.font, self.all_sprites))
                    if enemy.hp <= 0:
                        self.player.score += 10
                        enemy.kill()
                        AnimatedAction(self.enemy_frames['zombie']['die'], enemy.rect.center, enemy.image_direction > 0,
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
            self.update_indicators(delta_time)

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


if __name__ == '__main__':
    game = Game()
    game.run()
