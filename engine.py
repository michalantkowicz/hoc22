"""
Zestaw metod niezbędnych do utworzenia własnej gry.
"""

import random
from enum import Enum

import pygame
import pygame.freetype

from collectible import createCollectibles
from enemy import createEnemy
from image import Image
from map import createMap
from obstacle import createObstacle
from player import createPlayer

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_CENTER = [SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0]

MAP_VALID_WIDTH = (2, 8)
MAP_VALID_HEIGHT = (2, 6)

MAP_CONFIG = {}
MAP_POSITIONS = []
PLAYER_CONFIGS = []
ENEMY_CONFIGS = []
OBSTACLE_CONFIGS = []
COLLECTIBLE_CONFIGS = []

SCORE = 0
TARGET_SCORE = 1

GAME_OVER = False
WIN = False

clock = pygame.time.Clock()

players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()


class Obrazek(Enum):
    RYCERZ = "resources/player.png"
    SMOK = "resources/enemy.png"
    SKRZYNIA = "resources/crates.png"
    GWIAZDKA = "resources/star.png"


def stworz_mape(rozmiar=()):
    """
    **Przykłady użycia**

        stworz_mape()
        stworz_mape(rozmiar=(2,2))
        stworz_mape(rozmiar=(4,5))

    **Opis**

    Tworzy mapę o podanej ilości pól w poziomie i pionie.

    Mapa nie może być mniejsza niż 2x2 ani większa niż 6x8 pól.

    Metodę należy wywołać jeden raz. Drugie wywołanie spowoduje zwrócenie błędu (patrz: **Zwracane błędy**).

    ---

    Pola mapy numerowane są następująco:

        +---+---+---+
        |0,0|1,0|2,0|
        +---+---+---+
        |0,1|1,1|2,1|
        +---+---+---+
        |0,2|1,2|2,2|
        +---+---+---+

    **Parametry**

    - **rozmiar** _(opcjonalny)_ - liczba pól w poziomie
        - wartość minimalna: **(2,2)**
        - wartość maksymalna: **(6,8)**
        - wartość domyślna: **())** (program wylosuje rozmiar mapy: szerokość 2-8 pól, wysokość: 2-6 pól)

    **Zwracane błędy**

    - **RuntimeError**
        - _"Map width must be within (2,8) and height must be within (2,6)"_ - Podano nieprawidłowe wymiary mapy
        - _"Map was already created!"_ - Mapa została już wcześniej utworzona
    """
    if len(rozmiar) == 0:
        rozmiar = (
            random.randint(MAP_VALID_WIDTH[0], MAP_VALID_WIDTH[1]),
            random.randint(MAP_VALID_HEIGHT[0], MAP_VALID_HEIGHT[1])
        )
    __create_map(rozmiar[0], rozmiar[1])


def uruchom_gre():
    """
    **Przykłady użycia**

        uruchom_gre()

    **Opis**
    Uruchamia grę. Bez wywołania tej metody gra nie zostanie wyświetlona.
    """
    __run_game()


def dodaj_bohatera(awatar=Obrazek.RYCERZ, pozycja=()):
    """
    **Przykłady użycia**

        dodaj_bohatera()
        dodaj_bohatera(awatar=Obrazek.RYCERZ, pozycja=(2,2))
        dodaj_bohatera(pozycja=(4,5))

    **Opis**
    Ustawia na mapie bohatera, który może być kontrolowany za pomocą strzałek.

    Bohater reprezentowany jest za pomocą obrazka podanego przez użytkownika.


    **Parametry**

    - **awatar** _(opcjonalny)_ - obrazek, który będzie reprezentował bohatera
        - dopuszczalne wartości:
            - Obrazek.RYCERZ
    - **pozycja** _(opcjonalny)_ - numer pola w poziomie, na którym ustawiony zostanie bohater
        - wartość minimalna: **(0, 0)**
        - wartość maksymalna: zależy od wielkości mapy - np (4,4) dla mapy 4x4
        - wartość domyślna: **()** (program wylosuje pole)
    """
    if len(pozycja) == 0:
        pozycja = MAP_POSITIONS.pop(0)
    __create_player(awatar.value, pozycja[0], pozycja[1])


def dodaj_przeciwnika(awatar=Obrazek.SMOK, pozycja=(), predkosc=1):
    """
    **Przykłady użycia**

        dodaj_przeciwnika()
        dodaj_przeciwnika(awatar=Obrazek.SMOK, pozycja=(2,2), predkosc=3)
        dodaj_przeciwnika(pozycja=(4,5))
        dodaj_przeciwnika(predkosc=5)

    **Opis**
    Ustawia na mapie przeciwnika, który porusza się losowo.

    Jeśli przeciwnik złapie bohatera to gra kończy się przegraną.

    Prędkość może przyjąć jedną z pięciu wartości:

    - **1** (przeciwnik porusza się znacznie wolniej od bohatera)
    - **2** (przeciwnik porusza się wolniej od bohatera)
    - **3** (przeciwnik porusza się z taką prędkością jak bohater)
    - **4** (przeciwnik porusza się szybciej od bohatera)
    - **5** (przeciwnik porusza się znacznie szybciej od bohatera)

    lub **0** - przeciwnik będzie stał w miejscu.

    **Parametry**

    - **awatar** _(opcjonalny)_ - obrazek, który będzie reprezentował bohatera
        - dopuszczalne wartości:
            - Obrazek.SMOK
        - wartość domyślna: **Obrazek.SMOK**
    - **pozycja** _(opcjonalny)_ - numer pola w poziomie, na którym ustawiony zostanie przeciwnik
        - wartość minimalna: **(0, 0)**
        - wartość maksymalna: zależy od wielkości mapy - np (4,4) dla mapy 4x4
        - wartość domyślna: **()** (program wylosuje pole)
    - **predkosc** _(opcjonalny)_ - prędkość z jaką poruszał się będzie przeciwnik
        - wartość minimalna: **0**
        - wartość maksymalna: **5**
        - wartość domyślna: **1**

    **Zwracane błędy**

    - **RuntimeError**
        - _"Speed is invalid. Should be in range 0-5."_ - Podano nieprawidłową **predkosc**
    """
    if len(pozycja) == 0:
        pozycja = MAP_POSITIONS.pop(0)
    if predkosc < 0 or predkosc > 5:
        raise RuntimeError("Speed is invalid. Should be in range 0-5.")
    __create_enemy(awatar.value, pozycja[0], pozycja[1], predkosc)


def dodaj_przeszkode(awatar=Obrazek.SKRZYNIA, pozycja=()):
    """
    **Przykłady użycia**

        dodaj_przeszkode()
        dodaj_przeszkode(awatar=Obrazek.SKRZYNIA, pozycja=(2,2))
        dodaj_przeszkode(pozycja=(4,5))

    **Opis**
    Ustawia na mapie nieruchomą przeszkodę.

    Pole z przeszkodą jest nieosiągalne dla bohaterów i przeciwników.

    **Parametry**

    - **awatar** _(opcjonalny)_ - obrazek, który będzie reprezentował przeszkodę
        - dopuszczalne wartości:
            - Obrazek.SKRZYNIA
        - wartość domyślna: **Obrazek.SKRZYNIA**
    - **pozycja** _(opcjonalny)_ - numer pola w poziomie, na którym ustawiona zostanie przeszkoda
        - wartość minimalna: **(0, 0)**
        - wartość maksymalna: zależy od wielkości mapy - np (4,4) dla mapy 4x4
        - wartość domyślna: **()** (program wylosuje pole)
    """
    if len(pozycja) == 0:
        pozycja = MAP_POSITIONS.pop(0)
    __create_obstacle(awatar.value, pozycja[0], pozycja[1])


def dodaj_skarb(awatar=Obrazek.GWIAZDKA, pozycja=(), punkty=1):
    """
    **Przykłady użycia**

        dodaj_skarb()
        dodaj_skarb(awatar=Obrazek.GWIAZDKA, pozycja=(2,2), punkty=10)
        dodaj_skarb(pozycja=(4,5))
        dodaj_skarb(punkty=-1)

    **Opis**
    Ustawia na mapie skarb, który może zostać zebrana przez bohatera.

    Za zebranie skarbu bohater dostanie określoną liczbę punktów. Zebranie odpowiedniej ilości punktów jest niezbędne
    do wygrania rozgrywki.

    **Parametry**

    - **awatar** _(opcjonalny)_ - obrazek, który będzie reprezentował skarb
        - dopuszczalne wartości:
            - Obrazek.GWIAZDKA
        - wartość domyślna: **Obrazek.GWIAZDKA**
    - **pozycja** _(opcjonalny)_ - numer pola w poziomie, na którym ustawiony zostanie skarb
        - wartość minimalna: **(0, 0)**
        - wartość maksymalna: zależy od wielkości mapy - np (4,4) dla mapy 4x4
        - wartość domyślna: **()** (program wylosuje pole)
    - **punkty** _(opcjonalny)_ - ilość punktów, które uzyska bohater za zebranie skarbu
        - wartość minimalna: brak
        - wartość maksymalna: brak
        - wartość domyślna: **1**
    """
    if len(pozycja) == 0:
        pozycja = MAP_POSITIONS.pop(0)
    __create_collectible(awatar.value, pozycja[0], pozycja[1], punkty)


def ustaw_wynik_docelowy(punkty):
    """
    **Przykłady użycia**

        ustaw_wynik_docelowy(5)

    **Opis**
    Modyfikuje ilość punktów, które musi zebrać bohater by wygrać rozgrywkę.

    Domyślna wartość punktów, które musi zebrać bohater by wygrać rozgrywkę to **1 punkt**.

    **Parametry**

    - **punkty** _(obowiązkowy)_ - ilość punktów
        - wartość minimalna: **0**
        - wartość maksymalna: brak
        - wartość domyślna: brak

    **Zwracane błędy**

    - **RuntimeError**
        - _"Target points value must be greater than 0"_ - Podano zbyt niską wartość
    """
    __set_target_points(punkty)


def __create_map(width, height):
    global MAP_VALID_WIDTH
    global MAP_VALID_HEIGHT

    if width < MAP_VALID_WIDTH[0] or width > MAP_VALID_WIDTH[1] or height < MAP_VALID_HEIGHT[0] or height > \
            MAP_VALID_HEIGHT[1]:
        raise RuntimeError(
            "Map width must be within " + str(MAP_VALID_WIDTH) + " and height must be within " + str(MAP_VALID_HEIGHT))

    if len(MAP_CONFIG) != 0:
        raise RuntimeError("Map was already created!")

    MAP_CONFIG["width"] = width
    MAP_CONFIG["height"] = height
    for x in range(width):
        for y in range(height):
            MAP_POSITIONS.append((x, y))
    random.shuffle(MAP_POSITIONS)


def __create_player(sprite, x, y):
    PLAYER_CONFIGS.append({"sprite": sprite, "x": x, "y": y})
    if (x, y) in MAP_POSITIONS:
        MAP_POSITIONS.remove((x, y))


def __create_enemy(sprite, x, y, speed):
    ENEMY_CONFIGS.append({"sprite": sprite, "x": x, "y": y, "speed": speed})
    if (x, y) in MAP_POSITIONS:
        MAP_POSITIONS.remove((x, y))


def __create_obstacle(sprite, x, y):
    OBSTACLE_CONFIGS.append({"sprite": sprite, "x": x, "y": y})
    if (x, y) in MAP_POSITIONS:
        MAP_POSITIONS.remove((x, y))


def __create_collectible(sprite, x, y, score):
    COLLECTIBLE_CONFIGS.append({"sprite": sprite, "x": x, "y": y, "score": score})
    if (x, y) in MAP_POSITIONS:
        MAP_POSITIONS.remove((x, y))


def __set_target_points(score):
    global TARGET_SCORE
    if score < 0:
        raise RuntimeError("Target points value must be greater than 0")
    TARGET_SCORE = score


def __does_not_contain_obstacle(indices):
    return len([x for x in obstacles if x.current_tile_indices == indices]) == 0


def __tile_indices_valid(indices, map_size):
    return 0 <= indices[0] < map_size[0] and 0 <= indices[1] < map_size[1]


def __draw_sprites(screen, groups):
    for group in groups:
        for sprite in group:
            screen.blit(sprite.surf, sprite.rect)


def __draw_score(screen, star_label, game_font):
    text = str(SCORE) + "/" + str(TARGET_SCORE)
    width = 55 + (34 * len(text))

    star_label.rect.x = SCREEN_CENTER[0] - (width / 2)
    star_label.rect.y = SCREEN_CENTER[1] - 0.9 * SCREEN_CENTER[1]

    screen.blit(star_label.surf, star_label.rect)
    game_font.render_to(screen, (star_label.rect.x + 55, star_label.rect.y + 6), text, (0, 0, 0))


def __move_players(map_size, tilemap, keys):
    for player in players:
        if not player.is_moving:
            target_indices = player.current_tile_indices

            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                if keys[pygame.K_LEFT]:
                    target_indices = (target_indices[0] - 1, target_indices[1])
                if keys[pygame.K_RIGHT]:
                    target_indices = (target_indices[0] + 1, target_indices[1])
                if keys[pygame.K_UP]:
                    target_indices = (target_indices[0], target_indices[1] - 1)
                if keys[pygame.K_DOWN]:
                    target_indices = (target_indices[0], target_indices[1] + 1)

                if 0 <= target_indices[0] < map_size[0] \
                        and 0 <= target_indices[1] < map_size[1] \
                        and __does_not_contain_obstacle(target_indices):
                    player.moveTo(tilemap[target_indices])


def __move_enemies(map_size, tilemap):
    for enemy in enemies:
        if not enemy.is_moving:
            current = enemy.current_tile_indices
            possible_targets = [t for t in [
                (current[0] - 1, current[1]),
                (current[0] + 1, current[1]),
                (current[0], current[1] - 1),
                (current[0], current[1] + 1),
            ] if __does_not_contain_obstacle(t) and __tile_indices_valid(t, map_size)]

            if len(possible_targets) > 1 and enemy.previous_tile_indices in possible_targets:
                possible_targets.remove(enemy.previous_tile_indices)

            random.shuffle(possible_targets)

            enemy.moveTo(tilemap[possible_targets[0]])


def __run_game():
    global GAME_OVER
    global WIN
    global SCORE

    pygame.init()
    pygame.freetype.init()

    game_font = pygame.freetype.Font("resources/milkyboba.ttf", 48)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True

    map_size = (MAP_CONFIG["width"], MAP_CONFIG["height"])

    tilemap, tiles, tile_border = createMap(map_size[0], map_size[1], SCREEN_CENTER)

    for player_config in PLAYER_CONFIGS:
        indices = (player_config["x"], player_config["y"])
        player = createPlayer(player_config["sprite"], tilemap[indices])
        players.add(player)

    for enemy_config in ENEMY_CONFIGS:
        indices = (enemy_config["x"], enemy_config["y"])
        enemy = createEnemy(enemy_config["sprite"], tilemap[indices], enemy_config["speed"])
        enemies.add(enemy)

    for obstacle_config in OBSTACLE_CONFIGS:
        indices = (obstacle_config["x"], obstacle_config["y"])
        obstacle = createObstacle(obstacle_config["sprite"], tilemap[indices])
        obstacles.add(obstacle)

    for collectible_config in COLLECTIBLE_CONFIGS:
        indices = (collectible_config["x"], collectible_config["y"])
        collectible = createCollectibles(collectible_config["sprite"], tilemap[indices], collectible_config["score"])
        collectibles.add(collectible)

    cover = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(cover, (0, 0, 0, 120), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    game_over_label = Image("resources/game_over_label.png", SCREEN_CENTER[0], SCREEN_CENTER[1])
    win_label = Image("resources/win_label.png", SCREEN_CENTER[0], SCREEN_CENTER[1])
    star_label = Image("resources/star.png", 0, 0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if not GAME_OVER and not WIN:
            players.update()
            __move_players(map_size, tilemap, keys)

            enemies.update()
            __move_enemies(map_size, tilemap)

        for player in players:
            if pygame.sprite.spritecollide(player, enemies, False):
                GAME_OVER = True
            else:
                for collectible in pygame.sprite.spritecollide(player, collectibles, True):
                    SCORE += collectible.score
                    if SCORE >= TARGET_SCORE:
                        WIN = True

        screen.fill((130, 170, 60))

        __draw_sprites(screen, [tiles, tile_border, players, enemies, obstacles, collectibles])
        __draw_score(screen, star_label, game_font)

        if GAME_OVER:
            screen.blit(cover, (0, 0))
            screen.blit(game_over_label.surf, game_over_label.rect)

        if WIN:
            screen.blit(cover, (0, 0))
            screen.blit(win_label.surf, win_label.rect)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()
