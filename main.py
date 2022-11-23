from menus import *


#set framerate
clock = pygame.time.Clock()
font = pygame.font.Font('8-BIT WONDER.TTF', 32)

#game window
screen_width = 1280
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')


#background image
background_img = pygame.image.load('background.jpg').convert_alpha()
menus=Choices(screen, clock, background_img, font)

#game loop
menus.main_menu()
