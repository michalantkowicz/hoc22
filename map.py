import math
import pygame
from pygame.locals import (
    RLEACCEL,
)

TILE_WIDTH = 64
TILE_CORNER_WIDTH = 8
TILE_BORDER_SIZE = (64, 8)
TILE_BACKGROUNDS = ("resources/tile_floor_horizontal.png", "resources/tile_floor_vertical.png")


class Tile(pygame.sprite.Sprite):
    def __init__(self, background, center_x, center_y, indices):
        super(Tile, self).__init__()

        self.background = background
        self.x = center_x
        self.y = center_y

        self.surf = pygame.image.load(self.background).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        self.rect.centerx = center_x
        self.rect.centery = center_y

        self.indices = indices


class TileBorder(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, angle=0):
        super(TileBorder, self).__init__()

        self.surf = pygame.image.load("resources/tile_border.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.rotate(self.surf, angle)
        self.rect = self.surf.get_rect()

        self.rect.centerx = center_x
        self.rect.centery = center_y


class TileCorner(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, angle=0):
        super(TileCorner, self).__init__()

        self.surf = pygame.image.load("resources/tile_border_corner.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.rotate(self.surf, angle)
        self.rect = self.surf.get_rect()

        self.rect.centerx = center_x
        self.rect.centery = center_y


def createMap(map_width, map_height, screen_center):
    global TILE_BACKGROUNDS

    if map_width % 2 == 0:
        screen_center[0] += TILE_WIDTH / 2.0
    if map_height % 2 == 0:
        screen_center[1] += TILE_WIDTH / 2.0

    tilemap = {}
    tiles = pygame.sprite.Group()
    tile_border = pygame.sprite.Group()

    for i_y in range(-math.floor(map_height / 2.0), math.ceil(map_height / 2.0)):
        if map_width % 2 == 0:
            TILE_BACKGROUNDS = TILE_BACKGROUNDS[::-1]
        for i_x in range(-math.floor(map_width / 2.0), math.ceil(map_width / 2.0)):
            background = TILE_BACKGROUNDS[0]

            x = screen_center[0] + i_x * TILE_WIDTH
            y = screen_center[1] + i_y * TILE_WIDTH

            tile_indices = (i_x + math.floor(map_width / 2.0), i_y + math.floor(map_height / 2.0))

            tile = Tile(background, x, y, tile_indices)
            tilemap[tile_indices] = tile

            tiles.add(tile)

            TILE_BACKGROUNDS = TILE_BACKGROUNDS[::-1]

    for i_y in range(0, map_height):
        x_modifier = (TILE_WIDTH / 2.0) + (TILE_BORDER_SIZE[1] / 2.0)

        tile_left = tilemap[(0, i_y)]
        tile_border.add(TileBorder(tile_left.rect.centerx - x_modifier, tile_left.rect.centery, 90))

        tile_right = tilemap[(map_width - 1, i_y)]
        tile_border.add(TileBorder(tile_right.rect.centerx + x_modifier, tile_right.rect.centery, -90))

    for i_x in range(0, map_width):
        y_modifier = (TILE_WIDTH / 2.0) + (TILE_BORDER_SIZE[1] / 2.0)

        tile_top = tilemap[(i_x, 0)]
        tile_border.add(TileBorder(tile_top.rect.centerx, tile_top.rect.centery - y_modifier))

        tile_bottom = tilemap[(i_x, map_height - 1)]
        tile_border.add(TileBorder(tile_bottom.rect.centerx, tile_bottom.rect.centery + y_modifier, 180))

    x_modifier = (TILE_WIDTH / 2.0) + (TILE_CORNER_WIDTH / 2.0)
    y_modifier = (TILE_WIDTH / 2.0) + (TILE_CORNER_WIDTH / 2.0)

    bl_tile_rect = tilemap[(0, map_height - 1)].rect
    tile_border.add(TileCorner(bl_tile_rect.centerx - x_modifier, bl_tile_rect.centery + y_modifier, 180))

    tl_tile_rect = tilemap[(0, 0)].rect
    tile_border.add(TileCorner(tl_tile_rect.centerx - x_modifier, tl_tile_rect.centery - y_modifier, 90))

    br_tile_rect = tilemap[(map_width - 1, map_height - 1)].rect
    tile_border.add(TileCorner(br_tile_rect.centerx + x_modifier, br_tile_rect.centery + y_modifier, -90))

    tr_tile_rect = tilemap[(map_width - 1, 0)].rect
    tile_border.add(TileCorner(tr_tile_rect.centerx + x_modifier, tr_tile_rect.centery - y_modifier))

    return tilemap, tiles, tile_border
