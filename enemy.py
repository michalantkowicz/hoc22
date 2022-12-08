import math

import pygame
from pygame.locals import (
    RLEACCEL,
)


def v_length(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, background, center_x, center_y, current_tile_indices, speed):
        super(Enemy, self).__init__()

        self.background = background
        self.x = center_x
        self.y = center_y

        self.surf = pygame.image.load(self.background).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        self.rect.centerx = center_x
        self.rect.centery = center_y

        self.target_position = (center_x, center_y)

        self.speed = speed
        self.is_moving = False
        self.current_tile_indices = current_tile_indices
        self.previous_tile_indices = current_tile_indices

    def update(self):
        if self.is_moving:
            x = self.rect.centerx
            y = self.rect.centery
            t_x = self.target_position[0]
            t_y = self.target_position[1]
            if (self.rect.centerx, self.rect.centery) == self.target_position:
                self.is_moving = False
            elif v_length((t_x - x, t_y - y)) <= self.speed:
                self.rect.centerx = t_x
                self.rect.centery = t_y
            else:
                v = ((t_x - x), (t_y - y))
                v_norm = (v[0] / v_length(v), v[1] / v_length(v))
                self.rect.centerx += v_norm[0] * self.speed
                self.rect.centery += v_norm[1] * self.speed

    def moveTo(self, tile):
        self.is_moving = True
        self.previous_tile_indices = self.current_tile_indices
        self.current_tile_indices = tile.indices
        self.target_position = (tile.rect.centerx, tile.rect.centery)


def createEnemy(background, tile, speed):
    return Enemy(background, tile.rect.centerx, tile.rect.centery, tile.indices, speed)
