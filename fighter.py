import pygame
#game window
screen_width = 1280
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')
#define fighter elements
WARRIOR_SIZE=162
HERO_SIZE=200
WARRIOR_SCALE = 7
HERO_SCALE=6
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE]
HERO_DATA = [HERO_SIZE, HERO_SCALE]
#define action steps
warrior_IDLE_STEPS=10
hero_IDLE_STEPS=4
warrior_ATTACK_STEPS=7
warrior_HURT_STEPS=3
warrior_DEAD_STEPS=7
hero_ATTACK_STEPS=4
hero_HURT_STEPS=3
hero_DEAD_STEPS=7
#load spritesheets for fighters
hero_sheet_idle=pygame.image.load('Martial Hero 2/Sprites/Idle.png').convert_alpha()
hero_sheet_attack=pygame.image.load('Martial Hero 2/Sprites/Attack1.png').convert_alpha()
hero_sheet_hurt=pygame.image.load('Martial Hero 2/Sprites/Take hit.png').convert_alpha()
hero_sheet_dead=pygame.image.load('Martial Hero 2/Sprites/Death.png').convert_alpha()
hero_sheet_attack1=pygame.image.load('Martial Hero 2/Sprites/Attack2.png').convert_alpha()
warrior_sheet_idle=pygame.image.load('Fantasy Warrior/Sprites/Idle.png').convert_alpha()
warrior_sheet_attack=pygame.image.load('Fantasy Warrior/Sprites/Attack1.png').convert_alpha()
warrior_sheet_hurt=pygame.image.load('Fantasy Warrior/Sprites/Take hit.png').convert_alpha()
warrior_sheet_dead=pygame.image.load('Fantasy Warrior/Sprites/Death.png').convert_alpha()
warrior_sheet_attack1=pygame.image.load('Fantasy Warrior/Sprites/Attack2.png').convert_alpha()
#fighter class
class Fighter():
    def __init__(self, x, y, name, data, keys):
        self.player=1
        self.keys=keys #0:Magic 1:Sword 2:Potion
        self.name=name
        self.shoot_cooldown = pygame.USEREVENT +2
        self.size = data[0]
        self.image_scale = data[1]
        self.animation_list=[]
        self.alive=True
        self.health=100
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:hurt, 2:attack, 3:dead
        self.update_time = pygame.time.get_ticks()
        # load images
        if self.name == "hero":
            self.animation_list.append(self.load_images(hero_sheet_idle, hero_IDLE_STEPS))
            self.animation_list.append(self.load_images(hero_sheet_hurt, hero_HURT_STEPS))
            self.animation_list.append(self.load_images(hero_sheet_attack, hero_ATTACK_STEPS))
            self.animation_list.append(self.load_images(hero_sheet_dead, hero_DEAD_STEPS))
            self.animation_list.append(self.load_images(hero_sheet_attack1, hero_ATTACK_STEPS))
        elif self.name == "warrior":
            self.animation_list.append(self.load_images(warrior_sheet_idle, warrior_IDLE_STEPS))
            self.animation_list.append(self.load_images(warrior_sheet_hurt, warrior_HURT_STEPS))
            self.animation_list.append(self.load_images(warrior_sheet_attack, warrior_ATTACK_STEPS))
            self.animation_list.append(self.load_images(warrior_sheet_dead, warrior_DEAD_STEPS))
            self.animation_list.append(self.load_images(warrior_sheet_attack1, warrior_ATTACK_STEPS))
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def load_images(self, sprite_sheet, animation_steps):
        img_list=[]
        for x in range(animation_steps):
            temp_img=sprite_sheet.subsurface(x * self.size, 0, self.size, self.size)
            img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
        return img_list
    def draw(self):
        screen.blit(self.image, self.rect)
    def update(self):
        animation_cooldown = 100
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()
    def idle(self):
        # set variables to attack animation
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    def attack(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    def combo_attack(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    def get_hurt(self):
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    def die(self):
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

