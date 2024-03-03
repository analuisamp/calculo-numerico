import pygame
from button import Button
from screen import bissecao

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Projeto 1 - Cálculo numérico')

# Carrega imagens
img_bissecao = pygame.image.load("images/btn_bissecao.png").convert_alpha()
img_bissecao = pygame.transform.scale_by(img_bissecao, (1/3 * SCREEN_WIDTH) / img_bissecao.get_width())

# Texto
font = pygame.font.Font('fonts/BebasNeue-Regular.ttf', SCREEN_HEIGHT // 9)
res_text = font.render('Cálculo Numérico', True, (0, 0, 0), None)
res_text_rect = res_text.get_rect()
res_text_rect.center = (SCREEN_WIDTH / 2, res_text_rect.height)

font_subtitle = pygame.font.Font('fonts/BebasNeue-Regular.ttf', SCREEN_HEIGHT // 15)
subtitle = font_subtitle.render('Projeto 1', True, (0, 0, 0), None)
subtitle_rect = subtitle.get_rect()
subtitle_rect.center = (SCREEN_WIDTH / 2, res_text_rect.centery + (res_text_rect.height / 1.8))

center_x = (SCREEN_WIDTH / 2) - (img_bissecao.get_width() / 2)
first_button_y = (SCREEN_HEIGHT / 6) * 2

# Criando os botões
btn_bissecao = Button(center_x, first_button_y, img_bissecao)

def menu():
    run = True
    quit_prog = False

    while run:

        screen.fill((240, 240, 240))
        screen.blit(res_text, res_text_rect)
        screen.blit(subtitle, subtitle_rect)

        if btn_bissecao.run(screen):
            print('Bissecao')
            bissecao(screen)

        if quit_prog:
            run = False

        # Event handler
        for event in pygame.event.get():
            # Sair
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()

    pygame.quit()


menu()