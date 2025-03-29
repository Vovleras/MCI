import math
from Clases import *
from itertools import product
import copy

def calcularCI(red):
    totalAgentes = 0
    num = 0
    for ag in red:
        totalAgentes += ag.n
        num += ag.n * math.pow((ag.o1 - ag.o2), 2)
    
    if (totalAgentes == 0):
        return 0
    else: 
        return num / totalAgentes

def calcularEsfuerzo(red, e):
    esfuerzo = 0
    for i in range (len(red)):
        esfuerzo += math.ceil(math.fabs(red[i].o1 - red[i].o2) * red[i].r * e[i])
    return esfuerzo

ag1 = Agentes(3,-100,50,0.5)
ag2 = Agentes(1,100,80,0.1)
ag3 = Agentes(1,-10,0,0.5)
e1 = [0,1,1]
e2 = [1,0,0]

sec = [ag1, ag2, ag3]
redSocial = RedSocial(sec, 80)

#print(calcularCI(redSocial.sag))
#print(calcularEsfuerzo(redSocial.sag, e1))
#print(calcularEsfuerzo(redSocial.sag, e2))

def generar_combinaciones(maximos):
    combinaciones = []
    combinacion = [0] * len(maximos)
    def generar_combinacion(combinacion, index):
        if index == len(maximos):
            combinaciones.append(combinacion[:])
            return
        for i in range(maximos[index] + 1):
            combinacion[index] = i
            generar_combinacion(combinacion, index + 1)

    generar_combinacion(combinacion, 0)
    return combinaciones

def obtenerNuevaRed(redSocial, e):
    nuevaRed = copy.deepcopy(redSocial)
    for i in range (len(nuevaRed.sag)):
        nuevaRed.sag[i].n -= e[i]
    return nuevaRed

def printRed(red):
    for ag in red.sag:
        print(ag)

def maximoAgentes(redSocial):
    n = len(redSocial.sag)
    maxAgentes = []
    for i in range (n):
        maxAgentes.append(redSocial.sag[i].n)
    return maxAgentes
    

#Fuerza bruta
def modciFB(redSocial):
    maxAgentes = maximoAgentes(redSocial)
    combinaciones = generar_combinaciones(maxAgentes)
    soluciones = []
    solCombinacion = []
    for i in range (len(combinaciones)):
        if (calcularEsfuerzo(redSocial.sag, combinaciones[i]) <= redSocial.r_max):
            soluciones.append(obtenerNuevaRed(redSocial, combinaciones[i]))
            solCombinacion.append(combinaciones[i])

    solucion = soluciones[0]
    #e = solCombinacion[0]
    print("Solucion: ", solucion)
    for i in range (len(soluciones)):
        if (calcularCI(soluciones[i].sag) < calcularCI(solucion.sag)):
            solucion = soluciones[i]
            e = solCombinacion[i]

    for ag in solucion.sag:
        print(ag)
    print("CI: ", calcularCI(solucion.sag))
    print("Esfuerzo: ", calcularEsfuerzo(solucion.sag, e))
    print("E: ", e)


#modciFB(redSocial)

a1 = Agentes(5,-6,-94,0.062)
a2 = Agentes(6,-84,-7,0.378)
a3 = Agentes(1,-52,33,0.073)
a4 = Agentes(4,77,-47,0.626)
a5 = Agentes(4,-75,75,0.718)

sec2 = [a1, a2, a3, a4, a5]
redSocial2 = RedSocial(sec2, 4044)
modciFB(redSocial2)


#Programación voraz
def modciV():
    print("Hola desde modciV")

#Programación dinámica
def modciPD():
    print("Hola desde modciPD")