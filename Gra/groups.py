import pygame

from usefull_methods import read_settings


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.Vector2()

    def draw(self, target_pos):
        WINDOW_WIDTH = read_settings("WIDTH")
        WINDOW_HEIGHT = read_settings("HEIGHT")
        self.offset.x = -(target_pos[0] - WINDOW_WIDTH / 2)
        self.offset.y = -(target_pos[1] - WINDOW_HEIGHT / 2)
        ground_sprites = [sprite for sprite in self if hasattr(sprite, "ground")]
        indicator_sprites = [sprite for sprite in self if hasattr(sprite, "indicator_sprite")]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, "ground") and not hasattr(sprite, "indicator_sprite")]
        for layer in [ground_sprites, object_sprites, indicator_sprites]:
            for sprite in sorted(layer, key=lambda sprite: sprite.rect.centery):
                self.screen.blit(sprite.image, sprite.rect.topleft + self.offset)
