import pygame
import sys

pygame.mixer.init()
pygame.init()
size = (200, 200)
screen = pygame.display.set_mode(size)
LEFT = 1
s = pygame.mixer.Sound("shootsfx.mp3")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            print ("click")
            s.play()