import pygame

class Button():
    def __init__(self, x, y, img):
        self.img = img
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def run(self, screen):
        trigger = False

        # Checar mouse
        mouse_pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                trigger = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Desenha botão na tela
        screen.blit(self.img, (self.rect.x, self.rect.y))

        return trigger

