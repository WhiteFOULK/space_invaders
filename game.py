import pygame
from menu import MainMenu, YouAreDead, Invasion, Win
from player import Player
from projectiles import Live, Projectile
from enemies import Enemy, Shooter

clock = pygame.time.Clock()


class Game(object):
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.L_KEY, self.R_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 600, 850
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = '8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.dead = YouAreDead(self)
        self.invasion = Invasion(self)
        self.win_screen = Win(self)
        self.curr_menu = self.main_menu
        self.ship = Player(240, 750, 120, 90, self.window)
        self.bullets = []
        self.shoot_loop = 0
        self.enemy_loop = 0
        self.player_lives = []
        self.enemy_bullets = []
        self.enemies = []
        self.enemy_x = 0
        self.enemy_y = 105
        self.live_coord = 365

    def game_loop(self):
        self.update_the_game()

        while self.playing:
            if len(self.enemies) == 0:
                self.playing = False
                self.curr_menu = self.win_screen

            clock.tick(350)
            pygame.display.set_caption("Space Invasion")

            self.check_events()
            self.move_player()
            self.reset_keys()
            if self.START_KEY:
                self.playing = False

            # CHECKING ENEMY HITS AND INVASION
            for enemy in self.enemies:
                if not enemy.dead:
                    for bullet in self.bullets:
                        if (bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3]) \
                                and (bullet.y + bullet.radius > enemy.hitbox[1]):
                            if (bullet.x + bullet.radius > enemy.hitbox[0]) \
                                    and (bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]):
                                enemy.hit()
                                self.bullets.pop(self.bullets.index(bullet))
                                if enemy.dead:
                                    self.enemies.pop(self.enemies.index(enemy))

            # CHECKING THE INVASION
            for enemy in self.enemies:
                if not enemy.dead and (enemy.y >= 675):
                    self.playing = False
                    self.curr_menu = self.invasion
                    # self.curr_menu.display_menu()

            # PLAYER BULLETS
            for bullet in self.bullets:
                if (bullet.y < 850) and (bullet.y > 0):
                    bullet.y -= bullet.vel
                else:
                    self.bullets.pop(self.bullets.index(bullet))

            # ENEMY BULLETS
            for bullet in self.enemy_bullets:
                if (bullet.y < 850) and (bullet.y > 0):
                    bullet.y += bullet.vel
                else:
                    self.enemy_bullets.pop(self.enemy_bullets.index(bullet))

            # CHECKING IF ENEMY BULLET HITS PLAYER
            for bullet in self.enemy_bullets:
                if (bullet.y + bullet.radius < self.ship.y + self.ship.height) \
                        and (bullet.y - bullet.radius > self.ship.y):
                    if (bullet.x + bullet.radius > self.ship.x) \
                            and (bullet.x - bullet.radius < self.ship.x + self.ship.width):
                        self.ship.hit += 1

                        self.player_lives[self.ship.hit - 1].dead = True

                        self.enemy_bullets.pop(self.enemy_bullets.index(bullet))

                        if self.player_lives[0].dead and self.player_lives[1].dead and self.player_lives[2].dead:
                            self.playing = False
                            self.curr_menu = self.dead
                            self.curr_menu.display_menu()

            # SHOOTER
            if self.enemy_loop == 250:
                for enemy in self.enemies:
                    if type(enemy) == Shooter:
                        enemy.shoot()

                self.enemy_loop = 0

            self.enemy_loop += 1

            self.redraw_game_window()

    def update_the_game(self):
        self.playing = True
        self.ship = Player(240, 750, 120, 90, self.window)
        self.bullets = []
        self.shoot_loop = 0
        self.enemy_loop = 0
        self.player_lives = []
        self.enemy_bullets = []
        self.enemies = []
        self.enemy_x = 0
        self.enemy_y = 105
        self.live_coord = 365
        self.cast_enemies()
        self.cast_player_lives()

    def cast_enemies(self):
        for row in range(5):
            for column in range(5):
                if (row == 2) and (column == 2):
                    self.enemies.append(Shooter(self.enemy_x, self.enemy_y, 120, 80, self.window, self.enemy_bullets))
                else:
                    self.enemies.append(Enemy(self.enemy_x, self.enemy_y, 120, 80, self.window))
                self.enemy_x += 120
            self.enemy_x = 0
            self.enemy_y += 90

    def cast_player_lives(self):
        for live in range(3):
            self.player_lives.append(Live(self.live_coord, 25, self.window))
            self.live_coord += 80

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.curr_menu.run_display = False
                self.running, self.playing = False, False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.L_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.R_KEY = True
                if event.key == pygame.K_SPACE:
                    self.SPACE_KEY = True

    def move_player(self):
        if self.shoot_loop > 0:
            self.shoot_loop += 1
        if self.shoot_loop > 3:
            self.shoot_loop = 0

        self.check_events()
        if self.R_KEY:
            if self.ship.x + self.ship.vel <= 480:
                self.ship.x += 120
            self.R_KEY = False
        if self.L_KEY:
            if self.ship.x - self.ship.vel >= 0:
                self.ship.x -= 120
            self.L_KEY = False
        if self.SPACE_KEY:
            if len(self.bullets) < 5:
                self.bullets.append(Projectile(round(self.ship.x + self.ship.width // 2), round(self.ship.y + self.ship.height // 2), 6, self.WHITE, self.window))
            self.SPACE_KEY = False

            self.shoot_loop = 1

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.L_KEY, self.R_KEY, self.START_KEY, self.BACK_KEY, self.SPACE_KEY = False, False, False, False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def redraw_game_window(self):
        self.window.fill((0, 0, 0))

        if self.ship.hit < 3:
            self.ship.draw()

        for enemy_ship in self.enemies:
            if not enemy_ship.dead:
                enemy_ship.draw()

        for bul in self.bullets:
            bul.draw()

        for en_bul in self.enemy_bullets:
            en_bul.draw()

        for lv in self.player_lives:
            if not lv.dead:
                lv.draw()
            else:
                lv.draw_dead()

        pygame.display.update()
