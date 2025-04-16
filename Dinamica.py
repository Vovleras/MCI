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
    print("Entre a la funcion")
    global cIInicial, esfuerzos
    cIInicial = prueba.calcularCI(redSocial.sag)
    n = len(redSocial.sag)
    esfuerzos = matrizEsfuerzo(redSocial.sag)
    print("Calcule esfuerzos")
    esfuerzoMax = redSocial.r_max
    matrizCI = [[None] * (n) for _ in range(esfuerzoMax + 1)] 
    matrizAgentes = [[0] * (n) for _ in range(esfuerzoMax + 1)]  #Contiene la cantidad de agentes a cambiar
    
    #Caso trivial
    iTrivial =0
    iEsfuerzos=0
    conflictoVariable = cIInicial
    cantCambiar = 0
    while(iTrivial<=esfuerzoMax):
      print(f"i trivial: {iTrivial}")
      #print(f"Matriz de CI: {matrizCI}\nMatriz de Agentes: {matrizAgentes}")
      esfuerzoActual = esfuerzos[0][cantCambiar]
      print(cantCambiar)
      print("Esfuerzo: ", esfuerzoActual)
      if (iTrivial>=esfuerzoActual):
        print("Entro al else")
        cantCambiar+=1
        iEsfuerzos+=1
        e = [0]*n
        e[0] = cantCambiar
        redModificada = prueba.obtenerNuevaRed(redSocial, e)
        conflictoVariable = prueba.calcularCI(redModificada.sag)

      matrizCI[iTrivial][0] = conflictoVariable
      matrizAgentes[iTrivial][0] = cantCambiar    
        
      iTrivial+=1
    
    print(f"Matriz de CI: {matrizCI}\nMatriz de Agentes: {matrizAgentes}")
      
    #Solucion dinamica
    #j son las columnas, i son las filas
    for j in range(1,n):
      posCambiar = 0
      for i in range (0,esfuerzoMax):
        #print("Columna ", j+1)
        izquierda = matrizCI[i][j-1] #Valor de la izq se va a usar para comparar
        #print(izquierda)
        #Cuando el esfuerzo es menor que el de cambiar 1 persona
        if (i<esfuerzos[j][0]):
          nuevo = cIInicial
          matrizCI[i][j]=min(izquierda,nuevo)
        else:
          pos = i-esfuerzos[j][posCambiar]
          posCambiar+=1
          comparar = matrizAgentes[pos]
          comparar[j]=posCambiar
          
          
print("Inicial")
ag1 = Clases.Agentes(3,-100,50,0.5)
ag2 = Clases.Agentes(1,100,80,0.1)
ag3 = Clases.Agentes(1,-10,0,0.5)
sec = [ag1, ag2, ag3]
redSocial = Clases.RedSocial(sec, 80)
print("Creo la red social")
solucionDinamica(redSocial)    