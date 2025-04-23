import math
from Clases import *
from generales import *
import heapq

def calcularEsfuerzo(agente, e):
    return math.ceil(math.fabs(agente.o1 - agente.o2) * agente.r * e)
    
def beneficio(agente):
    return math.fabs(agente.o1 - agente.o2) /agente.r

def crearHeap(agentes):
    heap = []
    index = 0
    for agente in agentes:
        heapq.heappush(heap, (-beneficio(agente), index, agente))
        index += 1
    return heap

def modciV(rs):
    heap = crearHeap(rs.sag)
    mx = rs.r_max
    e = [0] * len(rs.sag)
    
    while heap and mx > 0:
        _, index, agente = heapq.heappop(heap)
        mod = agente.n 
        esfuerzo = calcularEsfuerzo(agente, mod)

        if esfuerzo > mx:
            mod = math.floor(mx / (math.fabs(agente.o1 - agente.o2) * agente.r)) # mod*e <= mx  -->  mod <= mx / e
            esfuerzo = calcularEsfuerzo(agente, mod)
        
        e[index] = mod
        mx -= esfuerzo

    ci = calcularCI(obtenerNuevaRed(rs, e))
    esfuerzoTotal = calcularEsfuerzoRed(rs, e)
    return e, esfuerzoTotal, ci

def salidaVoraz(rs):
    e,esfuerzo,ci =  modciV(rs)
    return Salida(e, esfuerzo,ci)
