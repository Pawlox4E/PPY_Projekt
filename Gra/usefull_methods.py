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
def read_scores():
    """
    Odczytuje wartość z pliku;

    Parametry:
    -

    Zwraca:
    - Slowanik -  player:score
    """
    scores = {}
    with open("data/scores", 'r') as file:
        for line in file:
            player, score = line.strip().split('=')
            scores[player] = int(score)
    return scores
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
        - setting: Słownik zawierający klucze i wartości ustawień do zapisania.

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


def write_score(player, score, top_n=5):
    lastscores = read_scores()
    newscore = {player: score}
    lastscores.update(newscore)
    sorted_scores = sort_dict_by_values(lastscores, top_n, True)

    with open("data/scores", 'w') as file:
        for key, value in sorted_scores.items():
            file.write(f"{key}={value}\n")


def sort_dict_by_values(d, top_n=None, reverse=False):
    """
    Sortuje słownik po jego wartościach i zwraca N najwyższych elementów.

    Parametry:
        d (dict): Słownik do posortowania.
        top_n (int, opcjonalnie): Liczba najwyższych elementów do zwrócenia. Jeśli None, zwraca wszystkie elementy.
        reverse (bool): Jeśli True, sortowanie malejące, w przeciwnym razie rosnące.

    Zwraca:
        dict: Nowy słownik posortowany według wartości zawierający N najwyższych elementów.
    """
    sorted_items = sorted(d.items(), key=lambda item: item[1], reverse=reverse)

    if top_n is not None:
        sorted_items = sorted_items[:top_n]

    sorted_dict = {k: v for k, v in sorted_items}

    return sorted_dict
