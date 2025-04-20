import math
import copy

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
  print(f"Matriz de esfuerzos: {matriz}")
  return(matriz)