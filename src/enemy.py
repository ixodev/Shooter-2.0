import pygame
from random import randint



class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.i = 1
        self.image = pygame.image.load("assets/mummy.png")
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect().move(randint(1500, 2500), 410)
        self.speed = 3
        self.lives = 50

    def update(self):
        self.i += 1
        self.image = pygame.image.load("assets/mummy/mummy" + str(self.i) + ".png")
        self.rect.x -= self.speed
        if self.i == 24:
            self.i = 1

    def respawn(self):
        self.rect.x = randint(1500, 2500)
        self.lives += 15