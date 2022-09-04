import pygame
from projectiles import Projectile


class Enemy(object):
    def __init__(self, x, y, width, height, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 35
        self.hitbox = (self.x, self.y, 120, 80)
        self.timer_count = 0
        self.dead = False
        self.hit_count = 0
        self.window = window

    def draw(self):
        self.move()
        self.hitbox = (self.x, self.y, 120, 80)
        self.window.blit(pygame.image.load("img/enemy_01.png"), (self.x, self.y))

    def move(self):
        if self.timer_count <= 1000:
            self.timer_count += 1
        else:
            self.y += self.vel
            self.timer_count = 0

    def hit(self):
        self.hit_count += 1
        if self.hit_count >= 5:
            self.dead = True
            # print("enemy is dead")
            self.hit_count = 0


class Shooter(Enemy):
    def __init__(self, x, y, width, height, window, enemy_bullets):
        Enemy.__init__(self, x, y, width, height, window)
        self.enemy_bullets = enemy_bullets

    def draw(self):
        self.move()
        self.hitbox = (self.x, self.y, 120, 80)
        self.window.blit(pygame.image.load("img/enemy_02.png"), (self.x, self.y))

    def shoot(self):
        if not self.dead:
            self.enemy_bullets.append(Projectile(round(self.x + self.width // 2), round(self.y + self.height // 2), 6, (255, 255, 255), self.window))
