from textinput import *
import pygame
import sys
from gameplay import Game
from pygame.locals import *

pygame.init()

class Choices():
    def __init__(self, screen, clock, background_img, font):
        self.screen = screen
        self.clock = clock
        self.WHITE=(255,255,255)
        self.background_img = background_img
        self.font = font
        self.players = 1
        #health?
        self.gamemode = "classic"
        self.Player1_keys = ["a", "s", "d"]
        self.Player2_keys = ["j", "k", "l"]
        self.player1_name = ""
        self.player2_name = ""
        self.tournament_wins = []
    # function for drawing text
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, self.WHITE)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    # keybindings menu
    def change_keys(self, button, click, keys, i):
        mx, my = pygame.mouse.get_pos()
        if button.collidepoint((mx, my)):
            if click:
                while click == True:
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                self.main_menu()
                            else:
                                keys[i] = pygame.key.name(event.key)
                            click = False
    def key_menu(self):
        click = False
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.draw_text('KEY BINDINGS', self.font, self.WHITE, self.screen, 465, 20)
            button_1 = pygame.Rect(640, 340, 50, 50)
            button_2 = pygame.Rect(640, 440, 50, 50)
            button_3 = pygame.Rect(640, 540, 50, 50)
            button_4 = pygame.Rect(940, 340, 50, 50)
            button_5 = pygame.Rect(940, 440, 50, 50)
            button_6 = pygame.Rect(940, 540, 50, 50)
            self.draw_text('( COMMAND )', self.font, self.WHITE, self.screen, 130, 240)
            self.draw_text('( KEY )', self.font, self.WHITE, self.screen, 570, 240)
            self.draw_text('Player 1', self.font, self.WHITE, self.screen, 540, 140)
            self.draw_text('( KEY )', self.font, self.WHITE, self.screen, 870, 240)
            self.draw_text('Player 2', self.font, self.WHITE, self.screen, 840, 140)
            self.draw_text(self.Player2_keys[0], self.font, self.WHITE, self.screen, 940, 340)
            self.draw_text(self.Player2_keys[1], self.font, self.WHITE, self.screen, 940, 440)
            self.draw_text(self.Player2_keys[2], self.font, self.WHITE, self.screen, 940, 540)
            self.draw_text('MAGIC', self.font, self.WHITE, self.screen, 200, 340)
            self.draw_text(self.Player1_keys[0], self.font, self.WHITE, self.screen, 640, 340)
            self.draw_text('SWORD', self.font, self.WHITE, self.screen, 195, 440)
            self.draw_text(self.Player1_keys[1], self.font, self.WHITE, self.screen, 640, 440)
            self.draw_text('POTION', self.font, self.WHITE, self.screen, 195, 540)
            self.draw_text(self.Player1_keys[2], self.font, self.WHITE, self.screen, 640, 540)
            self.change_keys(button_1, click, self.Player1_keys, 0)
            self.change_keys(button_2, click, self.Player1_keys, 1)
            self.change_keys(button_3, click, self.Player1_keys, 2)
            self.change_keys(button_4, click, self.Player2_keys, 0)
            self.change_keys(button_5, click, self.Player2_keys, 1)
            self.change_keys(button_6, click, self.Player2_keys, 2)
            click = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.main_menu()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
            self.clock.tick(60)
    #gameover menu
    def game_over(self, who_won):
        running = True
        while running:
            self.screen.fill(0)
            self.draw_text('GAME OVER', self.font, self.WHITE, self.screen, 470, 150)
            if who_won == 1:
                self.draw_text('Player 1 won', self.font, self.WHITE, self.screen, 450, 300)
            elif who_won==2:
                self.draw_text('Player 2 won', self.font, self.WHITE, self.screen, 450, 300)
            else:
                self.draw_text('Its a tie', self.font, self.WHITE, self.screen, 450, 300)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.main_menu()
            pygame.display.update()
            self.clock.tick(60)
    def rounds(self, i):
        running = True
        while running:
            self.screen.fill(0)
            self.draw_text(f'ROUND {i}', self.font, self.WHITE, self.screen, 500, 300)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        running = False
            pygame.display.update()
            self.clock.tick(60)
    # function for entering names
    def player_name_input(self, player):
        self.screen.fill(0)
        self.draw_text(player, self.font, self.WHITE, self.screen, 420, 250)
        text_input_box = TextInputBox(420, 300, 500, self.font)
        group = pygame.sprite.Group(text_input_box)
        run = True
        while run:
            event_list = pygame.event.get()
            group.update(event_list)
            group.draw(self.screen)
            pygame.display.flip()
            for event in event_list:
                if event.type == KEYDOWN:
                    if event.key == K_RETURN and player == 'Player1 name':
                        self.player_name_input('Player2 name')
                    elif event.key == K_RETURN:
                        self.settings_menu()
                    elif player == 'Player1 name':
                        self.player1_name += pygame.key.name(event.key)
                    else:
                        self.player2_name += pygame.key.name(event.key)
    # function for choosing how many people are playing
    def settings_menu(self):
        click = False
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.draw_text('CHOOSE HOW MANY PLAYERS', self.font, self.WHITE, self.screen, 300, 20)
            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(70, 150, 500, 100)
            button_2 = pygame.Rect(840, 140, 280, 50)
            button_3 = pygame.Rect(200, 450, 250, 50)
            button_4 = pygame.Rect(850, 450, 280, 50)
            self.draw_text('1 PLAYER', self.font, self.WHITE, self.screen, 200, 150)
            self.draw_text('( WITH A COMPUTER )', self.font, self.WHITE, self.screen, 70, 200)
            self.draw_text('2 PLAYERS', self.font, self.WHITE, self.screen, 850, 150)
            self.draw_text('CHOOSE GAME MODE', self.font, self.WHITE, self.screen, 400, 320)
            self.draw_text('Classic', self.font, self.WHITE, self.screen, 200, 450)
            self.draw_text('Tournament', self.font, self.WHITE, self.screen, 850, 450)
            if button_1.collidepoint((mx, my)):
                if click:
                    pygame.draw.rect(self.screen, (0,0,0), (70, 150, 600, 100))
                    self.players = 1
            if button_2.collidepoint((mx, my)):
                if click:
                    self.players = 2
                    pygame.draw.rect(self.screen, (0,0,0), (840, 140, 280, 50))
                    #self.player_name_input('Player1 name')
            if button_3.collidepoint((mx, my)):
                if click:
                    self.gamemode = "classic"
                    pygame.draw.rect(self.screen, (0,0,0), (200, 450, 250, 50))
            if button_4.collidepoint((mx, my)):
                if click:
                    self.gamemode = "tournament"
                    pygame.draw.rect(self.screen, (0,0,0), (850, 450, 280, 50))
            click = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.main_menu()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
            self.clock.tick(60)
    #function to show combos
    def combos(self):
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.draw_text('COMBO ATTACKS', self.font, self.WHITE, self.screen, 420, 20)
            self.draw_text('Magic * Sword * Potion', self.font, self.WHITE, self.screen, 320, 200)
            self.draw_text('Sword * Sword * Sword', self.font, self.WHITE, self.screen, 313, 300)
            self.draw_text('Sword * Magic * Magic', self.font, self.WHITE, self.screen, 320, 400)
            self.draw_text('Magic * Potion * Magic', self.font, self.WHITE, self.screen, 325, 500)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.main_menu()
            pygame.display.update()
            self.clock.tick(60)
    # function for main menu
    def main_menu(self):
        click=False
        while True:
            self.game_functions = Game(self.Player1_keys, self.Player2_keys, self.players, self.gamemode,
                                       self.player1_name, self.player2_name)
            self.screen.fill((0, 0, 0))
            self.draw_text('MAIN MENU', self.font, self.WHITE, self.screen, 485, 20)
            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(520, 140, 200, 50)
            button_2 = pygame.Rect(460, 240, 340, 50)
            button_3 = pygame.Rect(510, 340, 200, 50)
            button_4 = pygame.Rect(530, 450, 180, 50)
            button_5 = pygame.Rect(575, 550, 150, 50)
            self.draw_text('START', self.font, self.WHITE, self.screen, 550, 150)
            self.draw_text('KEY BINDINGS', self.font, self.WHITE, self.screen, 470, 250)
            self.draw_text('SETTINGS', self.font, self.WHITE, self.screen, 515, 350)
            self.draw_text('COMBOS', self.font, self.WHITE, self.screen, 530, 450)
            self.draw_text('EXIT', self.font, self.WHITE, self.screen, 575, 550)
            if button_1.collidepoint((mx, my)):
                if click:
                    if self.gamemode=="classic":
                        self.game_functions.game_loop()
                        self.game_over(self.game_functions.who_won())
                    else:
                        self.rounds(1)
                        self.game_functions.game_loop()
                        click = True
                        self.tournament_wins.append(self.game_functions.who_won())
                        self.rounds(2)
                        self.game_functions.game_loop()
                        self.tournament_wins.append(self.game_functions.who_won())
                        self.rounds(3)
                        self.game_functions.game_loop()
                        self.tournament_wins.append(self.game_functions.who_won())
                        x = 0
                        y = 0
                        for i in range(0, 1):
                            if self.tournament_wins[i] == 1:
                                x += 1
                            if self.tournament_wins[i] == 2:
                                y += 1
                        if x > y:
                            self.game_over(1)
                        elif x < y:
                            self.game_over(2)
                        else:
                            self.game_over(3)
            if button_2.collidepoint((mx, my)):
                if click:
                    self.key_menu()
            if button_3.collidepoint((mx, my)):
                if click:
                    self.settings_menu()
            if button_4.collidepoint((mx, my)):
                if click:
                    self.combos()
            if button_5.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
            self.clock.tick(60)