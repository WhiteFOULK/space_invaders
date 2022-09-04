import pygame


class Player(object):
    def __init__(self, x, y, width, height, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 120
        self.window = window
        self.hitbox = (self.x, self.y, 120, 90)
        self.hit = 0

    def draw(self):
        self.window.blit(pygame.image.load("img/ship.png"), (self.x, self.y))
