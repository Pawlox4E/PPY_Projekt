import pygame
class Button:
    def __init__(self, x, y, width, height, text, font, font_color, background_image):
        self.rect = pygame.Rect(x-width/2, y-height/2, width, height)
        self.text = text
        self.font = font
        self.font_color = font_color
        self.background_image = pygame.transform.scale(background_image, (width, height))

    def draw(self, surface):
        surface.blit(self.background_image, (self.rect.x, self.rect.y))
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)