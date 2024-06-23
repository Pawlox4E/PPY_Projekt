import pygame

from usefull_methods import read_settings


class Button:
    """
    Klasa reprezentująca przycisk w grze.

    Attributes:
        rect (pygame.Rect): Prostokąt definiujący pozycję i rozmiar przycisku.
        text (str): Tekst wyświetlany na przycisku.
        font (pygame.font.Font): Font używany do renderowania tekstu.
        font_color (tuple): Kolor tekstu (RGB tuple).
        background_image (pygame.Surface): Tło przycisku.
        click_sound (pygame.mixer.Sound): Dźwięk kliknięcia przycisku.

    Methods:
        draw(surface):
            Metoda rysująca przycisk na danej powierzchni.

        check_click(mouse_pos) -> bool:
            Metoda sprawdzająca, czy pozycja kliknięcia myszy znajduje się w granicach przycisku i odtwarzająca dźwięk.
    """

    def __init__(self, x, y, width, height, text, font, font_color, background_image):
        """
        Inicjalizuje obiekt przycisku.

        Args:
            x (int): Pozycja x środka przycisku.
            y (int): Pozycja y środka przycisku.
            width (int): Szerokość przycisku.
            height (int): Wysokość przycisku.
            text (str): Tekst wyświetlany na przycisku.
            font (pygame.font.Font): Font używany do renderowania tekstu.
            font_color (tuple): Kolor tekstu (RGB tuple).
            background_image (pygame.Surface): Tło przycisku.
        """
        self.rect = pygame.Rect(x - width/2, y - height/2, width, height)
        self.text = text
        self.font = font
        self.font_color = font_color
        self.background_image = pygame.transform.scale(background_image, (width, height))

        # Załaduj dźwięk kliknięcia
        self.click_sound = pygame.mixer.Sound("sounds/menu_click2.wav")
        self.click_sound.set_volume(read_settings("VOLUME") / 100)

    def draw(self, surface):
        """
        Rysuje przycisk na danej powierzchni.

        Args:
            surface (pygame.Surface): Powierzchnia, na której ma zostać narysowany przycisk.
        """
        surface.blit(self.background_image, (self.rect.x, self.rect.y))
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, mouse_pos):
        """
        Sprawdza, czy pozycja kliknięcia myszy znajduje się w granicach przycisku
        i odtwarza dźwięk kliknięcia.

        Args:
            mouse_pos (tuple): Pozycja kliknięcia myszy (x, y).

        Returns:
            bool: True, jeśli kliknięcie myszy jest w granicach przycisku, False w przeciwnym razie.
        """
        if self.rect.collidepoint(mouse_pos):
            self.click_sound.play()  # Odtwórz dźwięk kliknięcia
            return True
        return False
