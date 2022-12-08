import pygame
from pygame.locals import (
    RLEACCEL,
)


class Image(pygame.sprite.Sprite):
    def __init__(self, background, center_x, center_y):
        super(Image, self).__init__()

        self.background = background
        self.x = center_x
        self.y = center_y

        self.surf = pygame.image.load(self.background).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

        self.rect.centerx = center_x
        self.rect.centery = center_y
