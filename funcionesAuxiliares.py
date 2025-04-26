import math
import copy
import Clases
import Dinamica
import FuerzaBruta
import Voraz
from tkinter import messagebox

#Calcula el conflicto interno de una red social que recibe como parámetro
def calcularCI(red):
  totalAgentes = len(red)
  num = 0
  for ag in red:
    num += ag.n * math.pow((ag.o1 - ag.o2), 2) 
  
  return num / totalAgentes

#Obtiene la red social resultante de aplicar una estrategia de cambio de opinión e a la red original
def obtenerNuevaRed(redSocial, e):
  solucion = copy.deepcopy(redSocial)
  for i in range (len(solucion.sag)):
    solucion.sag[i].n -= e[i]
  return solucion

#Crea una matriz con los esfuerzos necesarios para cambiar la opinión de cada cantidad de agentes de grupo
def matrizEsfuerzo(redSocial):
  matriz = []
  matrizInterna = []
  for i in range (0, len(redSocial)):
    for j in range (0, redSocial[i].n):
      matrizInterna.append(math.ceil(math.fabs(redSocial[i].o1 - redSocial[i].o2) * redSocial[i].r *(j+1)))
    
    matrizInterna.append(math.inf)
    matrizInterna.insert(0, 0)
    matriz.append(matrizInterna)
    matrizInterna = []
  return(matriz)

def calcularEsfuerzoSol(solucion,matrizEsfuerzo):
  esfuerzoFinal = 0
  for i in range (0, len(matrizEsfuerzo)):
    esfuerzoFinal += matrizEsfuerzo[i][solucion[i]]
  
  return esfuerzoFinal

def calcularEsfuerzoRed(rs, e):
  red = rs.sag
  esfuerzo = 0
  for i in range (len(red)):
    esfuerzo += math.ceil(math.fabs(red[i].o1 - red[i].o2) * red[i].r * e[i])
  return esfuerzo

def salida(redSocial,algoritmo):
  match algoritmo:
    case "Fuerza Bruta":
      e, ci, esfuerzo = FuerzaBruta.modciFB(redSocial)
    case "Dinámica":
      e, ci, esfuerzo = Dinamica.solucionDinamica(redSocial)
    case "Voraz":
      e, ci, esfuerzo = Voraz.modciV(redSocial)
    case _:
      messagebox.showerror("Error", "Algoritmo no válido.")
      exit()
  
  return Clases.Salida(e, esfuerzo, ci)