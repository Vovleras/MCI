import math
from Clases import *
import copy


def calcularCI(red):
    totalAgentes = len(red.sag)
    num = 0
    for ag in red.sag:
        num += ag.n * math.pow((ag.o1 - ag.o2), 2) 
    
    return num / totalAgentes

def calcularEsfuerzo(agente, e):
        return math.ceil(math.fabs(agente.o1 - agente.o2) * agente.r * e)
    
def calcularEsfuerzoRed(red, e):
    esfuerzo = 0
    for i in range (len(red.sag)):
        agente = red.sag[i]
        esfuerzo += math.ceil(math.fabs(agente.o1 - agente.o2) * agente.r * e[i])
        
    return esfuerzo

def beneficio(agente):
    return math.fabs(agente.o1 - agente.o2) /agente.r

def crearDiccionario(agentes):
    dic = {}
    for agente in agentes:
        dic[agente] = beneficio(agente)
    ord = dict(sorted(dic.items(), key=lambda x: x[1], reverse=True))
    return ord

def modciV(rs):
    dic = crearDiccionario(rs.sag)
    mx = rs.r_max
    e = [0] * len(rs.sag)
    
    def voraz(dic, res, long, mx):
        if not dic or long == 0:
            return res
        else: 
            agente = list(dic.items())[0][0]
            esfuerzo = calcularEsfuerzo(agente, res)
            if esfuerzo <= mx:
                print("entro a el if de esfuerzo")
                print(agente)
                e[rs.sag.index(agente)]=res
                dic.pop(agente)
                
                if dic:
                    voraz(dic,list(dic.items())[0][0].n, long-1, mx-esfuerzo   )
            else:
                voraz(dic, res-1, long, mx)
    
           
    voraz(dic,list(dic.items())[0][0].n, len(dic), mx)
    return e

def obtenerNuevaRed(redSocial, e):
    solucion = copy.deepcopy(redSocial)
    for i in range (len(solucion.sag)):
        solucion.sag[i].n -= e[i]
    return solucion

def printRed(red):
    for ag in red.sag:
        print(ag)
        
def salida(redSocial):
    print("Entro a sALIDA")
    e =  modciV(redSocial)
    nuevaRed= obtenerNuevaRed(redSocial, e)
    ci = calcularCI(nuevaRed)
    esfuerzo = calcularEsfuerzoRed(redSocial, e)
    print("Salida bien")
    return Salida(e, ci, esfuerzo, nuevaRed)
    
        
                
""" #prueba
a1 = Agentes(2,-17,25,0.309)
a2 = Agentes(4,-54,88,0.339)
a3 = Agentes(3,-4,75,0.365)
a4 = Agentes(3,-87,-63,0.317)
a5 = Agentes(7,-99,-40,0.968)
sec2 = [a1, a2, a3, a4, a5]
redSocial2 = RedSocial(sec2,315)
printRed(obtenerNuevaRed(redSocial2, modciV(redSocial2))) """
        
    
    
