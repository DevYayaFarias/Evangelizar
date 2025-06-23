import pygame
import random
import textwrap

pygame.init()

largura, altura = 800, 650
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Caminho da Luz")

FUNDO = (30, 30, 60)
TEXTO = (255, 255, 255)
CAIXA = (0, 0, 0)
JOGADOR_COR = (183, 110, 121)
ITEM_COR = (255, 231, 101)

fonte = pygame.font.SysFont("Garamond", 30)
fonte_menor = pygame.font.SysFont("Garamond", 24)

def tela_inicial():
    tela.fill(FUNDO)

    titulo = fonte.render("CAMINHO DA LUZ", True, TEXTO)
    instrucao = fonte_menor.render("Pressione qualquer tecla para começar", True, TEXTO)
    boas_vindas = fonte_menor.render("Bem-vindo! Encontre a luz através da Palavra de Deus.", True, TEXTO)

    lampada_img = pygame.image.load("lampada.png")
    lampada_img = pygame.transform.scale(lampada_img, (50, 50))
    x_titulo = (largura - titulo.get_width()) // 2
    y_titulo = 200
    tela.blit(lampada_img, (x_titulo - 60, y_titulo))
    tela.blit(titulo, (x_titulo, y_titulo))
    tela.blit(boas_vindas, ((largura - boas_vindas.get_width()) // 2, 280))
    tela.blit(instrucao, ((largura - instrucao.get_width()) // 2, 340))

    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                esperando = False


tela_inicial()

lampada_img = pygame.image.load("lampada.png")
lampada_img = pygame.transform.scale(lampada_img, (50, 50))

jogador = pygame.Rect(400, 500, 40, 40)
velocidade = 5

versiculos_textos = [
    "Lâmpada para os meus pés é tua palavra, e luz para o meu caminho. - Salmos 119:105",
    "O Senhor é o meu pastor, nada me faltará. - Salmos 23:1",
    "Tudo posso naquele que me fortalece. - Filipenses 4:13",
    "Não temas, pois eu estou contigo. - Isaías 41:10",
    "Entrega o teu caminho ao Senhor. - Salmos 37:5",
    "Alegrai-vos na esperança, sede pacientes na tribulação. - Romanos 12:12",
    "Aquele que habita no esconderijo do Altíssimo... - Salmos 91:1"
]

historia = [
    "Era uma vez um jovem cansado do mundo e vazio por dentro...",
    "Ele ouviu falar de um caminho... o Caminho da Luz.",
    "Guiado pela fé, decidiu seguir mesmo sem saber o que encontraria.",
    "Pelo caminho, encontrou promessas de Deus escondidas...",
    "Cada versículo era como um sopro de esperança.",
    "As trevas tentavam pará-lo, mas a Palavra era mais forte.",
    "Ao chegar no fim, ele entendeu: Jesus sempre esteve com ele.",
]

versiculos = []
for texto in versiculos_textos:
    x = random.randint(50, largura - 70)
    y = random.randint(100, altura - 150)
    versiculos.append({"rect": pygame.Rect(x, y, 20, 20), "texto": texto})

fe = 0
versiculo_atual = ""
tempo_mensagem = 0

tempo_limite = 45
tempo_inicial = pygame.time.get_ticks()

clock = pygame.time.Clock()
rodando = True

while rodando:
    tela.fill(FUNDO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: jogador.x -= velocidade
    if teclas[pygame.K_RIGHT]: jogador.x += velocidade
    if teclas[pygame.K_UP]: jogador.y -= velocidade
    if teclas[pygame.K_DOWN]: jogador.y += velocidade

    for v in versiculos[:]:
        if jogador.colliderect(v["rect"]):
            versiculo_atual = v["texto"]
            tempo_mensagem = pygame.time.get_ticks()
            versiculos.remove(v)
            fe += 1

    pygame.draw.rect(tela, JOGADOR_COR, jogador)
    for v in versiculos:
        pygame.draw.rect(tela, ITEM_COR, v["rect"])

    texto_fe = fonte.render(f"Fé: {fe}", True, TEXTO)
    tela.blit(texto_fe, (10, 10))
    tempo_passado = (pygame.time.get_ticks() - tempo_inicial) // 1000
    tempo_restante = max(0, tempo_limite - tempo_passado)
    texto_tempo = fonte.render(f"Tempo: {tempo_restante}s", True, TEXTO)
    tela.blit(texto_tempo, (10, 50))

    if fe < len(historia):
        frase_atual = historia[fe]
    else:
        frase_atual = "Continue firme! A fé te trouxe até aqui."
    render_historia = fonte_menor.render(frase_atual, True, TEXTO)
    largura_texto = render_historia.get_width()
    tela.blit(render_historia, ((largura - largura_texto) // 2, 10))

    if versiculo_atual and pygame.time.get_ticks() - tempo_mensagem < 8000:
        largura_caixa = 700
        altura_caixa = 120
        x_caixa = 50
        y_caixa = altura - altura_caixa - 20
        pygame.draw.rect(tela, CAIXA, (x_caixa, y_caixa, largura_caixa, altura_caixa))
        pygame.draw.rect(tela, TEXTO, (x_caixa, y_caixa, largura_caixa, altura_caixa), 2)

        texto_formatado = textwrap.wrap(versiculo_atual, width=70)
        for i, linha in enumerate(texto_formatado):
            render = fonte_menor.render(linha, True, TEXTO)
            tela.blit(render, (x_caixa + 10, y_caixa + 10 + i * 25))
    elif pygame.time.get_ticks() - tempo_mensagem >= 8000:
        versiculo_atual = ""

    if fe == len(versiculos_textos):
        msg = fonte.render("Você venceu! Agora você é luz do mundo, IDE!", True, TEXTO)
        lampada_img = pygame.image.load("lampada.png")
        lampada_img = pygame.transform.scale(lampada_img, (60, 60))
        tela.blit(lampada_img, (360, 360))
        tela.blit(msg, (100, 300))
        pygame.display.flip()
        pygame.time.delay(5000)

        break
    elif tempo_restante <= 0:
        msg = fonte.render("Você perdeu... mas Jeus te ama e nunca desiste de você.", True, TEXTO)
        tela.blit(msg, (80, 300))
        pygame.display.flip()
        pygame.time.delay(5000)
        break

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
