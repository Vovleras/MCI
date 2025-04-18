import math
from Clases import *
from itertools import product
import copy

#Recibe como parámetro el SGA (Listado de grupos de agentes)
def calcularCI(red):
    totalAgentes = len(red)
    num = 0
    for ag in red:
        num += ag.n * math.pow((ag.o1 - ag.o2), 2) 
    
    return num / totalAgentes

#Recibe como parámetro el SGA, nuevas cantidades de agentes
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

#e: Cantidad a restar de agentes a cada grupo
def obtenerNuevaRed(redSocial, e):
    solucion = copy.deepcopy(redSocial)
    for i in range (len(solucion.sag)):
        solucion.sag[i].n -= e[i]
    return solucion

def printRed(red):
    for ag in red.sag:
        print(ag)

def maximoAgentes(redSocial):
    n = len(redSocial.sag)
    maxAgentes = []
    for i in range (n):
        maxAgentes.append(redSocial.sag[i].n)
    return maxAgentes
    

def generar_combinaciones(redSocial):
    maximos = maximoAgentes(redSocial)
    combinaciones = []
    combinacion = [0] * len(maximos)
    e = [0] * len(maximos)
    solucion = copy.deepcopy(redSocial)

    def generar_combinacion(combinacion, index, red, solucion, e):
        if index == len(maximos):
            if (calcularEsfuerzo(redSocial.sag, combinacion) <= redSocial.r_max):
                newRed = obtenerNuevaRed(red, combinacion)
                if (calcularCI(newRed.sag) < calcularCI(solucion.sag)):
                    solucion.sag = newRed.sag
                    e[:] = combinacion[:]
                    #combinaciones.append(combinacion[:])
            return
        #solucion = solucion
        #e=e
        for i in range(maximos[index] + 1):
            combinacion[index] = i
            generar_combinacion(combinacion, index + 1, red, solucion, e)

    generar_combinacion(combinacion, 0, redSocial, solucion, e)

    printRed(solucion)
    print("CI: ", calcularCI(solucion.sag))
    print("Esfuerzo: ", calcularEsfuerzo(solucion.sag, e))
    print("E: ", e)
    return solucion, e

#Fuerza bruta
def modciFB(redSocial):
    combinaciones = generar_combinaciones(redSocial)
    solucion = copy.deepcopy(redSocial)
    for i in range (len(combinaciones)):
        newRed = obtenerNuevaRed(redSocial, combinaciones[i])
        if (calcularCI(newRed.sag) < calcularCI(solucion.sag)):
            solucion = newRed
            e = combinaciones[i]

    for ag in solucion.sag:
        print(ag)
    print("CI: ", calcularCI(solucion.sag))
    print("Esfuerzo: ", calcularEsfuerzo(solucion.sag, e))
    print("E: ", e)


#modciFB(redSocial)

a1 = Agentes(2,-17,25,0.309)
a2 = Agentes(4,-54,88,0.339)
a3 = Agentes(3,-4,75,0.365)
a4 = Agentes(3,-87,-63,0.317)
a5 = Agentes(7,-99,-40,0.968)
"""a6 = Agentes(2,-43,-14,0.719)
a7 = Agentes(10,45,-61,0.475)
a8 = Agentes(10,4,-26,0.081)
a9 = Agentes(10,-7,-74,0.96)
a10 =Agentes(7,-29,91,0.188)"""

sec2 = [a1, a2, a3, a4, a5]#, a6, a7, a8, a9, a10]
redSocial2 = RedSocial(sec2,315)
#modciFB(redSocial2)
#generar_combinaciones(redSocial2)

ag1 = Agentes(6,57,10,0.537)
ag2 = Agentes(9,63,98,0.749)
ag3 = Agentes(4,-36,39,0.636)
ag4 = Agentes(9,-24,52,0.984)
ag5 = Agentes(4,49,-69,0.452)

sec = [ag1, ag2, ag3, ag4, ag5]
redSocial = RedSocial(sec, 460)
#generar_combinaciones(redSocial)    


#Programación voraz
def modciV():
    print("Hola desde modciV")

#Programación dinámica
def modciPD():
    print("Hola desde modciPD")