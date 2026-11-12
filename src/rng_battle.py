import pygame
import random
import math

def main():
    pygame.init()
    pygame.display.set_caption("RNG Battle")
    resoution = (800, 600)
    screen = pygame.display.set_mode(resoution)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('Blue')
    pygame.quit()


if __name__ == "__main__":
    main()