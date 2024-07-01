import pygame
from random import randint
from math import sqrt

tam_telaX = 660
tam_telaY = 750
white = (255,255,255)

tela = pygame.display.set_mode((tam_telaX, tam_telaY))
clock = pygame.time.Clock()
run = True

class Bola:
    def __init__(self, x, y, vx, vy, raio, m):

        if x + raio > tam_telaX or y + raio > tam_telaY:
            self.x = x - raio
            self.y = y - raio
        elif x - raio < 0 or y - raio < 0:
            self.x = x + raio
            self.y = y + raio
        else:
            self.x = x
            self.y = y

        self.vx = vx
        self.vy = vy
        self.raio = raio
        self.cor = (randint(115,150), randint(115,150),randint(115,150))
        self.m = m
    def moveBola(self):
        self.x += self.vx
        self.y += self.vy
    def colisoesParede(self):
        if self.x + self.raio >= tam_telaX or self.x - self.raio <= 0:
            self.vx = - self.vx
            self.x += self.vx
        if self.y + self.raio >= tam_telaY or self.y - self.raio <= 0:
            self.vy = - self.vy
            self.y += self.vy
    def checaColisao(bola1, bola2, flag):
        distancia = sqrt((bola1.x - bola2.x)**2 + (bola1.y - bola2.y)**2)
        if (bola1.raio + bola2.raio >= distancia):
            aux = bola1.vx
            bola1.vx = (bola1.m - bola2.m)/ (bola1.m + bola2.m) * bola1.vx + 2*bola2.m/ (bola1.m + bola2.m) * bola2.vx 
            bola2.vx = (bola2.m - bola1.m) * bola2.vx/ (bola1.m + bola2.m) + 2*bola1.m * aux/ (bola1.m + bola2.m)
            aux = bola1.vy
            bola1.vy = (bola1.m - bola2.m) * bola1.vy/ (bola1.m + bola2.m) + 2*bola2.m * bola2.vy/ (bola1.m + bola2.m)
            bola2.vy = (bola2.m - bola1.m) * bola2.vy/ (bola1.m + bola2.m) + 2*bola1.m * aux/ (bola1.m + bola2.m)
            flag = 1
    def mudaCoordenadas(bola):
        x = randint(0, tam_telaX)
        y = randint(0, tam_telaY)
        if x + bola.raio > tam_telaX or y + bola.raio > tam_telaY:
            bola.x = x - bola.raio
            bola.y = y - bola.raio
        elif x - bola.raio < 0 or y - bola.raio < 0:
            bola.x = x + bola.raio
            bola.y = y + bola.raio
        else:
            bola.x = x
            bola.y = y

n_bolas = int(input("n_bolas"))

bolas = []

for i in range(n_bolas):
    bolas.append(Bola(randint(0, tam_telaX), 
                      randint(0, tam_telaY), 
                      randint(-5, 5), 
                      randint(-5, 5), 
                      randint(18, 35),
                      randint(2,15)))

cont_bola = 0
while cont_bola < n_bolas:
    nasceu_certo = 1
    for j in range (n_bolas):
        distancia = sqrt((bolas[cont_bola].x - bolas[j].x)**2 + (bolas[cont_bola].y - bolas[j].y)**2)
        if(bolas[cont_bola].raio + bolas[j].raio >= distancia and j != cont_bola):
            nasceu_certo = 0;
            Bola.mudaCoordenadas(bolas[cont_bola])
            break

    if nasceu_certo:
        cont_bola += 1

while run:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    tela.fill(white)

    for i in range(n_bolas):
        pygame.draw.circle(tela, bolas[i].cor, (bolas[i].x, bolas[i].y), bolas[i].raio)
    
        Bola.colisoesParede(bolas[i])

        for j in range(i):
            colidiu = 0
            Bola.checaColisao(bolas[i], bolas[j], colidiu)
            if colidiu:
                for k in range (n_bolas):
                    if (k != j and k != i):
                        Bola.checaColisao(bolas[i], bolas[k], colidiu)
                        Bola.checaColisao(bolas[k], bolas[j], colidiu)
                Bola.colisoesParede(bolas[j])

        Bola.colisoesParede(bolas[i]) 
        Bola.moveBola(bolas[i])
        
    pygame.display.update()
pygame.quit()
