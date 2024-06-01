import pygame
class SliderButton:
    def __init__(self, x, y, width, height, value, max_value, font, font_color, background_image, slider_image,text):
        self.rect = pygame.Rect(x - width / 2, y - height / 2, width, height)
        self.value = value
        self.max_value = max_value
        self.font = font
        self.font_color = font_color
        self.background_image = pygame.transform.scale(background_image, (width, height))
        self.slider_image = pygame.transform.scale(slider_image, (60, 100))
        self.slider_rect = self.slider_image.get_rect(center=(x, y))
        self.is_dragging = False
        self.text = text

    def draw(self, surface):
        surface.blit(self.background_image, (self.rect.x, self.rect.y))
        text_surface = self.font.render(self.text, True, self.font_color)
        slider_position = self.rect.x + (self.rect.width - self.slider_image.get_width()) * (self.value / self.max_value)
        self.slider_rect.centerx = slider_position
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery-50))
        surface.blit(text_surface, text_rect)
        surface.blit(self.slider_image, self.slider_rect)
        text_surface2 = self.font.render(f"{int(self.value)}", True, self.font_color)
        text_rect2 = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface2, text_rect2)

    def check_click(self, mouse_pos):
        if self.slider_rect.collidepoint(mouse_pos):
            self.is_dragging = True
            return True
        return False

    def release(self):
        self.is_dragging = False

    def move_slider(self, mouse_x):
        if self.is_dragging:
            new_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width - self.slider_image.get_width()))
            self.slider_rect.centerx = new_x
            self.value = ((self.slider_rect.centerx - self.rect.x) / (
                        self.rect.width - self.slider_image.get_width())) * self.max_value
class DiscreteSliderButton(SliderButton):
    def __init__(self, x, y, width, height, value, options, font, font_color, background_image, slider_image, text):
        super().__init__(x, y, width, height, value, len(options)-1, font, font_color, background_image, slider_image, text)
        self.options = options
        self.value = options.index(value) if value in options else 0  # Zapewnienie, że wartość początkowa jest z listy

    def move_slider(self, mouse_x):
        if self.is_dragging:
            new_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width - self.slider_image.get_width()))
            self.slider_rect.centerx = new_x
            # Obliczenie indeksu najbliższego punktu na liście wartości
            proportional_index = (self.slider_rect.centerx - self.rect.x) / (self.rect.width - self.slider_image.get_width())
            self.value = round(proportional_index * self.max_value)
            self.value = max(0, min(self.value, self.max_value))

    def draw(self, surface):
        surface.blit(self.background_image, (self.rect.x, self.rect.y))
        text_surface = self.font.render(self.text, True, self.font_color)
        slider_position = self.rect.x + (self.rect.width - self.slider_image.get_width()) * (
                    self.value / self.max_value)
        self.slider_rect.centerx = slider_position
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - 50))
        surface.blit(text_surface, text_rect)
        surface.blit(self.slider_image, self.slider_rect)
        text_surface2 = self.font.render(f"{self.options[self.value]}", True, self.font_color)
        text_rect2 = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface2, text_rect2)

    def get_selected_value(self):
        return self.options[self.value]