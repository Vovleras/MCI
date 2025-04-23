from Clases import *
import copy
from generales import *
import time

"""def printRed(red):
    for ag in red.sag:
        print(ag)"""

def maximoAgentes(redSocial):
    n = len(redSocial.sag)
    maxAgentes = []
    for i in range (n):
        maxAgentes.append(redSocial.sag[i].n)
    return maxAgentes
    

def modciFB(rs):
    ti = time.time()
    maximos = maximoAgentes(rs)
    combinacion = [0] * len(maximos)
    e = [0] * len(maximos)
    solucion = copy.deepcopy(rs)

    def generarCombinacion(combinacion, index, red, solucion, e):
        if index == len(maximos):
            if (calcularEsfuerzoRed(rs, combinacion) <= rs.r_max):
                nuevaRed = obtenerNuevaRed(red, combinacion)
                if (calcularCI(nuevaRed) < calcularCI(solucion)):
                    solucion.sag = nuevaRed.sag
                    e[:] = combinacion[:]
            return
        for i in range(maximos[index] + 1):
            combinacion[index] = i
            generarCombinacion(combinacion, index + 1, red, solucion, e)

    generarCombinacion(combinacion, 0, rs, solucion, e)

    esfuerzo = calcularEsfuerzoRed(solucion, e)
    ci = calcularCI(solucion)
    tf = time.time()
    tiempo = str(round(tf-ti,4)).replace('.', ',')
    print("Tiempo de ejecución: ", tiempo)
    print("CI: ", str(ci).replace('.', ','))
    print("Solución: ", e)
    return e, esfuerzo, ci

def salidaFB(rs):
    e,esfuerzo,ci =  modciFB(rs)
    return Salida(e, esfuerzo,ci)
