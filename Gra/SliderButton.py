import pygame

from usefull_methods import read_settings

class SliderButton:
    """
    Klasa reprezentująca przycisk suwaka w grze.

    Attributes:
        rect (pygame.Rect): Prostokąt definiujący pozycję i rozmiar przycisku.
        value (float): Aktualna wartość suwaka.
        max_value (float): Maksymalna wartość suwaka.
        font (pygame.font.Font): Font używany do renderowania tekstu.
        font_color (tuple): Kolor tekstu (RGB tuple).
        background_image (pygame.Surface): Tło przycisku.
        slider_image (pygame.Surface): Grafika suwaka.
        slider_rect (pygame.Rect): Prostokąt określający pozycję suwaka.
        is_dragging (bool): Flaga określająca, czy suwak jest przeciągany.
        text (str): Tekst wyświetlany obok suwaka.

    Methods:
        draw(surface):
            Metoda rysująca przycisk suwaka na danej powierzchni.

        check_click(mouse_pos) -> bool:
            Metoda sprawdzająca, czy pozycja kliknięcia myszy znajduje się w granicach przycisku suwaka.

        release():
            Metoda zatrzymująca przeciąganie suwaka.

        move_slider(mouse_x):
            Metoda przemieszczająca suwak w odpowiedzi na ruch myszy.
    """

    def __init__(self, x, y, width, height, value, max_value, font, font_color, background_image, slider_image, text):
        """
        Inicjalizuje obiekt przycisku suwaka.

        Args:
            x (int): Pozycja x środka przycisku.
            y (int): Pozycja y środka przycisku.
            width (int): Szerokość przycisku.
            height (int): Wysokość przycisku.
            value (float): Początkowa wartość suwaka.
            max_value (float): Maksymalna wartość suwaka.
            font (pygame.font.Font): Font używany do renderowania tekstu.
            font_color (tuple): Kolor tekstu (RGB tuple).
            background_image (pygame.Surface): Tło przycisku.
            slider_image (pygame.Surface): Grafika suwaka.
            text (str): Tekst wyświetlany obok suwaka.
        """
        self.rect = pygame.Rect(x - width / 2, y - height / 2, width, height)
        self.value = value
        self.max_value = max_value
        self.font = font
        self.font_color = font_color
        self.background_image = pygame.transform.scale(background_image, (width, height))
        self.slider_image = pygame.transform.scale(slider_image, (width/10, height))
        self.slider_rect = self.slider_image.get_rect(center=(x, y))
        self.is_dragging = False
        self.text = text
        self.click_sound = pygame.mixer.Sound("sounds/menu_click2.wav")
        self.click_sound.set_volume(read_settings("VOLUME")/100)

    def draw(self, surface):
        """
        Rysuje przycisk suwaka na danej powierzchni.

        Args:
            surface (pygame.Surface): Powierzchnia, na której ma zostać narysowany suwak.
        """
        surface.blit(self.background_image, (self.rect.x, self.rect.y))
        text_surface = self.font.render(self.text, True, self.font_color)
        slider_position = (self.rect.x+self.rect.width/25) + (self.rect.width - self.slider_image.get_width()) * (self.value / self.max_value)
        self.slider_rect.centerx = slider_position
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - self.rect.height / 2))
        surface.blit(text_surface, text_rect)
        surface.blit(self.slider_image, self.slider_rect)
        text_surface2 = self.font.render(f"{int(self.value)}", True, self.font_color)
        text_rect2 = text_surface2.get_rect(center=self.rect.center)
        surface.blit(text_surface2, text_rect2)

    def check_click(self, mouse_pos):
        """
        Sprawdza, czy pozycja kliknięcia myszy znajduje się w granicach przycisku suwaka.

        Args:
            mouse_pos (tuple): Pozycja kliknięcia myszy (x, y).

        Returns:
            bool: True, jeśli kliknięcie myszy jest w granicach suwaka, False w przeciwnym razie.
        """
        if self.slider_rect.collidepoint(mouse_pos):
            self.click_sound.play()
            self.is_dragging = True
            return True
        return False

    def release(self):
        """
        Zatrzymuje przeciąganie suwaka.
        """
        self.is_dragging = False

    def move_slider(self, mouse_x):
        """
        Przemieszcza suwak w odpowiedzi na ruch myszy.

        Args:
            mouse_x (int): Pozycja x myszy.
        """
        if self.is_dragging:
            new_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width - self.slider_image.get_width()))
            self.slider_rect.centerx = new_x
            self.value = ((self.slider_rect.centerx - self.rect.x) / (self.rect.width - self.slider_image.get_width())) * self.max_value

    def get_selected_value(self):
        """
        Zwraca aktualnie wybraną wartość suwaka (opcję z listy).

        Returns:
            Any: Aktualnie wybrana wartość suwaka (opcja z listy).
        """
        return self.value


class DiscreteSliderButton(SliderButton):
    """
    Klasa reprezentująca dyskretny przycisk suwaka.

    Rozszerza klasę SliderButton.

    Attributes:
        options (list): Lista opcji dostępnych dla suwaka.

    Methods:
        move_slider(mouse_x):
            Przesuwa suwak na podstawie ruchu myszy, wybierając najbliższą opcję z listy.

        draw(surface):
            Rysuje przycisk suwaka dyskretnego na danej powierzchni.

        get_selected_value() -> Any:
            Zwraca aktualnie wybraną wartość suwaka (opcję z listy).
    """

    def __init__(self, x, y, width, height, value, options, font, font_color, background_image, slider_image, text):
        """
        Inicjalizuje obiekt przycisku suwaka dyskretnego.

        Args:
            x (int): Pozycja x środka przycisku.
            y (int): Pozycja y środka przycisku.
            width (int): Szerokość przycisku.
            height (int): Wysokość przycisku.
            value (Any): Początkowa wartość suwaka (opcja z listy).
            options (list): Lista dostępnych opcji suwaka.
            font (pygame.font.Font): Font używany do renderowania tekstu.
            font_color (tuple): Kolor tekstu (RGB tuple).
            background_image (pygame.Surface): Tło przycisku.
            slider_image (pygame.Surface): Grafika suwaka.
            text (str): Tekst wyświetlany obok suwaka.
        """
        super().__init__(x, y, width, height, value, len(options) - 1, font, font_color, background_image, slider_image, text)
        self.options = options
        self.value = options.index(value) if value in options else 0  # Zapewnienie, że wartość początkowa jest z listy
        self.click_sound = pygame.mixer.Sound("sounds/menu_click2.wav")
        self.click_sound.set_volume(read_settings("VOLUME") / 100)

    def move_slider(self, mouse_x):
        """
        Przesuwa suwak na podstawie ruchu myszy, wybierając najbliższą opcję z listy.

        Args:
            mouse_x (int): Pozycja x myszy.
        """
        if self.is_dragging:
            new_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width - self.slider_image.get_width()))
            self.slider_rect.centerx = new_x
            # Obliczenie indeksu najbliższego punktu na liście wartości
            proportional_index = (self.slider_rect.centerx - self.rect.x) / (self.rect.width - self.slider_image.get_width())
            self.value = round(proportional_index * self.max_value)
            self.value = max(0, min(self.value, self.max_value))

    def draw(self, surface):
        """
        Rysuje przycisk suwaka dyskretnego na danej powierzchni.

        Args:
            surface (pygame.Surface): Powierzchnia, na której ma zostać narysowany suwak.
        """
        surface.blit(self.background_image, (self.rect.x, self.rect.y))
        text_surface = self.font.render(self.text, True, self.font_color)
        slider_position = (self.rect.x+self.rect.width/25) + (self.rect.width - self.slider_image.get_width()) * (self.value / self.max_value)
        self.slider_rect.centerx = slider_position
        text_rect = text_surface.get_rect(center=(self.rect.centerx, self.rect.centery - self.rect.height / 2))
        surface.blit(text_surface, text_rect)
        surface.blit(self.slider_image, self.slider_rect)
        text_surface2 = self.font.render(f"{self.options[self.value]}", True, self.font_color)
        text_rect2 = text_surface2.get_rect(center=self.rect.center)
        surface.blit(text_surface2, text_rect2)

    def get_selected_value(self):
        """
        Zwraca aktualnie wybraną wartość suwaka (opcję z listy).

        Returns:
            Any: Aktualnie wybrana wartość suwaka (opcja z listy).
        """
        return self.options[self.value]


class LinkedDiscreteSliderButton(DiscreteSliderButton):
    """
    Klasa reprezentująca połączone suwaki dyskretne, które synchronizują swoje wartości.
    """
    def __init__(self, x, y, width, height, value, options, font, font_color, background_image, slider_image, text, linked_slider=None):
        super().__init__(x, y, width, height, value, options, font, font_color, background_image, slider_image, text)
        self.linked_slider = linked_slider

    def move_slider(self, mouse_x):
        super().move_slider(mouse_x)
        if self.linked_slider:
            self.linked_slider.set_value(self.value)

    def set_value(self, value):
        """
        Ustawia wartość suwaka i przesuwa go do odpowiedniej pozycji.
        """
        self.value = value
        slider_position = self.rect.x + (self.rect.width - self.slider_image.get_width()) * (self.value / self.max_value)
        self.slider_rect.centerx = slider_position

    def link(self, slider):
        self.linked_slider = slider
