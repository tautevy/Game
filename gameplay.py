import random
import time

from fighter import *
import pygame
from pygame.locals import *
from custom_queue import Queue


class Game:
    def __init__(self, Player1_keys, Player2_keys, players, gamemode, player1_name, player2_name):
        # background image
        self.background_img = pygame.image.load('background.jpg').convert_alpha()
        # set framerate
        self.clock = pygame.time.Clock()
        self.fps = 60
        # define colors
        self.RED = (102, 0, 0)
        self.GREEN = (0, 102, 102)
        self.WHITE = (255, 255, 255)
        self.Player1_keys=Player1_keys
        self.Player2_keys=Player2_keys
        self.players=players
        self.gamemode=gamemode
        self.player1_name=player1_name
        self.player2_name=player2_name
        # creating fighters
        self.fighter1 = Fighter(250, 450, 'hero', HERO_DATA, self.Player1_keys)
        self.fighter2 = Fighter(980, 480, 'warrior', WARRIOR_DATA, self.Player2_keys)
        # health
        self.fighter1_health = 100
        self.fighter2_health = 100
        # creating queue
        self.fighter1_queue = Queue()
        self.fighter2_queue = Queue()
        # game variables
        self.computer = False
        self.current_fighter = 1
        self.player1_attack_delay = False
        self.player2_attack_delay = False
        self.player1_attack_cooldown = pygame.USEREVENT + 2
        self.player2_attack_cooldown = pygame.USEREVENT + 2
        self.fighter1_alive = True
        self.fighter2_alive = True
        self.screen = pygame.display.set_mode((1280, 700))
        self.win=0
        self.run = True
        self.event_key=""
        self.combo=False
        # function for drawing background
    # create function for drawing text
    def draw_text(self, text, x, y):
        font = pygame.font.Font('8-BIT WONDER.TTF', 26)
        img = font.render(text, True, (255, 255, 255))
        screen.blit(img, (x, y))
    def draw_bg(self):
        screen.blit(self.background_img, (0, 0))
    # function for drawing health bars
    def draw_health_bar(self, health, x, y):
        ratio = health / 100
        pygame.draw.rect(self.screen, self.WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self.screen, self.RED, (x, y, 400, 30))
        pygame.draw.rect(self.screen, self.GREEN, (x, y, 400 * ratio, 30))

    def combo_attack(self):
        temp=[]
        #current_time = pygame.time.get_ticks()
        #message_end_time = pygame.time.get_ticks() + 3000
        if self.current_fighter == 1:
            while not self.fighter1_queue.is_empty():
                temp.append(self.fighter1_queue.peek())
                self.fighter1_queue.dequeue()
            if temp[0] == self.Player1_keys[0] and temp[1] == self.Player1_keys[1] and temp[2] == self.Player1_keys[2]:  # ULTIMA M+S+P
                self.fighter1.combo_attack()
                self.fighter2_health -= 40
                print("Ultima")
            elif temp[0] == self.Player1_keys[1] and temp[1] == self.Player1_keys[1] and temp[2] == self.Player1_keys[1]:  # Staby Stab S+S+S
                self.fighter1.combo_attack()
                self.fighter2_health -= 20
                print("StabyStab")
            elif temp[0] == self.Player1_keys[1] and temp[1] == self.Player1_keys[0] and temp[2] == self.Player1_keys[0]:  # Magic Sword S+M+M
                self.fighter1.combo_attack()
                self.fighter2_health -= 30
                print("MagicSword")
            else:
                self.fighter1.attack()
                self.fighter2_health -= 10
        elif self.current_fighter == 2:
            while not self.fighter2_queue.is_empty():
                temp.append(self.fighter2_queue.peek())
                self.fighter2_queue.dequeue()
            if temp[0] == self.Player2_keys[0] and temp[1] == self.Player2_keys[1] and temp[2] == self.Player2_keys[2]:  # ULTIMA M+S+P
                self.fighter2.combo_attack()
                self.fighter1_health -= 40
                print("Ultima")
            elif temp[0] == self.Player2_keys[1] and temp[1] == self.Player2_keys[1] and temp[2] == self.Player2_keys[1]:  # Staby Stab S+S+S
                self.fighter2.combo_attack()
                self.fighter1_health -= 20
                print("StabyStab")
            elif temp[0] == self.Player2_keys[1] and temp[1] == self.Player2_keys[0] and temp[2] == self.Player2_keys[0]:  # Magic Sword S+M+M
                self.fighter2.combo_attack()
                self.fighter1_health -= 30
                print("MagicSword")
            else:
                self.fighter2.attack()
                self.fighter1_health -= 10

    def action_attack(self):
        if self.current_fighter==1:
            if self.event_key in self.Player1_keys and self.player1_attack_delay == False:
                pygame.time.set_timer(self.player1_attack_cooldown, 600)
                self.player1_attack_delay = True
                if len(self.fighter1_queue) == 2:
                    self.fighter1_queue.enqueue(self.event_key)
                    self.fighter2.get_hurt()
                else:
                    self.fighter1.attack()
                    self.fighter2.get_hurt()
                    self.fighter1_queue.enqueue(self.event_key)
                    self.fighter2_health -= 10
                self.current_fighter = 2
        elif self.current_fighter == 2:
            if self.event_key in self.Player2_keys and self.player2_attack_delay == False:
                pygame.time.set_timer(self.player2_attack_cooldown, 600)
                self.player2_attack_delay = True
                if len(self.fighter2_queue) == 2:
                    self.fighter2_queue.enqueue(self.event_key)
                    self.fighter1.get_hurt()
                else:
                    self.fighter2.attack()
                    self.fighter1.get_hurt()
                    self.fighter2_queue.enqueue(self.event_key)
                    self.fighter1_health -= 10
                self.current_fighter = 1

    def who_won(self):
        return self.win

    def game_loop(self):
        # if tournament mode
        # if classic mode
        pygame.time.set_timer(pygame.USEREVENT, 800)
        while self.run:
            if self.fighter1_alive == False or self.fighter2_alive == False:
                self.run = False
            self.clock.tick(self.fps)
            # draw background
            self.draw_bg()
            # draw healthbar
            self.draw_health_bar(self.fighter1_health, 50, 20)
            self.draw_health_bar(self.fighter2_health, 820, 20)
            # draw fighters
            self.fighter1.update()
            self.fighter1.draw()
            self.fighter2.update()
            self.fighter2.draw()

            # player action
            if self.players == 2:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.run = False
                    if event.type == self.player1_attack_cooldown:
                        self.player1_attack_delay = False
                    if event.type == self.player2_attack_cooldown:
                        self.player2_attack_delay = False
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            self.run = False
                        self.event_key=pygame.key.name(event.key)
                        self.action_attack()
                    if self.fighter1_health <= 0 < self.fighter2_health:
                            self.fighter1_alive = False
                            self.fighter1.die()
                            self.win=2;
                            break
                    elif self.fighter1_health > 0 >= self.fighter2_health:
                            self.fighter2_alive = False
                            self.fighter2.die()
                            self.win=1;
                            break
            if self.players == 1:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        self.run = False
                    if event.type == self.player1_attack_cooldown:
                        self.player1_attack_delay = False
                    if event.type == self.player2_attack_cooldown:
                        self.player2_attack_delay = False
                    if event.type == KEYDOWN and self.computer == False:
                        if event.key == K_ESCAPE:
                            self.run = False
                        self.event_key = pygame.key.name(event.key)
                        self.action_attack()
                        self.computer = True
                    if event.type == pygame.USEREVENT and self.computer == True:
                        self.event_key = random.choice(self.Player2_keys)
                        self.action_attack()
                        self.computer = False
                    if self.fighter1_health <= 0 < self.fighter2_health:
                        self.fighter1_alive = False
                        self.fighter1.die()
                        self.win = 2
                        break
                    elif self.fighter1_health > 0 >= self.fighter2_health:
                        self.fighter2_alive = False
                        self.fighter2.die()
                        self.win = 1
                        break
            pygame.display.update()
            self.clock.tick(60)
