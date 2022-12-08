import math

import pygame
from pygame.locals import (
    RLEACCEL,
)


def v_length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


class Collectible(pygame.sprite.Sprite):
    def __init__(self, background, center_x, center_y, current_tile_indices, score):
        super(Collectible, self).__init__()

        self.background = background
        self.x = center_x
        self.y = center_y

        self.surf = pygame.image.load(self.background).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        self.rect.centerx = center_x
        self.rect.centery = center_y

        self.current_tile_indices = current_tile_indices

        self.score = score


def createCollectibles(background, tile, score):
    return Collectible(background, tile.rect.centerx, tile.rect.centery, tile.indices, score)
