import pygame



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.i = 1
        self.image = pygame.image.load("assets/player/player1.png")
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect().move(-15, 375)
        self.speed = 3
        self.score = 0
        self.lives = 500
        self.attack = False

    def update(self):
        self.i += 1
        self.image = pygame.image.load("assets/player/player" + str(self.i) + ".png")
        if self.i == 24:
            self.i = 1
            self.attack = False