import sys, pygame
from pygame.locals import *
import sys, pygame
from pygame.locals import *
# Constantes
WIDTH = 1280
HEIGHT = 768


#Cursor
class Cursor(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self,0,0,1,1)
    def update(self):
        self.left,self.top=pygame.mouse.get_pos()


#Creacion de botones
class Boton(pygame.sprite.Sprite):
    def __init__(self,imagen1,imagen2,x=200,y=200):
        self.imagen_normal=imagen1
        self.imagen_seleccion=imagen2
        self.imagen_actual=self.imagen_normal
        self.rect=self.imagen_actual.get_rect()
        self.rect.left,self.rect.top=(x,y)

    def update(self,pantalla,cursor):
        if cursor.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccion
        else: self.imagen_actual = self.imagen_normal

        pantalla.blit(self.imagen_actual,self.rect)


class Opciones(pygame.sprite.Sprite):
    pygame.init()  # inicializo el modulo

    # fijo las dimensiones de la pantalla
    pantalla = pygame.display.set_mode((1280, 768))

    pygame.display.set_caption("Burton Burguer Game")  # Titulo de la Ventana
    # creo un reloj para controlar los fps
    reloj1 = pygame.time.Clock()


#Menu del Juego
def mainMenu():
    pygame.init()  # inicializo el modulo

    # fijo las dimensiones de la pantalla
    pantalla = pygame.display.set_mode((1280, 768))

    pygame.display.set_caption("Burton Burguer Game")  # Titulo de la Ventana
    # creo un reloj para controlar los fps
    reloj1 = pygame.time.Clock()

    inicio1=pygame.image.load("play.png")
    inicio2 = pygame.image.load("play1.png")
    opcion1 = pygame.image.load("multi.png")
    opcion2 = pygame.image.load("multi1.png")
    salir1 = pygame.image.load("exit.png")
    salir2 = pygame.image.load("exit1.png")
    fondo = pygame.image.load("fondo2.png")
    pygame.mixer.music.load('menu.mp3')
    pygame.mixer.music.play(3)


    boton1=Boton(inicio1,inicio2,533,258)
    boton2=Boton(salir1,salir2,533,458)
    boton3=Boton(opcion1,opcion2,533,358)

    cursor1=Cursor()



    salir = False

    while salir != True:
        # todos los eventos producido
        for event in pygame.event.get():
             if event.type==pygame.MOUSEBUTTONDOWN:
                if cursor1.colliderect(boton1.rect):
                    main()
                if cursor1.colliderect(boton2.rect):
                    salir = True
                if cursor1.colliderect(boton3.rect):
                    main2()
            # pygame.QUIT( cruz de la ventana)
        if event.type == pygame.QUIT:
                salir = True

        reloj1.tick(20)  # operacion para que todo corra a 20fps
        pantalla.blit(fondo,(0,0))
        cursor1.update()
        boton1.update(pantalla,cursor1)
        boton2.update(pantalla,cursor1)
        boton3.update(pantalla,cursor1)

        pygame.display.update()  # actualizo el display

    pygame.quit()



# Clases
# ---------------------------------------------------------------------
# CLASE QUE CREA EL PUCK



class Puck(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("comida1.gif", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = [-0.5, -0.5]

    def mover(self, time, jugador1,jugador2,puntos):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time

        if self.rect.left <= 0:
            puntos[1] += 1
        if self.rect.right >= WIDTH:
            puntos[0] += 1
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * time
        if pygame.sprite.collide_rect(self, jugador1):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time
        if pygame.sprite.collide_rect(self, jugador2):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * time

        return puntos


class Jugador(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("tarma3.gif", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = 0.5

    def mover(self, time, keys):
        if self.rect.top >= 0:
            if keys[K_w]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_s]:
                self.rect.centery += self.speed * time

    def ia(self, time, puck_2):
        if puck_2.speed[0] >= 0 and puck_2.rect.centerx >= WIDTH / 2:
            if self.rect.centery < puck_2.rect.centery:
                self.rect.centery += self.speed * time
            if self.rect.centery > puck_2.rect.centery:
                self.rect.centery -= self.speed * time

    def mover2(self, time, keys):
        if self.rect.top >= 0:
            if keys[K_UP]:
                self.rect.centery -= self.speed * time
        if self.rect.bottom <= HEIGHT:
            if keys[K_DOWN]:
                self.rect.centery += self.speed * time


# ---------------------------------------------------------------------

# Funciones
# ---------------------------------------------------------------------

def load_image(filename, transparent=False):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        raise
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image

def texto(texto, posx, posy, color=(255, 255, 255)):
    fuente = pygame.font.Font(None, 50)
    salida = pygame.font.Font.render(fuente, texto, 3, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect


# ---------------------------------------------------------------------

def main():
    pygame.mixer.music.load("intro.mp3")

    pygame.mixer.music.play(2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Burton Burguer Game")
    background_image = load_image('fondo.gif')
    puck = Puck()
    jugador1 = Jugador(100)
    jugador2 = Jugador(WIDTH -100)

    clock = pygame.time.Clock()

    auxTime=0
    estiloLetra = pygame.font.SysFont("Arial", 50)

    puntos = [0, 0]

    while puntos[0]!=3:
        while puntos[1]!=3:
            time = clock.tick(60)
            keys = pygame.key.get_pressed()
            tiempo = pygame.time.get_ticks() / 1000  # para el reloj
            if auxTime<= tiempo:
                print (str(auxTime)+" Segundos")
                auxTime+=1
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)

            puntos = puck.mover( time, jugador1,jugador2,puntos)
            jugador1.mover(time, keys)
            jugador2.ia(time,puck)

            p_jug, p_jug_rect = texto('Jugador 1: '+str(puntos[0]), WIDTH / 4, 40)
            p_cpu, p_cpu_rect = texto('Tarma: '+str(puntos[1]), WIDTH - WIDTH / 4, 40)

            screen.blit(background_image, (0, 0))
            screen.blit(p_jug, p_jug_rect)
            screen.blit(p_cpu, p_cpu_rect)
            screen.blit(puck.image, puck.rect)
            screen.blit(jugador1.image, jugador2.rect)
            screen.blit(jugador2.image, jugador1.rect)

            mensajeReloj = estiloLetra.render("Tiempo: " + str(auxTime) + ' Segundos', 0,(255, 255, 255))  # mensaje de reloj en pantalla
            screen.blit(mensajeReloj, (WIDTH/3, 50))  # aparicion de reloj en pantalla
            pygame.display.flip()
        return 0

def main2():
    pygame.mixer.music.load("intro.mp3")

    pygame.mixer.music.play(2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Burton Burguer Game")
    background_image = load_image('fondo.gif')
    puck = Puck()
    jugador1 = Jugador(100)
    jugador2 = Jugador(WIDTH-100)

    clock = pygame.time.Clock()

    auxTime=0
    estiloLetra = pygame.font.SysFont("Arial", 50)

    puntos = [0, 0]

    while puntos[1]!=3:
        while puntos[0]!=3:
            time = clock.tick(60)
            keys = pygame.key.get_pressed()
            tiempo = pygame.time.get_ticks() / 1000  # para el reloj
            if auxTime<= tiempo:
                print (str(auxTime)+" Segundos")
                auxTime+=1
            for eventos in pygame.event.get():
                if eventos.type == QUIT:
                    sys.exit(0)

            puntos = puck.mover( time, jugador1,jugador2,puntos)
            jugador1.mover(time, keys)
            jugador2.mover2(time,keys)

            p_jug, p_jug_rect = texto('Jugador 1: '+str(puntos[0]), WIDTH / 4, 40)
            p_cpu, p_cpu_rect = texto('Jugador 2: '+str(puntos[1]), WIDTH - WIDTH / 4, 40)

            screen.blit(background_image, (0, 0))
            screen.blit(p_jug, p_jug_rect)
            screen.blit(p_cpu, p_cpu_rect)
            screen.blit(puck.image, puck.rect)
            screen.blit(jugador1.image, jugador2.rect)
            screen.blit(jugador2.image, jugador1.rect)

            mensajeReloj = estiloLetra.render("Tiempo: " + str(auxTime) + ' Segundos', 0,(255, 255, 255))  # mensaje de reloj en pantalla
            screen.blit(mensajeReloj, (WIDTH/3, 50))  # aparicion de reloj en pantalla
            pygame.display.flip()
        return 0

mainMenu()