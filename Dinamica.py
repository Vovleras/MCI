import Clases
import prueba
import heapq
import numpy as np
import math

#Calcular el conflicto interno inicial


#Inicializar las matrices de resultado
#Llenar matriz de esfuerzos
#Empezamos a recorrer

#Recibe como parámetro el SAG de la red
def matrizEsfuerzo(redSocial):
  matriz = []
  matrizInterna = []
  for i in range (0, len(redSocial)):
    for j in range (0, redSocial[i].n):
      matrizInterna.append(math.ceil(math.fabs(redSocial[i].o1 - redSocial[i].o2) * redSocial[i].r *(j+1)))
    matriz.append(matrizInterna)
    matrizInterna = []
  print(f"Matriz de esfuerzos: {matriz}")
  return(matriz)

#Caso trivial

#Dos matrices, una con ceros y otras con CI inicial
  
def solucionDinamica(redSocial):
  global cIInicial, esfuerzos
  cIInicial = prueba.calcularCI(redSocial.sag)
  n = len(redSocial.sag)
  esfuerzos = matrizEsfuerzo(redSocial.sag)
  esfuerzoMax = redSocial.r_max
  matrizCI = [[None] * (n) for _ in range(esfuerzoMax + 1)] 
  matrizAgentes = [[0] * (n) for _ in range(esfuerzoMax + 1)]  #Contiene la cantidad de agentes a cambiar

  for i in range(0,n):
    conflictoVariable = cIInicial
    cantCambiar = 0
    for j in range (0,esfuerzoMax):
      esfuerzoActual = esfuerzos[i][cantCambiar]
      
      #Caso trivial
      if (i==0):
        if (j>=esfuerzoActual):
          cantCambiar+=1
          print(f"Cantidad a cambiar trivial: {cantCambiar}")
          e = [0]*n
          e[i] = cantCambiar
          redModificada = prueba.obtenerNuevaRed(redSocial, e)
          conflictoVariable = prueba.calcularCI(redModificada.sag)
      
      #Caso restante
      else:
        izquierda = matrizCI[j][i-1] #Valor de la izq se va a usar para comparar
        posComparar = j-esfuerzos[i][cantCambiar]
        
        if(posComparar<0):
          conflictoVariable = min(izquierda,cIInicial)
        else:
          e = matrizAgentes[posComparar] 
                      
          if (j>=esfuerzoActual):
            cantCambiar+=1
            print(f"Cantidad a cambiar restante: {cantCambiar}")
          
          e[i] = cantCambiar
          redModificada = prueba.obtenerNuevaRed(redSocial, e)
          conflictoVariable=min(izquierda,prueba.calcularCI(redModificada.sag))
        
      matrizCI[j][i] = conflictoVariable
      matrizAgentes[j][i] = cantCambiar
  
  print(f"Matriz de CI: {matrizCI}\nMatriz de Agentes: {matrizAgentes}")
      
ag1 = Clases.Agentes(3,-100,50,0.5)
ag2 = Clases.Agentes(1,100,80,0.1)
ag3 = Clases.Agentes(1,-10,0,0.5)
sec = [ag1, ag2, ag3]
redSocial = Clases.RedSocial(sec, 80)
solucionDinamica(redSocial)    