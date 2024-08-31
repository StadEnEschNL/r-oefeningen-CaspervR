import pygame
from pygame import Color, Rect, Surface
from environment import Environment
import random
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, rect, color):
        self.rect = rect
        self.hidden = False
        self.color = color

    def update(self, env):
        pass
    
    def draw(self, surface):
        surface.fill(self.color)

pygame.init()
screen = pygame.display.set_mode([300, 300])
clock = pygame.time.Clock()
running = True

env = Environment(screen.get_rect())
# TODO aanmaken agents

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # TODO updaten environment

    screen.fill((255, 255, 255))
    env.draw(screen)
    pygame.display.update()

    clock.tick(10)

pygame.quit()

