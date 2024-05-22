# Written by Younès B.
# Images : https://www.flaticon.com
# Inspired from Graven
import random

try:
    import pygame
    from pygame.locals import *
    from pygame.mixer import *
    import sys
    from src.player import *
    from src.projectile import *
    from src.enemy import *
    from src.comet import *
except ImportError:
    raise SystemExit("Sorry, can't find required libraries.")


pygame.init()
pygame.display.init()
pygame.mixer.init()


class Game:
    def __init__(self):

        self.GAME_STATE = False
        self.SCREENRECT = pygame.Rect(0, 0, 1500, 631)
        self.WHITE = [255, 255, 255]
        self.BLACK = [0, 0, 0]
        self.IS_PLAYING = True
        self.FULLSCREEN = False
        self.SOUND = True
        self.L_INDEX = 0

        self.player = Player()
        self.projectiles = []

        self.enemies = []
        for enemy in range(3):
            self.enemies.append(Enemy())
        

        self.screen = pygame.display.set_mode(self.SCREENRECT.size)
        pygame.display.set_caption("Shooter v2.0")
        pygame.display.set_icon(pygame.image.load("assets/banner.png"))

        self.bg = pygame.image.load("assets/bg.jpg")

        self.comet_rain = False
        self.comets = []
        self.credits_font = pygame.font.Font("assets/Font.ttf", 20)

    def spawn_comets(self):


        for x in range(10):
            comet = Comet()
            comet.rect.x = random.randint(0, self.SCREENRECT.width - comet.rect.width)
            comet.rect.y = random.randint(round(self.SCREENRECT.height / 2 * -1), comet.rect.height * -1)
            self.comets.append(comet)

        self.comet_rain = True


    def play_game_music(self):
        music = pygame.mixer.music.load("assets/sounds/music.ogg")
        pygame.mixer.music.play(-1)
        
    def play_sound(self, name):
        sound = pygame.mixer.Sound("assets/sounds/" + name + ".ogg")
        sound.play()

    def handle_inputs(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.player.rect.x <= self.SCREENRECT.width - self.player.rect.width:
            self.player.rect.x += self.player.speed
        elif key[pygame.K_LEFT] and self.player.rect.x >= 0:
            self.player.rect.x -= self.player.speed

    def launch_projectile(self):
        projectile = Projectile()
        projectile.rect.y = self.player.rect.y + self.player.rect.height * 0.5
        projectile.rect.x = self.player.rect.x + self.player.rect.width * 0.5
        self.projectiles.append(projectile)

    def draw_texts(self):
        color = pygame.Color("black")
        score_lives_font = pygame.font.Font("assets/Font.ttf", 35)
        credits = self.credits_font.render("Written by Younes B.", 0, color)
        score = score_lives_font.render("Score : " + str(self.player.score) + " points", 0, color)
        lives = score_lives_font.render("Lives : " + str(self.player.lives), 0, color)
        self.screen.blit(credits, (5, 5))
        self.screen.blit(score, (5, 30))
        self.screen.blit(lives, (5, 65))

    def draw_pause_text(self):
        color = pygame.Color("blue")
        font = pygame.font.Font("assets/Font.ttf", 40)
        image = font.render("GAME PAUSED", 0, color)
        rect = image.get_rect()
        self.screen.blit(image, (self.SCREENRECT.width * 0.5 - rect.width * 0.5, self.SCREENRECT.height * 0.5 - rect.width * 0.5))

    def game_over(self):
        pygame.mixer.music.stop()
        color = pygame.Color("red")
        font = pygame.font.Font("assets/Font.ttf", 40)
        image = font.render("GAME OVER", 0, color)
        rect = image.get_rect()
        self.screen.fill(self.WHITE)
        self.screen.blit(image, (self.SCREENRECT.width * 0.5 - rect.width * 0.5, self.SCREENRECT.height * 0.5 - rect.width * 0.5))
        pygame.display.flip()
        self.play_sound("game_over")
        pygame.time.wait(5000)
        self.GAME_STATE = False
        self.player.lives, self.player.score = 500, 0


    def draw_menu(self):
        self.screen.blit(self.bg, (0, 0))
        banner = pygame.image.load("assets/banner.png")
        banner = pygame.transform.scale(banner, (banner.get_width() / 2, banner.get_height() / 2))
        rect = banner.get_rect()
        self.screen.blit(banner, (self.SCREENRECT.width / 2 - rect.width / 2, self.SCREENRECT.height / 2 - rect.height / 2))
        font = pygame.font.Font("assets/Font.ttf", 30)
        text = font.render("Shooter 2.0 by Younes B.", 0, [255, 255, 255])
        rect = text.get_rect()
        self.screen.blit(text, (self.SCREENRECT.width / 2 - rect.width / 2, 10))
        button = pygame.image.load("assets/button.png")
        button = pygame.transform.scale(button, (button.get_width() / 2.5, button.get_height() / 2.5))
        rect = button.get_rect()
        rect.x, rect.y = self.SCREENRECT.width / 2 - rect.width / 2, self.SCREENRECT.height - rect.height - 50
        self.screen.blit(button, rect)
        pygame.display.flip()

        for evt in pygame.event.get():
            if evt.type == QUIT or evt.type == KEYDOWN and evt.key == K_ESCAPE:
                pygame.quit()
                quit()
            elif evt.type == MOUSEBUTTONDOWN:
                if rect.collidepoint(evt.pos):
                    self.GAME_STATE = True


    def run(self):

        clock = pygame.time.Clock()
        running = True
        #self.play_game_music()

        while running:
            if not self.GAME_STATE: self.draw_menu()

            else:
                if self.IS_PLAYING:

                    self.handle_inputs()

                    self.screen.blit(self.bg, (0, 0))
                    self.draw_texts()
                    self.screen.blit(self.player.image, self.player.rect)

                    if self.player.attack:
                        self.player.update()
                        if self.player.i == 24:
                            self.player.attack = False

                    for projectile in self.projectiles:
                        self.screen.blit(projectile.image, projectile.rect)
                        projectile.update()

                    for enemy in self.enemies:
                        enemy.update()
                        self.screen.blit(enemy.image, enemy.rect)
                        if enemy.rect.x == 0: enemy.respawn()

                        i = 0
                        for projectile in self.projectiles:
                            if projectile.rect.colliderect(enemy.rect):
                                enemy.lives -= 5
                                del self.projectiles[i]
                                self.player.score += 0.25
                            i += 1

                        if enemy.rect.colliderect(self.player.rect): self.player.lives -= 2
                        if enemy.lives <= 0:
                            enemy.respawn()
                            self.player.score += 1

                    if random.randint(0, 100) == 24 and not self.comet_rain:
                        self.comet_rain = True
                        self.spawn_comets()

                    for comet in self.comets:
                        comet.update()
                        if comet.finish:
                            self.comets.remove(comet)
                        else:
                            self.screen.blit(comet.image, comet.rect)

                    print(len(self.comets))

                    if len(self.comets) == 0:
                        self.comet_rain = False

                    if self.player.lives <= 0:
                        pygame.time.wait(2000)
                        self.game_over()

                    pygame.display.flip()

                    for evt in pygame.event.get():
                        if evt.type == QUIT or evt.type == KEYDOWN and evt.key == K_ESCAPE: self.GAME_STATE = False
                        elif evt.type == KEYDOWN and evt.key == K_SPACE:
                            self.play_sound("click")
                            self.player.attack = True
                            self.launch_projectile()
                            self.play_sound("tir")
                        elif evt.type == KEYDOWN and evt.key == K_f:
                            sc = self.screen.copy()
                            if self.FULLSCREEN: self.screen = pygame.display.set_mode(self.SCREENRECT.size)
                            else: self.screen = pygame.display.set_mode(self.SCREENRECT.size, FULLSCREEN)
                            self.FULLSCREEN = not self.FULLSCREEN
                        elif evt.type == KEYDOWN and evt.key == K_m:
                            if self.SOUND: pygame.mixer.music.pause()
                            else: pygame.mixer.music.unpause()
                            self.SOUND = not self.SOUND
                        elif evt.type == KEYDOWN and evt.key == K_p:
                            pygame.mixer.music.pause()
                            self.IS_PLAYING = not self.IS_PLAYING


                    self.L_INDEX += 1

                    if self.L_INDEX == 500:
                        self.enemies.append(Enemy())

                        for enemy in self.enemies:
                            enemy.speed += 1
                            enemy.lives += 1

                        self.L_INDEX = 0

                    clock.tick(100)


                elif not self.IS_PLAYING:

                    self.draw_pause_text()
                    pygame.display.flip()

                    for evt in pygame.event.get():
                        if evt.type == QUIT or evt.type == KEYDOWN and evt.key == K_ESCAPE: self.GAME_STATE = False
                        elif evt.type == KEYDOWN and evt.key == K_f:
                            sc = self.screen.copy()
                            if self.FULLSCREEN: self.screen = pygame.display.set_mode(self.SCREENRECT.size)
                            else: self.screen = pygame.display.set_mode(self.SCREENRECT.size, FULLSCREEN)
                            self.FULLSCREEN = not self.FULLSCREEN
                        if evt.type == KEYDOWN and evt.key == K_p:
                            pygame.mixer.music.unpause()
                            self.IS_PLAYING = not self.IS_PLAYING


        pygame.quit()
        quit()


if __name__ == "__main__":
    app = Game()
    app.run()
