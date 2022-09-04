import pygame


class Live(object):
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.player_hit = 0
        self.dead = False
        self.window = window

    def draw(self):
        self.window.blit(pygame.image.load("img/heart_alive.png"), (self.x, self.y))

    def draw_dead(self):
        self.window.blit(pygame.image.load("img/heart_dead.png"), (self.x, self.y))


class Projectile(object):
    def __init__(self, x, y, radius, color, window):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 1
        self.window = window

    def draw(self):
        pygame.draw.circle(self.window, self.color, (self.x, self.y), self.radius)
