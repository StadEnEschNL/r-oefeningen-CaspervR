import pygame
from pygame import Rect, Color

class TopSecretSymbol:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, Color(0, 0, 0), self.rect, width=1)
        # TODO: vul hieronder zelf de code aan om de 
        # figuur/cirkel/lijnen te tekenen
        # Gebruik self.rect en self.color


pygame.init()
screen = pygame.display.set_mode([300, 300])
clock = pygame.time.Clock()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(Color(255, 255, 255))
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()

