import pygame  # importa a biblioteca pygame (gráficos, teclado, som)
import random  # importa funções de aleatoriedade

pygame.mixer.pre_init(44100, -16, 2, 512)  
# configura o sistema de áudio antes de iniciar (qualidade, canais, buffer)

pygame.init()  # inicia todos os módulos do pygame (janela, input, etc)
pygame.mixer.init()  # inicia especificamente o sistema de som

GRID_SIZE = 30  # tamanho da grid (quantidade de quadrados por lado)
TILE = 25  # tamanho de cada quadrado em pixels

WIDTH = GRID_SIZE * TILE  # largura da tela
HEIGHT = GRID_SIZE * TILE  # altura da tela

screen = pygame.display.set_mode((WIDTH, HEIGHT))  
# cria a janela do jogo

clock = pygame.time.Clock()  
# controla o FPS (velocidade do jogo)

# CORES (RGB)
PLAYER_COLOR = (160, 32, 240)
DRAGON_COLOR = (255, 0, 0)
OGRE_COLOR = (0, 200, 0)
ATTACK_COLOR = (120, 120, 120)
PLAYER_ATTACK_COLOR = (200, 0, 200)
SUMMONER_COLOR = (255, 0, 127)
BG = (0, 0, 0)

# 🎵 MUSICA
pygame.mixer.music.load("music.mp3")  # carrega música
pygame.mixer.music.set_volume(0.4)  # volume da música
pygame.mixer.music.play(-1)  # toca em loop infinito

# 🔊 SOM
attack_sound = pygame.mixer.Sound("attack.mp3")  # carrega som de ataque
attack_sound.set_volume(0.8)  # volume do som
summon_sound = pygame.mixer.Sound("summon.mp3")
summon_sound.set_volume(2)
# ================= PLAYER =================

class Player:  # classe do jogador
    def __init__(self):
        self.x = GRID_SIZE // 2  # começa no meio horizontal
        self.y = GRID_SIZE - 1  # começa embaixo
        self.dir = (0, -1)  # direção inicial (cima)
        self.attack_fx = []  # lista de efeitos visuais de ataque

    def move(self, dx, dy, enemies):  # função de movimento
        nx = self.x + dx  # nova posição x
        ny = self.y + dy  # nova posição y

        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:  
        # verifica limite da tela
            for e in enemies:  
                if (e.x, e.y) == (nx, ny):  
                    return False  # bloqueia se tiver inimigo
            self.x = nx  # aplica movimento
            self.y = ny
            self.dir = (dx, dy)  # atualiza direção
            return True  # movimento válido
        return False  # movimento inválido

    def attack(self, enemies):  # função de ataque
        tx = self.x + self.dir[0]  # posição alvo x
        ty = self.y + self.dir[1]  # posição alvo y

        self.attack_fx = [(tx, ty)]  # cria efeito visual

        attack_sound.stop()  # para som atual (evita sobreposição)
        attack_sound.play()  # toca som

        for e in enemies:  
            if (e.x, e.y) == (tx, ty):  
                enemies.remove(e)  # remove inimigo (mata)
                return True  # ataque funcionou
        return False  # não acertou nada

# ================= ENEMY =================

class Enemy:  # classe dos inimigos
    def __init__(self, x, y, type):
        self.x = x  # posição x
        self.y = y  # posição y
        self.type = type  # tipo (ogre ou dragon)
        self.turn_counter = 0  # contador de turnos

    def summon(self):

        summon_sound.stop()
        summon_sound.play()

        for dx in [-3,0,3]:
            for dy in [-3,0,3]:

                if dx != 0 or dy != 0:

                    sx = self.x + dx
                    sy = self.y + dy

                    # verifica se está dentro da tela
                    if 0 <= sx < GRID_SIZE and 0 <= sy < GRID_SIZE:

                        n = random.randint(0,10)

                        if n > 7:
                            spawn_enemy(sx, sy, False)

    def move(self, player, enemies):  # movimento do inimigo
        dx, dy = 0, 0

        # lógica de perseguição (segue o player)
        if self.x < player.x: dx = 1
        elif self.x > player.x: dx = -1
        elif self.y < player.y: dy = 1
        elif self.y > player.y: dy = -1

        nx = self.x + dx  # nova posição
        ny = self.y + dy

        if not (0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE):
            return  # evita sair do mapa

        if (nx, ny) == (player.x, player.y):
            return  # não entra no player

        for e in enemies:
            if e != self and (e.x, e.y) == (nx, ny):
                return  # evita colisão com outros inimigos

        self.x, self.y = nx, ny  # move

    def attack_tiles(self):  # define área de ataque
        tiles = []

        if self.type == "ogre":
            # ataque em volta (8 direções)
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx != 0 or dy != 0:
                        tiles.append((self.x+dx, self.y+dy))

        elif self.type == "dragon":
            # ataque em linha (cruz)
            for i in range(1,3):
                tiles += [
                    (self.x+i, self.y),
                    (self.x-i, self.y),
                    (self.x, self.y+i),
                    (self.x, self.y-i)
                ]

        return tiles  # retorna lista de tiles

    def can_attack(self):  # define quando pode atacar
        if self.type == "ogre":
            return self.turn_counter % 2 == 0  # a cada 2 turnos
        if self.type == "dragon":
            return self.turn_counter % 3 == 0  # a cada 3 turnos
        if self.type == "summoner":
            return self.turn_counter % 20 == 0

# ================= JOGO =================

def spawn_enemy(x = 0, y = 0, summoner=True):  # cria inimigo aleatório
    global score
    if score > 5 and summoner:
        t = random.choice(["ogre","dragon","summoner"])  # escolhe tipo
    else:
        t = random.choice(["ogre","dragon"])  # escolhe tipo
    while True:
        if not x != 0 and not y != 0:
            x = random.randint(0, GRID_SIZE-1)
            y = random.randint(0, GRID_SIZE-3)
        if (x,y) != (player.x, player.y):  # evita spawn no player
            enemies.append(Enemy(x,y,t))
            break

def reset_game():  # reinicia o jogo
    global player, enemies, score, game_over
    player = Player()  # recria player
    enemies = []  # limpa inimigos
    score = 0  # zera score
    game_over = False  # tira game over

    pygame.mixer.music.play(-1)  # reinicia música

    for _ in range(3):  # cria 3 inimigos
        spawn_enemy()
    

reset_game()  # roda inicialização

# ================= DRAW =================

def draw():  # desenha tudo
    screen.fill(BG)  # limpa tela

    # desenha ataques inimigos
    for e in enemies:
        if e.can_attack():
            for tx, ty in e.attack_tiles():
                if 0 <= tx < GRID_SIZE and 0 <= ty < GRID_SIZE:
                    pygame.draw.rect(screen, ATTACK_COLOR,
                        (tx*TILE, ty*TILE, TILE, TILE))

    # desenha ataque do player
    for tx, ty in player.attack_fx:
        if 0 <= tx < GRID_SIZE and 0 <= ty < GRID_SIZE:
            pygame.draw.rect(screen, PLAYER_ATTACK_COLOR,
                (tx*TILE, ty*TILE, TILE, TILE))

    player.attack_fx = []  # limpa efeito

    # desenha player
    pygame.draw.rect(screen, PLAYER_COLOR,
        (player.x*TILE, player.y*TILE, TILE, TILE))

    # desenha inimigos
    for e in enemies:
        if e.type=="dragon":
            color = DRAGON_COLOR      
        elif e.type=="summoner":
            color = SUMMONER_COLOR
        else:
             color = OGRE_COLOR
        pygame.draw.rect(screen, color,
            (e.x*TILE, e.y*TILE, TILE, TILE))

    pygame.display.update()  # atualiza tela

# ================= TURN =================

def enemy_turn():  # turno dos inimigos
    global game_over

    for e in enemies:
        e.turn_counter += 1  # incrementa turno


  

        if e.can_attack():
            if e.type == "summoner":
                e.summon()
                enemies.remove(e)
            elif (player.x, player.y) in e.attack_tiles():  
                game_over = True  # mata player
                pygame.mixer.music.stop()  # para música
        else:
            if not e.type == "summoner":
                e.move(player, enemies)  # move inimigo

# ================= LOOP =================

running = True  # controle do loop principal

while running:
    clock.tick(10)  # limita FPS

    for event in pygame.event.get():  # pega eventos
        if event.type == pygame.QUIT:
            running = False  # fecha jogo

        if event.type == pygame.KEYDOWN:  # tecla pressionada

            if game_over and event.key == pygame.K_r:
                reset_game()  # reinicia jogo

            if not game_over:
                action = False  # controla turno

                # movimento do player
                if event.key == pygame.K_w:
                    action = player.move(0,-1,enemies)
                elif event.key == pygame.K_s:
                    action = player.move(0,1,enemies)
                elif event.key == pygame.K_a:
                    action = player.move(-1,0,enemies)
                elif event.key == pygame.K_d:
                    action = player.move(1,0,enemies)

                # ataque
                elif event.key == pygame.K_x:
                    if player.attack(enemies):
                        score += 1  # aumenta score
                        for _ in range(random.randint(1,3)):
                            spawn_enemy()  # spawn inimigos
                        action = True

                if action:
                    enemy_turn()  # turno inimigo

    draw()  # desenha frame

    if game_over:
        font = pygame.font.SysFont(None, 30)  # fonte
        text = font.render(f"GAME OVER - Score: {score} (R)", True, (255,255,255))
        screen.blit(text, (20, HEIGHT//2))  # desenha texto
        pygame.display.update()

pygame.quit()  # encerra pygame