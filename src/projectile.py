import pygame



class Projectile:
    def __init__(self):
        self.image = pygame.image.load("assets/projectile.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 10, self.image.get_height() / 10))
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self):
        self.rect.x += self.speed