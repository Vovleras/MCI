import Clases
import prueba
import heapq
import numpy as np
import math
import copy

#Recibe como parámetro el SAG de la red
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
    cantCambiar = 0 #Cantidad de agentes que cambio actualmente
    agenteSiguiente = 1 #Cantidad de agentes que se busca cambiar
    
    for j in range (0,esfuerzoMax+1):
      esfuerzoActual = esfuerzos[i][cantCambiar] #Esfuerzo que me costo cambiar la cantidad de cantCambiar
      esfuerzoSiguiente = esfuerzos[i][agenteSiguiente] #Esfuerzo que me va a costar cambiar un agente más
      #print(f"Esfuerzo actual: {esfuerzoActual}")
      #Caso trivial
      
      if (i==0):
        if (j==esfuerzoSiguiente):
          cantCambiar+=1
          agenteSiguiente+=1
          
        e = [0]*n
        e[i] = cantCambiar
        redModificada = prueba.obtenerNuevaRed(redSocial, e)
        conflictoVariable = prueba.calcularCI(redModificada.sag)
        matrizCI[j][i] = conflictoVariable
        matrizAgentes[j][i] = cantCambiar
      
      #Caso restante
      else:
        izquierda = matrizCI[j][i-1] #Valor de la izq se va a usar para comparar
        
        if (j==esfuerzoSiguiente):
          cantCambiar+=1
          agenteSiguiente+=1

        if(cantCambiar==0):
          print(f"Entre al if de cant=0 con i={i} j={j}")
          conflictoVariable = min(izquierda,cIInicial)
          matrizCI[j][i] = conflictoVariable
          matrizAgentes[j][i] = 0
          #print(f"i: {i} | j:{j} | izq: {izquierda} | comparacion: {cIInicial}")
        else:
          #Cuando cantCambiar sea mayor a 0
          posRef = j-esfuerzoActual #Pos utilizada para comparar con izq
          e = copy.deepcopy(matrizAgentes[posRef])
          e[i] = cantCambiar
          redModificada = prueba.obtenerNuevaRed(redSocial, e)
          valorComparar = prueba.calcularCI(redModificada.sag)
          
          #Miro j, cuantos puedo cambiar con ese j
          #Recorrer el arreglo de esfuerzo, y hallar la pos del mayor valor <=j
          
          #Y comparo entre 1 y esa cantidad
          
          print(f"i: {i} | j:{j} | izq: {izquierda} | comparacion: {valorComparar}")

          if (izquierda <= valorComparar):
            matrizCI[j][i] = izquierda
            matrizAgentes[j][i] = 0
          else:
            matrizCI[j][i] = valorComparar
            matrizAgentes[j][i] = cantCambiar
  
  print(f"Matriz de CI:")
  for j in range (0,esfuerzoMax+1):
    print(f"{j}\t{matrizCI[j]}")
  
  print(f"\nMatriz de Cantidades:")
  for j in range (0,esfuerzoMax+1):
    print(f"{j}\t{matrizAgentes[j]}")
      
ag1 = Clases.Agentes(3,-100,50,0.5)
ag2 = Clases.Agentes(1,100,80,0.1)
ag3 = Clases.Agentes(1,-10,0,0.5)

# ag1 = Clases.Agentes(1,-67,-8,0.41)
# ag2 = Clases.Agentes(5,-73,-96,0.73)
# ag3 = Clases.Agentes(6,-26,-20,0.703)
# ag4 = Clases.Agentes(7,88,-3,0.068)
# ag5 = Clases.Agentes(7,73,-3,0.608)

sec = [ag1, ag2, ag3]
redSocial = Clases.RedSocial(sec, 80)
solucionDinamica(redSocial)    