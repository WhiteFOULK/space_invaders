import pygame

pygame.init()
pygame.font.init()


class Menu(object):
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.start_x, self.start_y = self.mid_w, self.mid_h + 30
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 50
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
        self.credits = False

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            pygame.display.set_caption("Space Invasion")
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            if self.credits:
                self.game.draw_text("That game was made by", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 120)
            self.game.draw_text("Start Game", 20, self.start_x, self.start_y)
            self.game.draw_text("Credits", 20, self.credits_x, self.credits_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.run_display = False
                self.game.playing = True
            elif self.state == 'Credits':
                self.credits = True


class YouAreDead(object):
    def __init__(self, game):
        self.game = game
        self.run_display = True
        # Menu.__init__(self, game)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("You are dead", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 60)
            self.game.draw_text("Press Enter twice to restart", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.run_display = False
            # self.game.playing = False
            # self.game.curr_menu = self.game.main_menu


class Invasion(object):
    def __init__(self, game):
        self.game = game
        self.run_display = True
        # Menu.__init__(self, game)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("You failed to", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("prevent the invasion", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.game.draw_text("Press Enter once to restart", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.run_display = False
            # self.game.playing = False
            # self.game.curr_menu = self.game.main_menu


class Win(object):
    def __init__(self, game):
        self.game = game
        self.run_display = True
        # Menu.__init__(self, game)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("You are winner", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text("Press Enter once to restart", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.game.draw_text("Or just quit the game", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
            self.blit_screen()

    def check_input(self):
        if self.game.START_KEY:
            self.run_display = False
            # self.game.playing = False
            # self.game.curr_menu = self.game.main_menu
