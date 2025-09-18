import pygame
import os
import json
import random
import time
import math

# Configurações iniciais
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
SAVE_FILE = os.path.join(BASE_DIR, "save_game.json")

# Inicialização do Pygame
pygame.init()
pygame.font.init()

# Obter informações do monitor
info = pygame.display.Info()
LARGURA, ALTURA = info.current_w, info.current_h
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("My Clicker")
relogio = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
CINZA_ESCURO = (100, 100, 100)
VERMELHO = (255, 0, 0)
VERDE = (0, 200, 0)
AZUL = (0, 120, 255)
LARANJA = (255, 165, 0)
ROXO = (128, 0, 128)

# Variáveis do jogo
pontos = 0
cursores = 0
spaceships = 0
pcursores = 5
pspaceships = 50
loja_aberta = False
spaceship_animations = []
botao_upgradado = False
mensagem_temporaria = ""
mensagem_tempo = 0
botao_clique_pressionado = False
botao_clique_tempo = 0

# Variáveis para controle de clique
clique_liberado = True
mouse_pressionado = False

# Sistema de inflação/deflação complexo
intervalo_inflacao = 180000  # 3 minutos em milissegundos
ultimo_periodo_inflacao = 0
proximo_periodo_inflacao = 0
compras_periodo_cursor = 0
compras_periodo_spaceship = 0
compras_anteriores_cursor = 0
compras_anteriores_spaceship = 0
mensagens_inflacao = {"cursor": "", "spaceship": ""}
tempo_mensagens_inflacao = {"cursor": 0, "spaceship": 0}

# Fontes
fonte_titulo = pygame.font.SysFont("comicsansms", 60, bold=True)
fonte_grande = pygame.font.SysFont("comicsansms", 30)
fonte_media = pygame.font.SysFont("comicsansms", 24)
fonte_pequena = pygame.font.SysFont("comicsansms", 20)
fonte_muito_pequena = pygame.font.SysFont("comicsansms", 16)

# Funções de utilidade
def carregar_imagem(nome_arquivo, tamanho=(30, 30)):
    """Carrega uma imagem da pasta images com fallback para cor sólida"""
    caminho = os.path.join(IMAGE_DIR, nome_arquivo)
    try:
        if os.path.exists(caminho):
            img = pygame.image.load(caminho).convert_alpha()
            return pygame.transform.scale(img, tamanho)
        else:
            surf = pygame.Surface(tamanho, pygame.SRCALPHA)
            if "cursor" in nome_arquivo:
                surf.fill((0, 0, 255, 255))
            elif "spaceship" in nome_arquivo:
                surf.fill((0, 255, 0, 255))
            else:
                surf.fill((255, 0, 0, 255))
            return surf
    except Exception as e:
        print(f"Erro ao carregar imagem {nome_arquivo}: {e}")
        surf = pygame.Surface(tamanho, pygame.SRCALPHA)
        surf.fill((255, 0, 0, 255))
        return surf

# Carregar todas as imagens
cursor_icon = carregar_imagem("cursor.png", (60, 60))
spaceship_icon = carregar_imagem("spaceship.png", (60, 60))
click_icon = carregar_imagem("click_button.png", (300, 100))
buy_icon = carregar_imagem("buy_button.png", (200, 30))
buy_spaceship_icon = carregar_imagem("buy_spaceship_button.png", (200, 30))
click_pressed_icon = carregar_imagem("click_button_pressed.png", (300, 100))
buy_pressed_icon = carregar_imagem("buy_button_pressed.png", (200, 30))
buy_spaceship_pressed_icon = carregar_imagem("buy_spaceship_button_pressed.png", (200, 30))
loja_icon = carregar_imagem("loja_icon.png", (64, 64))
save_icon = carregar_imagem("save_icon.png", (64, 64))
load_icon = carregar_imagem("load_icon.png", (64, 64))
click_upgraded_icon = carregar_imagem("click_button_upgraded.png", (300, 100))
click_upgraded_pressed_icon = carregar_imagem("click_button_upgraded_pressed.png", (300, 100))

# Fallback para imagens
if buy_pressed_icon.get_size() == (1, 1):
    buy_pressed_icon = pygame.Surface((200, 30))
    buy_pressed_icon.fill(CINZA_ESCURO)
    
if buy_spaceship_pressed_icon.get_size() == (1, 1):
    buy_spaceship_pressed_icon = pygame.Surface((200, 30))
    buy_spaceship_pressed_icon.fill(CINZA_ESCURO)

if click_pressed_icon.get_size() == (1, 1):
    click_pressed_icon = pygame.Surface((300, 100))
    click_pressed_icon.fill(CINZA_ESCURO)

if click_upgraded_icon.get_size() == (1, 1):
    click_upgraded_icon = pygame.Surface((300, 100))
    click_upgraded_icon.fill((150, 100, 200))

if click_upgraded_pressed_icon.get_size() == (1, 1):
    click_upgraded_pressed_icon = pygame.Surface((300, 100))
    click_upgraded_pressed_icon.fill((100, 50, 150))

# Funções do jogo
def salvar_jogo():
    """Salva o progresso do jogo em um arquito JSON"""
    global mensagem_temporaria, mensagem_tempo
    
    try:
        dados = {
            "pontos": pontos,
            "cursores": cursores,
            "spaceships": spaceships,
            "pcursores": pcursores,
            "pspaceships": pspaceships,
            "botao_upgradado": botao_upgradado,
            "ultimo_periodo_inflacao": ultimo_periodo_inflacao,
            "compras_periodo_cursor": compras_periodo_cursor,
            "compras_periodo_spaceship": compras_periodo_spaceship,
            "compras_anteriores_cursor": compras_anteriores_cursor,
            "compras_anteriores_spaceship": compras_anteriores_spaceship
        }
        
        with open(SAVE_FILE, 'w') as f:
            json.dump(dados, f)
        
        mensagem_temporaria = "Jogo salvo com sucesso!"
        mensagem_tempo = pygame.time.get_ticks()
        
    except Exception as e:
        mensagem_temporaria = f"Erro ao salvar: {e}"
        mensagem_tempo = pygame.time.get_ticks()

def carregar_jogo():
    """Carrega o progresso do jogo do arquivo de salvamento"""
    global pontos, cursores, spaceships, pcursores, pspaceships, botao_upgradado
    global mensagem_temporaria, mensagem_tempo, ultimo_periodo_inflacao
    global compras_periodo_cursor, compras_periodo_spaceship, proximo_periodo_inflacao
    global compras_anteriores_cursor, compras_anteriores_spaceship
    
    try:
        if not os.path.exists(SAVE_FILE):
            mensagem_temporaria = "Nenhum arquivo de salvamento encontrado!"
            mensagem_tempo = pygame.time.get_ticks()
            return
        
        with open(SAVE_FILE, 'r') as f:
            dados = json.load(f)
        
        pontos = dados["pontos"]
        cursores = dados["cursores"]
        spaceships = dados["spaceships"]
        pcursores = dados["pcursores"]
        pspaceships = dados["pspaceships"]
        botao_upgradado = dados.get("botao_upgradado", False)
        ultimo_periodo_inflacao = dados.get("ultimo_periodo_inflacao", 0)
        compras_periodo_cursor = dados.get("compras_periodo_cursor", 0)
        compras_periodo_spaceship = dados.get("compras_periodo_spaceship", 0)
        compras_anteriores_cursor = dados.get("compras_anteriores_cursor", 0)
        compras_anteriores_spaceship = dados.get("compras_anteriores_spaceship", 0)
        
        proximo_periodo_inflacao = ultimo_periodo_inflacao + intervalo_inflacao
        
        spaceship_animations.clear()
        for _ in range(spaceships):
            adicionar_spaceship_animacao()
        
        mensagem_temporaria = "Jogo carregado com sucesso!"
        mensagem_tempo = pygame.time.get_ticks()
        
    except Exception as e:
        mensagem_temporaria = f"Erro ao carregar: {e}"
        mensagem_tempo = pygame.time.get_ticks()

def comprar_upgrade_secreto():
    """Função para comprar o upgrade secreto do botão de clique"""
    global pontos, botao_upgradado, mensagem_temporaria, mensagem_tempo
    
    if pontos >= 45:
        pontos -= 45
        botao_upgradado = True
        mensagem_temporaria = "Upgrade secreto ativado! +3 pontos por clique!"
        mensagem_tempo = pygame.time.get_ticks()
    else:
        mensagem_temporaria = "Pontos insuficientes para o upgrade!"
        mensagem_tempo = pygame.time.get_ticks()

def adicionar_spaceship_animacao():
    """Adiciona uma nova spaceship para animação"""
    x = random.randint(100, LARGURA - 100)
    y = random.randint(ALTURA // 2, ALTURA - 100)
    speed = random.uniform(1.5, 3.0)
    spaceship_animations.append({"x": x, "y": y, "speed": speed})

def clicker():
    """Função que aumenta pontos automaticamente baseado nos cursores e spaceships"""
    global pontos
    pontos += 5 * cursores
    pontos += 20 * spaceships

def clique():
    """Aumenta pontos ao clicar manualmente ou pressionar espaço"""
    global pontos, botao_clique_pressionado, botao_clique_tempo
    
    if botao_upgradado:
        pontos += 3
    else:
        pontos += 1
        
    botao_clique_pressionado = True
    botao_clique_tempo = pygame.time.get_ticks()

def buy_cursor():
    """Compra um cursor se tiver pontos suficientes"""
    global cursores, pontos, pcursores, mensagem_temporaria, mensagem_tempo
    global compras_periodo_cursor
    
    if pontos >= pcursores:
        pontos -= pcursores
        cursores += 1
        compras_periodo_cursor += 1
        pcursores = int(pcursores + pcursores * 0.15)
        mensagem_temporaria = "Cursor comprado!"
        mensagem_tempo = pygame.time.get_ticks()
    else:
        mensagem_temporaria = "Pontos insuficientes!"
        mensagem_tempo = pygame.time.get_ticks()

def buy_spaceship():
    """Compra uma spaceship se tiver pontos suficientes"""
    global spaceships, pontos, pspaceships, mensagem_temporaria, mensagem_tempo
    global compras_periodo_spaceship
    
    if pontos >= pspaceships:
        pontos -= pspaceships
        spaceships += 1
        compras_periodo_spaceship += 1
        pspaceships = int(pspaceships + pspaceships * 0.25)
        adicionar_spaceship_animacao()
        mensagem_temporaria = "Spaceship comprada!"
        mensagem_tempo = pygame.time.get_ticks()
    else:
        mensagem_temporaria = "Pontos insuficientes!"
        mensagem_tempo = pygame.time.get_ticks()

def calcular_inflacao():
    """Calcula e aplica a inflação/deflação baseada nas compras dos períodos"""
    global pcursores, pspaceships, compras_periodo_cursor, compras_periodo_spaceship
    global compras_anteriores_cursor, compras_anteriores_spaceship
    global mensagens_inflacao, tempo_mensagens_inflacao
    
    # Calcular variação para cursores
    if compras_anteriores_cursor > 0:
        # Calcular diferença em relação ao período anterior
        diferenca_cursor = compras_anteriores_cursor - compras_periodo_cursor 
        variacao_cursor = diferenca_cursor * 2  # 2% por unidade de diferença
        
        # Aplicar variação (pode ser positiva ou negativa)
        if variacao_cursor != 0:
            novo_preco_cursor = pcursores * (1 + variacao_cursor / 100)
            pcursores = max(1, int(novo_preco_cursor))
            
            if variacao_cursor > 0:
                mensagens_inflacao["cursor"] = f"Cursor +{variacao_cursor}%"
            else:
                mensagens_inflacao["cursor"] = f"Cursor {variacao_cursor}%"
            
            tempo_mensagens_inflacao["cursor"] = pygame.time.get_ticks()
            print(f"Variação Cursor: {variacao_cursor}%")
    else:
        # Primeiro período ou período sem compras anteriores: aplicar -10%
        if compras_periodo_cursor == 0:
            pcursores = max(1, int(pcursores * 0.9))
            mensagens_inflacao["cursor"] = "Cursor -10% (estoque)"
            tempo_mensagens_inflacao["cursor"] = pygame.time.get_ticks()
            print("Cursor: -10% (excesso de estoque)")
    
    # Calcular variação para spaceships
    if compras_anteriores_spaceship > 0:
        # Calcular diferença em relação ao período anterior
        diferenca_spaceship = compras_anteriores_spaceship - compras_periodo_spaceship
        variacao_spaceship = diferenca_spaceship * 2  # 2% por unidade de diferença
        
        # Aplicar variação (pode ser positiva ou negativa)
        if variacao_spaceship != 0:
            novo_preco_spaceship = pspaceships * (1 + variacao_spaceship / 100)
            pspaceships = max(1, int(novo_preco_spaceship))
            
            if variacao_spaceship > 0:
                mensagens_inflacao["spaceship"] = f"Spaceship +{variacao_spaceship}%"
            else:
                mensagens_inflacao["spaceship"] = f"Spaceship {variacao_spaceship}%"
            
            tempo_mensagens_inflacao["spaceship"] = pygame.time.get_ticks()
            print(f"Variação Spaceship: {variacao_spaceship}%")
    else:
        # Primeiro período ou período sem compras anteriores: aplicar -10%
        if compras_periodo_spaceship == 0:
            pspaceships = max(1, int(pspaceships * 0.9))
            mensagens_inflacao["spaceship"] = "Spaceship -10% (estoque)"
            tempo_mensagens_inflacao["spaceship"] = pygame.time.get_ticks()
            print("Spaceship: -10% (excesso de estoque)")
    
    # Atualizar compras anteriores para o próximo período
    compras_anteriores_cursor = compras_periodo_cursor
    compras_anteriores_spaceship = compras_periodo_spaceship
    
    # Resetar contadores do período atual
    compras_periodo_cursor = 0
    compras_periodo_spaceship = 0

def toggle_loja():
    """Abre ou fecha a loja"""
    global loja_aberta
    loja_aberta = not loja_aberta

def desenhar_botao(surface, rect, texto, fonte, cor_normal, cor_hover, cor_texto, image=None, pressed=False):
    """Desenha um botão na tela"""
    mouse_pos = pygame.mouse.get_pos()
    
    hover = rect.collidepoint(mouse_pos)
    
    if pressed:
        cor = cor_hover
    elif hover and mouse_pressionado:
        cor = cor_hover
    elif hover:
        cor = cor_hover
    else:
        cor = cor_normal
    
    if image:
        if pressed and image != click_icon and image != click_upgraded_icon:
            dark_image = image.copy()
            dark_image.fill((50, 50, 50, 0), special_flags=pygame.BLEND_RGBA_SUB)
            surface.blit(dark_image, rect)
        else:
            surface.blit(image, rect)
    else:
        pygame.draw.rect(surface, cor, rect, border_radius=10)
        pygame.draw.rect(surface, CINZA_ESCURO, rect, 2, border_radius=10)
    
    if not image and texto:
        texto_surf = fonte.render(texto, True, cor_texto)
        texto_rect = texto_surf.get_rect(center=rect.center)
        surface.blit(texto_surf, texto_rect)
    
    return hover

def desenhar_loja():
    """Desenha a interface da loja"""
    # Fundo da loja
    loja_rect = pygame.Rect(LARGURA // 4, 100, LARGURA // 2, ALTURA - 200)
    pygame.draw.rect(tela, BRANCO, loja_rect, border_radius=15)
    pygame.draw.rect(tela, CINZA_ESCURO, loja_rect, 3, border_radius=15)
    
    # Título da loja
    titulo_texto = fonte_titulo.render("Loja", True, PRETO)
    titulo_rect = titulo_texto.get_rect(center=(LARGURA // 2, 150))
    tela.blit(titulo_texto, titulo_rect)
    
    # Timer de inflação
    tempo_atual = pygame.time.get_ticks()
    tempo_restante = max(0, proximo_periodo_inflacao - tempo_atual)
    minutos_restantes = tempo_restante // 60000
    segundos_restantes = (tempo_restante % 60000) // 1000
    
    timer_texto = fonte_pequena.render(f"Próximo ajuste: {minutos_restantes:02d}:{segundos_restantes:02d}", True, ROXO)
    timer_rect = timer_texto.get_rect(center=(LARGURA // 2, 190))
    tela.blit(timer_texto, timer_rect)
    
    # Compras no período
    compras_texto = fonte_muito_pequena.render(f"Compras: Cursor({compras_periodo_cursor}/+{compras_periodo_cursor*2}%) Spaceship({compras_periodo_spaceship}/+{compras_periodo_spaceship*2}%)", True, PRETO)
    compras_rect = compras_texto.get_rect(center=(LARGURA // 2, 210))
    tela.blit(compras_texto, compras_rect)
    
    # Compras período anterior
    if compras_anteriores_cursor > 0 or compras_anteriores_spaceship > 0:
        anteriores_texto = fonte_muito_pequena.render(f"Período anterior: Cursor({compras_anteriores_cursor}) Spaceship({compras_anteriores_spaceship})", True, CINZA_ESCURO)
        anteriores_rect = anteriores_texto.get_rect(center=(LARGURA // 2, 225))
        tela.blit(anteriores_texto, anteriores_rect)
    
    # Item Cursor
    cursor_rect = pygame.Rect(LARGURA // 4 + 50, 240, LARGURA // 2 - 100, 60)
    pygame.draw.rect(tela, CINZA, cursor_rect, border_radius=10)
    
    texto_cursor = fonte_media.render("Cursor", True, PRETO)
    tela.blit(texto_cursor, (cursor_rect.x + 20, cursor_rect.y + 15))
    
    texto_preco = fonte_media.render(f"Preço: {pcursores}pts", True, PRETO)
    tela.blit(texto_preco, (cursor_rect.x + 200, cursor_rect.y + 15))
    
    # Mensagem de inflação do cursor
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - tempo_mensagens_inflacao["cursor"] < 3000 and mensagens_inflacao["cursor"]:
        cor_inflacao = VERMELHO if "+" in mensagens_inflacao["cursor"] else VERDE
        inflacao_texto = fonte_muito_pequena.render(mensagens_inflacao["cursor"], True, cor_inflacao)
        tela.blit(inflacao_texto, (cursor_rect.x + 20, cursor_rect.y + 40))
    
    botao_cursor_rect = pygame.Rect(cursor_rect.right - 220, cursor_rect.y + 15, 200, 30)
    hover_cursor = desenhar_botao(tela, botao_cursor_rect, "Comprar", fonte_pequena, VERDE, (0, 150, 0), BRANCO, buy_icon)
    
    # Item Spaceship
    spaceship_rect = pygame.Rect(LARGURA // 4 + 50, 320, LARGURA // 2 - 100, 60)
    pygame.draw.rect(tela, CINZA, spaceship_rect, border_radius=10)
    
    texto_spaceship = fonte_media.render("Spaceship", True, PRETO)
    tela.blit(texto_spaceship, (spaceship_rect.x + 20, spaceship_rect.y + 15))
    
    texto_preco_sp = fonte_media.render(f"Preço: {pspaceships}pts", True, PRETO)
    tela.blit(texto_preco_sp, (spaceship_rect.x + 200, spaceship_rect.y + 15))
    
    # Mensagem de inflação da spaceship
    if tempo_atual - tempo_mensagens_inflacao["spaceship"] < 3000 and mensagens_inflacao["spaceship"]:
        cor_inflacao = VERMELHO if "+" in mensagens_inflacao["spaceship"] else VERDE
        inflacao_texto = fonte_muito_pequena.render(mensagens_inflacao["spaceship"], True, cor_inflacao)
        tela.blit(inflacao_texto, (spaceship_rect.x + 20, spaceship_rect.y + 40))
    
    botao_spaceship_rect = pygame.Rect(spaceship_rect.right - 220, spaceship_rect.y + 15, 200, 30)
    hover_spaceship = desenhar_botao(tela, botao_spaceship_rect, "Comprar", fonte_pequena, AZUL, (0, 100, 200), BRANCO, buy_spaceship_icon)
    
    # Botão Fechar Loja
    fechar_rect = pygame.Rect(LARGURA // 2 - 100, ALTURA - 150, 200, 50)
    hover_fechar = desenhar_botao(tela, fechar_rect, "Fechar Loja", fonte_media, VERMELHO, (200, 0, 0), BRANCO)
    
    return {
        'cursor': hover_cursor,
        'spaceship': hover_spaceship,
        'fechar': hover_fechar
    }

# Inicializar animações de spaceships
for _ in range(spaceships):
    adicionar_spaceship_animacao()

# Inicializar sistema de inflação
tempo_atual = pygame.time.get_ticks()
if ultimo_periodo_inflacao == 0:
    ultimo_periodo_inflacao = tempo_atual
    proximo_periodo_inflacao = tempo_atual + intervalo_inflacao

# Variáveis para controle de interface
botoes_loja_hover = {'cursor': False, 'spaceship': False, 'fechar': False}
botao_salvar_hover = False
botao_carregar_hover = False
botao_loja_hover = False
botao_clique_hover = False

# Loop principal
executando = True
ultimo_tempo_clique = 0
tempo_inicial = pygame.time.get_ticks()

while executando:
    tempo_atual = pygame.time.get_ticks()
    tempo_decorrido = (tempo_atual - tempo_inicial) / 1000.0
    
    # Verificar período de inflação
    if tempo_atual >= proximo_periodo_inflacao:
        calcular_inflacao()
        ultimo_periodo_inflacao = tempo_atual
        proximo_periodo_inflacao = tempo_atual + intervalo_inflacao
    
    # Atualizar produção automática
    if tempo_decorrido - ultimo_tempo_clique >= 2.5:
        clicker()
        ultimo_tempo_clique = tempo_decorrido
    
    # Processar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            executando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                executando = False
            elif evento.key == pygame.K_SPACE:
                clique()
            elif evento.key == pygame.K_l:
                toggle_loja()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                mouse_pressionado = True
                clique_liberado = False
                x, y = evento.pos
                
                # Botão de clique principal
                botao_clique_rect = pygame.Rect(LARGURA // 2 - 150, ALTURA - 150, 300, 100)
                if botao_clique_rect.collidepoint(x, y):
                    clique()
                
                # Easter egg
                titulo_texto = fonte_titulo.render("My Clicker", True, PRETO)
                titulo_rect = titulo_texto.get_rect(center=(LARGURA // 2, 80))
                ponto_i_x = titulo_rect.right - 30
                if abs(x - ponto_i_x) < 20 and abs(y - titulo_rect.centery) < 20:
                    if pontos == 69 and not botao_upgradado:
                        comprar_upgrade_secreto()
                
                # Botões de controle
                botao_salvar_rect = pygame.Rect(50, ALTURA - 100, 64, 64)
                if botao_salvar_rect.collidepoint(x, y):
                    salvar_jogo()
                
                botao_carregar_rect = pygame.Rect(130, ALTURA - 100, 64, 64)
                if botao_carregar_rect.collidepoint(x, y):
                    carregar_jogo()
                
                botao_loja_rect = pygame.Rect(LARGURA - 130, ALTURA - 100, 64, 64)
                if botao_loja_rect.collidepoint(x, y):
                    toggle_loja()
                
                # Botões da loja
                if loja_aberta:
                    if botoes_loja_hover['cursor']:
                        buy_cursor()
                    elif botoes_loja_hover['spaceship']:
                        buy_spaceship()
                    elif botoes_loja_hover['fechar']:
                        toggle_loja()
                        
        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1:
                mouse_pressionado = False
                clique_liberado = True
    
    # Atualizar animações
    for anim in spaceship_animations:
        anim["y"] -= anim["speed"]
        if anim["y"] < -60:
            anim["y"] = ALTURA + 60
            anim["x"] = random.randint(60, LARGURA - 60)
    
    # Resetar botão de clique
    if botao_clique_pressionado and tempo_atual - botao_clique_tempo > 500:
        botao_clique_pressionado = False
    
    # Renderizar
    tela.fill(BRANCO)
    
    # Título
    titulo_texto = fonte_titulo.render("My Clicker", True, PRETO)
    titulo_rect = titulo_texto.get_rect(center=(LARGURA // 2, 80))
    tela.blit(titulo_texto, titulo_rect)
    
    # Estatísticas
    texto_pontos = fonte_grande.render(f"Pontos: {pontos:.1f}", True, PRETO)
    tela.blit(texto_pontos, (50, 50))
    
    texto_cursores = fonte_grande.render(f"Cursores: {cursores}", True, PRETO)
    tela.blit(texto_cursores, (LARGURA - texto_cursores.get_width() - 50, 50))
    
    # Cursores visuais
    for i in range(cursores):
        x = random.randint(40, LARGURA - 40)
        y = random.randint(150, ALTURA - 200)
        tela.blit(cursor_icon, (x, y))
    
    # Spaceships animadas
    for anim in spaceship_animations:
        tela.blit(spaceship_icon, (anim["x"], anim["y"]))
    
    # Botões de controle
    botao_salvar_rect = pygame.Rect(50, ALTURA - 100, 64, 64)
    botao_salvar_hover = desenhar_botao(tela, botao_salvar_rect, "", fonte_media, CINZA, CINZA_ESCURO, PRETO, save_icon)
    
    botao_carregar_rect = pygame.Rect(130, ALTURA - 100, 64, 64)
    botao_carregar_hover = desenhar_botao(tela, botao_carregar_rect, "", fonte_media, CINZA, CINZA_ESCURO, PRETO, load_icon)
    
    botao_loja_rect = pygame.Rect(LARGURA - 130, ALTURA - 100, 64, 64)
    botao_loja_hover = desenhar_botao(tela, botao_loja_rect, "", fonte_media, CINZA, CINZA_ESCURO, PRETO, loja_icon)
    
    # Botão de clique principal
    botao_clique_rect = pygame.Rect(LARGURA // 2 - 150, ALTURA - 150, 300, 100)
    
    if botao_upgradado:
        if botao_clique_pressionado:
            botao_clique_hover = desenhar_botao(tela, botao_clique_rect, "", fonte_media, CINZA, CINZA_ESCURO, PRETO, click_upgraded_pressed_icon, True)
        else:
            botao_clique_hover = desenhar_botao(tela, botao_clique_rect, "", fonte_media, CINZA, CINZA_ESCURO, PRETO, click_upgraded_icon)
    else:
        if botao_clique_pressionado:
            botao_clique_hover = desenhar_botao(tela, botao_clique_rect, "", fonte_media, CINZA, CINZA_ESCURO, PRETO, click_pressed_icon, True)
        else:
            botao_clique_hover = desenhar_botao(tela, botao_clique_rect, "", fonte_media, CINZA, CINZA_ESCURO, PRETO, click_icon)
    
    # Loja
    if loja_aberta:
        botoes_loja_hover = desenhar_loja()
    
    # Mensagem temporária
    if mensagem_temporaria and tempo_atual - mensagem_tempo < 2000:
        texto_msg = fonte_media.render(mensagem_temporaria, True, PRETO)
        msg_rect = texto_msg.get_rect(center=(LARGURA // 2, 120))
        tela.blit(texto_msg, msg_rect)
    elif mensagem_temporaria:
        mensagem_temporaria = ""
    
    pygame.display.flip()
    relogio.tick(60)

pygame.quit()