# import the pygame module, so you can use it
import random

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
TARGET_SCORE = 3

GAME_OVER = False
WIN = False

clock = pygame.time.Clock()

players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()


def stworz_mape(szerokosc=-1, wysokosc=-1):
    """Tworzy mapę o podanej ilości pól w poziomie i pionie. """
    if szerokosc == -1 and wysokosc == -1:
        szerokosc = random.randint(MAP_VALID_WIDTH[0], MAP_VALID_WIDTH[1])
        wysokosc = random.randint(MAP_VALID_HEIGHT[0], MAP_VALID_HEIGHT[1])
    __create_map(szerokosc, wysokosc)


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


def dodaj_gracza(obrazek="player.png", x=-1, y=-1):
    if x == -1 and y == -1:
        x, y = MAP_POSITIONS.pop(0)
    __create_player(obrazek, x, y)


def __create_player(sprite, x, y):
    PLAYER_CONFIGS.append({"sprite": sprite, "x": x, "y": y})
    if (x, y) in MAP_POSITIONS:
        MAP_POSITIONS.remove((x, y))


def dodaj_przeciwnika(obrazek="enemy.png", x=-1, y=-1, predkosc=1):
    if x == -1 and y == -1:
        x, y = MAP_POSITIONS.pop(0)
    __create_enemy(obrazek, x, y, predkosc)


def __create_enemy(sprite, x, y, speed):
    ENEMY_CONFIGS.append({"sprite": sprite, "x": x, "y": y, "speed": speed})
    if (x, y) in MAP_POSITIONS:
        MAP_POSITIONS.remove((x, y))


def dodaj_przeszkode(obrazek="crates.png", x=-1, y=-1):
    if x == -1 and y == -1:
        x, y = MAP_POSITIONS.pop(0)
    __create_obstacle(obrazek, x, y)


def __create_obstacle(sprite, x, y):
    OBSTACLE_CONFIGS.append({"sprite": sprite, "x": x, "y": y})
    if (x, y) in MAP_POSITIONS:
        MAP_POSITIONS.remove((x, y))


def dodaj_znajdzke(obrazek="star.png", x=-1, y=-1, punkty=1):
    if x == -1 and y == -1:
        x, y = MAP_POSITIONS.pop(0)
    __create_collectible(obrazek, x, y, punkty)


def __create_collectible(sprite, x, y, score):
    COLLECTIBLE_CONFIGS.append({"sprite": sprite, "x": x, "y": y, "score": score})
    if (x, y) in MAP_POSITIONS:
        MAP_POSITIONS.remove((x, y))


def ustaw_wynik_docelowy(punkty):
    __set_target_points(punkty)


def __set_target_points(score):
    global TARGET_SCORE
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


def uruchom_gre():
    __run_game()


def __run_game():
    global GAME_OVER
    global WIN
    global SCORE

    pygame.init()
    pygame.freetype.init()

    game_font = pygame.freetype.Font("milkyboba.ttf", 48)
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

    game_over_label = Image("game_over_label.png", SCREEN_CENTER[0], SCREEN_CENTER[1])
    win_label = Image("win_label.png", SCREEN_CENTER[0], SCREEN_CENTER[1])
    star_label = Image("star.png", 0, 0)

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
