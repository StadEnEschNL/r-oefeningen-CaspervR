import pygame
from pygame import Color, Rect, Surface
from environment import Environment
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, rect: Rect):
        self.status = "healthy"
        self.rect = rect
        self.hidden = False

    def update(self, env: Environment):
        pass # TODO

    
    def draw(self, surface: Surface):
        pass # TODO

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

