import pygame
import random


class Comet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/comet.png")
        self.rect = self.image.get_rect()
        self.rect.move(random.randint(10, 1500 - self.rect.width + 10), 0 - self.rect.width - 10)
        self.speed = 5
        self.finish = False

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 631:
            self.finish = True