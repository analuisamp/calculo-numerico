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

def newton(screen: pygame.Surface):
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
    f_linha = lambda x: -4800 * (np.e ** (-0.48 * x))
    x0 = 8
    tol = 10e-5
    max_iter = 20
    min_x_graph=5
    max_x_graph=20
    ###########################################################################

    approx = x0

    nums = np.linspace(min_x_graph, max_x_graph, 200)
    res = [f(x) for x in nums]
    x_span = max_x_graph - min_x_graph
    y_span = abs(max(res) - min(res))

    plt.clf()
    g = sns.lineplot(x=nums, y=res, label='f(x)')
    g.axhline(0, color='r', linestyle='--');
    sns.scatterplot(x=[approx], y=[f(approx)], c='red')
    plt.text(approx + x_span * 0.03, f(approx) - y_span * 0.05, 'Ponto inicial', fontsize=10)
    plt.savefig('images/plot_0.png')
    ###########################################################################

    print(f'{0}: - X = {approx} | f(X) = {f(approx)}')

    dif_x = np.inf
    reached_tol = False
    steps = 0
    for i in range(max_iter):

        reta_tan = lambda x: f_linha(approx) * (x - approx) + f(approx)

        plt.clf()
        g = sns.lineplot(x=nums, y=res, label='f(x)')
        g.axhline(0, color='r', linestyle='--');
        sns.lineplot(x=nums, y=[reta_tan(x) for x in nums], color='orange', label=f"Reta tangente no ponto x = {approx:.2f}")
        sns.scatterplot(x=[approx], y=[f(approx)], c='red')
        if dif_x >= tol * 100:
            plt.text(approx + x_span * 0.03, f(approx) - y_span * 0.05, f'$X_{i}$', fontsize=10)

        dif_x = approx
        approx = approx - f(approx) / f_linha(approx)
        dif_x -= approx; dif_x = np.abs(dif_x) / np.abs(approx)

        sns.scatterplot(x=[approx], y=[0], c='red')
        if dif_x >= tol * 100:
            plt.text(approx + x_span * 0.03, 0 - y_span * 0.05, f'$X_{i+1}$', fontsize=10)
        g.vlines(approx, ymin=min([f(approx), 0]), ymax=max([f(approx), 0]), linestyles='dotted')

        plt.savefig(f'images/plot_{i+1}.png')

        print(f'{i+1}: - X = {approx} | f(X) = {f(approx)} | diff = {dif_x}')

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
            if contador != steps:
                contador += 1
            else:
                contador = 0
            
            reload_plot = True
        
        if contador == steps and not show_res:
            font = pygame.font.Font('fonts/timesnewroman.ttf', screen.get_height() // 16)
            res_text = font.render(f'Raiz: {approx:.4f} | {steps} passos', True, (0, 0, 0), None)
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
    # I = I0 * np.e ** (u*p*x)
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
    nums = np.linspace(min_x_graph, max_x_graph, 200)
    res = [f(x) for x in nums]
    x_span = max_x_graph - min_x_graph
    y_span = abs(max(res) - min(res))

    middle_x = np.inf
    dif_x = np.inf
    reached_tol = False
    for i in range(max_iter):
        
        plt.clf()
        res = [f(x) for x in nums]
        g = sns.lineplot(x=nums, y=res, label='f(x)')
        g.axhline(0, color='r', linestyle='--');
        sns.scatterplot(x=[x0], y=[0], c='green')
        if np.abs(x1 - x0) > tol * 1000:
            plt.text(x0 + x_span * 0.03, 0 - y_span * 0.05, '$X^*_{inf}$', fontsize=10)
            plt.text(x1 + x_span * 0.03, 0 - y_span * 0.05, '$X^*_{sup}$', fontsize=10)
        sns.scatterplot(x=[x1], y=[0], c='green')
        plt.savefig(f'images/plot_{conta_graficos}.png')
        conta_graficos += 1
    ###########################################################################

        dif_x = middle_x
        middle_x = (x0 + x1) / 2
        dif_x -= middle_x; dif_x = np.abs(dif_x) / np.abs(middle_x)

        print(f'X_{i}: {middle_x:.6f} | dif: {dif_x}')

        sns.scatterplot(x=[middle_x], y=[0], c='red')
        plt.text(middle_x + x_span * 0.03, -y_span * 0.05, f'$X_{{{i}}}$', fontsize=10)
        plt.savefig(f'images/plot_{conta_graficos}.png')
        conta_graficos += 1

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
            font = pygame.font.Font('fonts/timesnewroman.ttf', screen.get_height() // 16)
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

def secante(screen: pygame.Surface):
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

    approx = x1

    nums = np.linspace(min_x_graph, max_x_graph, 200)
    res = [f(x) for x in nums]
    x_span = max_x_graph - min_x_graph
    y_span = abs(max(res) - min(res))

    plt.clf()
    g = sns.lineplot(x=nums, y=res, label='f(x)')
    g.axhline(0, color='r', linestyle='--');
    sns.scatterplot(x=[x0], y=[f(x0)], c='green')
    sns.scatterplot(x=[x1], y=[f(x1)], c='green')
    plt.text(x0 + x_span * 0.03, f(x0) - y_span * 0.05, '$X_0$', fontsize=10)
    plt.text(x1 + x_span * 0.03, f(x1) - y_span * 0.05, '$X_1$', fontsize=10)
    plt.savefig('images/plot_0.png')
    ###########################################################################

    print(f'{0}: - X = {approx} | f(X) = {f(approx)}')

    dif_x = np.inf
    reached_tol = False
    steps = 0
    for i in range(max_iter):

        m = (f(x1) - f(x0)) / (x1 - x0)
        reta_secante = lambda x: m * (x - x0) + f(x0)

        plt.clf()
        g = sns.lineplot(x=nums, y=res, label='f(x)')
        g.axhline(0, color='r', linestyle='--');
        sns.lineplot(x=nums, y=[reta_secante(x) for x in nums], color='orange', label=f"Reta secante")
        sns.scatterplot(x=[x1], y=[f(x1)], c='green')
        sns.scatterplot(x=[x0], y=[f(x0)], c='green')
        if dif_x >= tol * 100:
            plt.text(x0 + x_span * 0.03, f(x0) - y_span * 0.05, f'$X_{i}$', fontsize=10)
            plt.text(x1 + x_span * 0.03, f(x1) - y_span * 0.05, f'$X_{i + 1}$', fontsize=10)

        dif_x = approx
        approx = (x0*f(x1) - x1*f(x0))/(f(x1) - f(x0))
        dif_x -= approx; dif_x = np.abs(dif_x) / np.abs(approx)

        x0, x1 = x1, approx

        sns.scatterplot(x=[approx], y=[0], c='red')
        sns.scatterplot(x=[approx], y=[f(approx)], c='red')
        plt.text(approx + x_span * 0.03, 0 - y_span * 0.05, f'$X_{i + 2}$', fontsize=10)
        # if dif_x >= tol * 100:
        #     plt.text(approx + x_span * 0.03, 0 - y_span * 0.05, f'$X_{i+1}$', fontsize=10)
        g.vlines(approx, ymin=min([f(approx), 0]), ymax=max([f(approx), 0]), linestyles='dotted')

        plt.savefig(f'images/plot_{i+1}.png')

        print(f'{i+1}: - X = {approx} | f(X) = {f(approx)} | diff = {dif_x}')

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
            if contador != steps:
                contador += 1
            else:
                contador = 0
            
            reload_plot = True
        
        if contador == steps and not show_res:
            font = pygame.font.Font('fonts/timesnewroman.ttf', screen.get_height() // 16)
            res_text = font.render(f'Raiz: {approx:.4f} | {steps} passos', True, (0, 0, 0), None)
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