import math
from Clases import *
import copy

def calcularCI(rs):
    red = rs.sag
    totalAgentes = len(red)
    num = 0
    for ag in red:
        num += ag.n * math.pow((ag.o1 - ag.o2), 2) 
    
    return num / totalAgentes

def calcularEsfuerzoRed(rs, e):
    red = rs.sag
    esfuerzo = 0
    for i in range (len(red)):
        esfuerzo += math.ceil(math.fabs(red[i].o1 - red[i].o2) * red[i].r * e[i])
    return esfuerzo

def obtenerNuevaRed(redSocial, e):
    solucion = copy.deepcopy(redSocial)
    for i in range (len(solucion.sag)):
        solucion.sag[i].n -= e[i]
    return solucion