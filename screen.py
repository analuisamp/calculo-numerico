import pygame
from button import Button
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_plot(screen:pygame.Surface, n: int):
    plot = pygame.image.load(f"images/plot_{n}.png")
    plot_rect = plot.get_rect()
    plot_rect.center = (screen.get_width() / 2, screen.get_height() / 2.4)

    return plot, plot_rect

def bissecao(screen: pygame.Surface):
    sns.set(rc={'figure.figsize':(0.0073125 * screen.get_width(), 0.00918 * screen.get_height())})

    loop = True
    quit_prog = False

    # Carregando imagens dos botões
    img_prox = pygame.image.load("images/proximo_passo.png").convert_alpha()
    img_voltar = pygame.image.load("images/voltar.png").convert_alpha()
    img_prox = pygame.transform.scale_by(img_prox, (1/4 * screen.get_width()) / img_prox.get_width())
    img_voltar = pygame.transform.scale_by(img_voltar, (1/4 * screen.get_width()) / img_voltar.get_width())

    # Criando os botões
    center_x = (screen.get_width() / 2) - (img_prox.get_width() / 2)
    btn_prox = Button(center_x, screen.get_height() * 0.85, img_prox)
    btn_voltar = Button(center_x * 1.9, screen.get_height() * 0.85, img_voltar)


    ###########################################################################
    # Parâmetros do problema
    f = lambda x: 10000 * (np.e ** (-0.48 * x)) - 100
    x0 = 8
    x1 = 12
    tol = 10e-5
    max_iter = 20
    min_x_graph=5
    max_x_graph=20
    ###########################################################################

    conta_graficos = 0
    ###########################################################################
    nums = np.linspace(min_x_graph, max_x_graph, 200) #sequencia de 200 numeros entre 5 e 20
    res = [f(x) for x in nums] #lista com os resultados da função para cada um dos 200 numeros  
    x_span = max_x_graph - min_x_graph # 15 
    y_span = abs(max(res) - min(res)) # Modulo do max e minimo das funções 

    middle_x = np.inf #inf = infinito
    dif_x = np.inf
    reached_tol = False 
    for i in range(max_iter): #Até 20 vezes
        
        plt.clf()
        res = [f(x) for x in nums]
        g = sns.lineplot(x=nums, y=res, label='f(x)') #plot do grafico 
        g.axhline(0, color='r', linestyle='--') # Linha tracejada em 0 
        sns.scatterplot(x=[x0], y=[0], c='green') #plot do ponto Xinf
        if np.abs(x1 - x0) > tol * 1000:
            plt.text(x0 + x_span * 0.03, 0 - y_span * 0.05, '$X^*_{inf}$', fontsize=10) #plot do texto do ponto Xinf
            plt.text(x1 + x_span * 0.03, 0 - y_span * 0.05, '$X^*_{sup}$', fontsize=10) #plot do texto do ponto Xsup
        sns.scatterplot(x=[x1], y=[0], c='green') #plot do ponto Xsup
        plt.savefig(f'images/plot_{conta_graficos}.png') #plot das varias imagens 
        conta_graficos += 1 #passa pra prox imagem
    ###########################################################################

        dif_x = middle_x
        middle_x = (x0 + x1) / 2 #método da divisão da bisseção, primeira iteração = 10 
        dif_x -= middle_x
        dif_x = np.abs(dif_x) / np.abs(middle_x)

        print(f'X_{i}: {middle_x:.6f} | dif: {dif_x}')

        sns.scatterplot(x=[middle_x], y=[0], c='red') # plota o ponto vermelho da bisseção a cada iteração
        plt.text(middle_x + x_span * 0.03, -y_span * 0.05, f'$X_{{{i}}}$', fontsize=10)
        plt.savefig(f'images/plot_{conta_graficos}.png') # salva a imagem com o ponto vermelho
        conta_graficos += 1
        
        #Troca dos pontos 
        # Xsup = X0
        # X1 = middle_x
        if f(middle_x) * f(x0) < 0:
            # Esquerda
            x1 = middle_x
        else:
            # Direita
            x0 = middle_x

        if dif_x < tol:
            reached_tol = True
            steps = i + 1
            break
    
    if not reached_tol:
        steps = max_iter

    contador = 0
    show_res = False
    reload_plot = True
    while loop:
        screen.fill((255, 255, 255))
        
        if reload_plot:
            img_plot, img_plot_rect = load_plot(screen, contador)
            reload_plot = False
        screen.blit(img_plot, img_plot_rect)

        if btn_voltar.run(screen):
            loop = False
        elif btn_prox.run(screen):
            if contador != conta_graficos-1:
                contador += 1
            else:
                contador = 0
            
            reload_plot = True
        
        if contador == conta_graficos - 1 and not show_res:
            font = pygame.font.Font('fonts/BebasNeue-Regular.ttf', screen.get_height() // 16)
            res_text = font.render(f'Raiz: {middle_x:.4f} | {steps} passos', True, (0, 0, 0), None)
            res_text_rect = res_text.get_rect()
            res_text_rect.center = (screen.get_width() / 6, screen.get_height() * 0.902)
            show_res = True
        if show_res:
            screen.blit(res_text, res_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_prog = True
                loop = False
        
        pygame.display.update()

    return quit_prog