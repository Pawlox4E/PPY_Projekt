def read_settings(key):
    """
    Odczytuje wartość z pliku ustawień na podstawie podanego klucza.

    Parametry:
    - key: Klucz (nazwa ustawienia) do odczytania z pliku ustawień.

    Zwraca:
    - Wartość ustawienia jako int, jeśli klucz został znaleziony, w przeciwnym razie None.
    """
    with open("data/settings", 'r') as file:
        for line in file:
            if line.startswith(key):
                _, value = line.split('=')
                return int(value.strip())
    return None

def save_settings_to_file(settings):
    """
    Zapisuje aktualne ustawienia do pliku "data/settings".

    Parametry:
    - settings: Słownik zawierający klucze i wartości ustawień do zapisania.

    Zwraca:
    - None
    """
    with open("data/settings", 'w') as file:
        for key, value in settings.items():
            file.write(f"{key}={value}\n")
def save_setting(setting):
    """
        Zapisuje aktualne ustawienia do pliku "data/settings".

        Parametry:
        - settings: Słownik zawierający klucze i wartości ustawień do zapisania.

        Zwraca:
        - None
        """
    settings = {
        "VOLUME": read_settings("VOLUME"),
        "BRIGHTNESS": read_settings("BRIGHTNESS"),
        "FONT_SIZE": read_settings("FONT_SIZE"),
        "FPS": read_settings("FPS"),
        "WIDTH": read_settings("WIDTH"),
        "HEIGHT": read_settings("HEIGHT"),
        "TILE_SIZE": read_settings("TILE_SIZE"),
        "DIFFICULTY": read_settings("DIFFICULTY")
    }
    settings.update(setting)

    with open("data/settings", 'w') as file:
        for key, value in settings.items():
            file.write(f"{key}={value}\n")