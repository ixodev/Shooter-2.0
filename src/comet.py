import pygame
import random


class Comet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/comet.png")
        self.rect = self.image.get_rect()
        self.rect.move(random.randint(10, 1500 - self.rect.width + 10), 0 - self.rect.width - 10)
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.y == 375 - self.rect.height: self.rect.y = 0 - self.rect.height