import pygame
from random import randint, randrange

#---FUNCIONES PARA LA VIDA DEL JUGADOR Y SU PUNTAJE---#
def Texto(surface, text, size, x, y ):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

def Vida(surface, x, y, percent):
    largo = 100
    ancho = 15
    vida = (percent/100) * largo
    borde = pygame.Rect(x, y, largo, ancho)
    vida = pygame.Rect(x, y, vida, 15)
    pygame.draw.rect(surface, (172,27,27), vida)
    pygame.draw.rect(surface, (255,255,255), borde, 4)

#---CLASES PARA DAR INSTRUCCIONES A CADA SPRITE---#
class Space_ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave.png").convert()
        self.image.set_colorkey(0,0)
        self.rect = self.image.get_rect()
        self.rect.centerx = 300
        self.rect.bottom = 580
        self.velo_x = 0
        self.velo_y = 0
        self.shield = 100
    def Cambio(self, x):
        self.velo_x += x
        self.velo_y += y
    def update(self):
        self.rect.x += self.velo_x
        self.rect.y = 520

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("virus.png").convert()
        self.image.set_colorkey(0,0)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(700 - self.rect.width)
        self.rect.y = randrange(-100, -40)
        self.speedy = randrange(4, 8)
        self.speedx = randrange(-5,5)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > 600 + 10 or self.rect.left < -25 or self.rect.right > 700 + 25:
            self.rect.x = randrange(700 - self.rect.width)
            self.rect.y = randrange(-100, -40)
            self.speedy = randrange(4,  8)

class Shot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert()
        self.image.set_colorkey(0,0)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y -= 3

#---INICIO DEL MENU PRINCIPAL---#
def G_OVER():
    screen.fill((50, 28, 28))
    Texto(screen, "-----------------------------", 65, 300, 80)
    Texto(screen, "'CORONEADOS'", 65, 300, 150)
    Texto(screen, "-----------------------------", 65, 300, 220)
    Texto(screen, "'El covid-19 ha mutado y ahora está en el espacio'", 25, 300, 300)
    Texto(screen, "¡Trata de eliminarlo!", 25, 300, 325)
    Texto(screen, "-----------------------------", 65, 300, 370)
    Texto(screen, "DALE A CUALQUIER TECLA", 20, 300, 450)
    pygame.display.flip()
    wait = True
    while wait:
        fps.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                wait = False

#---INICIALIZACIÓN DEL JUEGO Y CARACTERÍSTICAS---#
pygame.init()
screen = pygame.display.set_mode((600, 600))
fps = pygame.time.Clock()
start = True
pygame.display.set_caption("Coroneados")
icon = pygame.image.load('virus.png')
pygame.display.set_icon(icon)

#---SONIDOS USADOS---#
pium = pygame.mixer.Sound("laser1.wav")
uh = pygame.mixer.Sound("uh.wav")
game_over = True

#---LÓGICA DEL JUEGO---#
while start:
    if game_over:
        G_OVER()
        game_over = False
        score = 0

        # ---CREACIÓN DE LISTAS PARA PODER RELACIONAR LOS SPRITES---#
        sprites = pygame.sprite.Group()
        shot_list = pygame.sprite.Group()
        spaceship = Space_ship()
        enemies_list = pygame.sprite.Group()
        sprites.add(spaceship)

        # ---AUMENTA EL RANGO PARA MÁS DIFICULTAD---#
        for i in range(30):
            enemy = Enemy()
            enemy.rect.x = randrange(580)
            enemy.rect.y = randrange(300)
            enemies_list.add(enemy)
            sprites.add(enemy)

        # ---MOVIMIENTO DE LOR CÍRCULOS SIMULANDO MOVIMIENTO---#
        first = []
        for i in range(200):
            x = randint(0, 700)
            y = randint(0, 650)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), 3)
            first.append([x, y])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False

        #---CONTROL DEL MOVIMIENTO DE LA NAVE---#
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                spaceship.Cambio(-3)
            if event.key == pygame.K_RIGHT:
                spaceship.Cambio(3)
            if event.key == pygame.K_SPACE:
                shot = Shot()
                shot.rect.x = spaceship.rect.x + 20
                shot.rect.y = spaceship.rect.y - 20
                sprites.add(shot)
                shot_list.add(shot)
                pium.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                spaceship.Cambio(3)
            if event.key == pygame.K_RIGHT:
                spaceship.Cambio(-3)
    sprites.update()

    #---CICLO PARA QUE REAPAREZCAN LOS ENEMIGOS Y SE CUENTE LAS VECES QUE CHOCAN CON LA NAVE---#
    choques = pygame.sprite.groupcollide(enemies_list, shot_list, True, True)
    for choque in choques:
        enemy = Enemy()
        sprites.add(enemy)
        enemies_list.add(enemy)
        score += 1
        uh.play()
    choques = pygame.sprite.spritecollide(spaceship, enemies_list, True)
    for i in choques:
        spaceship.shield -= 20
        if spaceship.shield == 0:
            game_over = True

    #---CICLO PARA ELIMINAR ENEMIGOS CUANDO RECIBEN UN DISPARO Y DESAPARECER EL DISPARO---#
    for shot in shot_list:
        touch_list = pygame.sprite.spritecollide(shot, enemies_list, True)
        for enemy in touch_list:
            sprites.remove(shot)
            shot_list.remove(shot)
    for shot in shot_list:
        if shot.rect.y < -10:
            sprites.remove(shot)
            shot_list.remove(shot)

    #---CONTEO DE PUNTAJE---#
    if score == 100:
        start = False

    #---COLOR DE FONDO Y DIBUJO DE LAS ESTRELLAS---#
    screen.fill((50,28,28))
    for i in first:
        pygame.draw.circle(screen, (255,255,255), i, 1)
        i[1] += 2
        if i[1] > 600:
            i[1] = 0
            
    #---APARICIÓN DE SPRITES, VIDA Y PUNTAJE---#
    sprites.draw(screen)
    Texto(screen, str(f"Puntos:{score}"), 25, 300, 10)
    Vida(screen, 5, 5, spaceship.shield)
    pygame.display.update()
    fps.tick(60)
