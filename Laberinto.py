import turtle
import math

wn = turtle.Screen()
wn.title("El laberinto")
wn.bgcolor('black')
wn.setup(700,700)

# clases de creador de laberinto, jugador, coleccionables
class laberinto(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)  #inicializar al padre de la clase
        self.shape("square")
        self.color('green')
        self.penup() #para no ver las lineas al crear el laberinto
        self.speed(0)
class jugador(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)
        self.gold = 0
    #movimiento
    def arriba(self): #Se mueve si no hay pared
        if (self.xcor(), self.ycor() + 24) not in muros:
            self.goto(self.xcor(), self.ycor()+24)
        muros.append((self.xcor(), self.ycor()))
        laberinto.goto(self.xcor(), self.ycor())
        laberinto.stamp()
    def abajo(self):
        if (self.xcor(), self.ycor() - 24) not in muros:
            self.goto(self.xcor(), self.ycor() - 24)
        muros.append((self.xcor(), self.ycor()))
        laberinto.goto(self.xcor(), self.ycor())
        laberinto.stamp()
    def derecha(self):
        if (self.xcor() + 24, self.ycor()) not in muros:
            self.goto(self.xcor() + 24, self.ycor())
        muros.append((self.xcor(), self.ycor()))
        laberinto.goto(self.xcor(), self.ycor())
        laberinto.stamp()
    def izquierda(self):
        if (self.xcor() - 24, self.ycor()) not in muros:
            self.goto(self.xcor() -24 , self.ycor())
        muros.append((self.xcor(), self.ycor()))
        laberinto.goto(self.xcor(), self.ycor())
        laberinto.stamp()
    def colision(self, otro):
        a = self.xcor() - otro.xcor()
        b = self.ycor() - otro.ycor()
        distancia = math.sqrt((a ** 2) + (b ** 2)) #pitagoras

        if distancia <5:
            return True
        else:
            return False

    def reiniciarlaberinto(self):
        return crearlaberinto(niveles[1])


class coleccionable(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("gray")
        self.penup()
        self.speed(0)
        self.gold = 1
        self.goto(x,y)
    def desaparecer(self):
        self.goto(1000, 1000)
        self.hideturtle()

#Lista para los niveles
niveles = [''] # las comillas por conveniencia, empezar la lista en la posicion 1
nivel1 = [
"FFFFFFFFFFFFFFFFFFFFFFFFF",
"FC  FF   FFF   FFFFF FFFF",
"F F C              F  FFF",
"F F                    FF",
"F F                    FF",
"F FFFFFFFF      FF F CFFF",
"F FFFFFFFF     FFFFFFF CF",
"F FFFFFFFF  FFFFFFFFFF  F",
"F F         FFFFFFFF    F",
"F F                F    F",
"F F                F    F",
"FC FFFFFF               F",
"F          F            F",
"F          F          FFF",
"F          F         F CF",
"FF         F        F   F",
"FFFFFFFFF  FFFFFFFFFF   F",
"FFFC         FFFFFFF    F",
"FF            FFFFF     F",
"F              FFFF     F",
"F               FFF    FF",
"F                    FFFF",
"F                   FFFFF",
"FJ                 FFFFFF",
"FFFFFFFFFFFFFFFFFFFFFFFFF"
]
niveles.append(nivel1)
#lista para muros
muros = []
#lista para coleccionables
coleccionables = []

#Funcion para crear muros
def crearlaberinto(nivel):
    for y in range(len(nivel)):
        for x in range(len(nivel[y])):
            caracter = nivel[y][x]
            puntox: int = -288 + (x * 24)
            puntoy: int = 288 - (y * 24)

            if caracter == "F":
                laberinto.goto(puntox, puntoy)
                laberinto.stamp()
                muros.append((puntox, puntoy)) #tupla de coordenadas

            if caracter == "J":
                jugador.goto(puntox, puntoy)

            if caracter == "C":
                coleccionables.append(coleccionable(puntox, puntoy))




#Instancias de clase
laberinto = laberinto()
jugador = jugador()

#Crear nivel
crearlaberinto(niveles[1])


#Asignacion de teclas
turtle.listen()
turtle.onkey(jugador.arriba, 'Up')
turtle.onkey(jugador.abajo, 'Down')
turtle.onkey(jugador.derecha, 'Right')
turtle.onkey(jugador.izquierda, 'Left')



#loop
while True:
    for puntaje in coleccionables:
        if jugador.colision(puntaje):
            jugador.gold += puntaje.gold
            print('Tienes {}/7 antivirus contra el COVID-19'.format(jugador.gold))
            if jugador.gold == 7:
                print('Estás curado!! "Deseamos que fuese tan facil fuera de esta realidad"....')
                wn.bye()
            puntaje.desaparecer()
            coleccionables.remove(puntaje)
    wn.update()
    
