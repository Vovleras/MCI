import Clases
from funcionesAuxiliares import *
import heapq
  
def solucionDinamica(redSocial):
  #Inicializar variables y matrices
  sag = redSocial.sag
  cIInicial = calcularCI(sag)
  n = len(sag)
  esfuerzos = matrizEsfuerzo(sag)
  esfuerzoMax = redSocial.r_max
  matrizCI = [[cIInicial] * (n) for _ in range(esfuerzoMax + 1)] #Contiene los CI parciales
  matrizSolucion = [[[0] * n for _ in range(n)] for _ in range(esfuerzoMax + 1)]  #Contiene las soluciones parciales
  
  for i in range(0,n):
    #Inicializar variables
    cantCambiar = 0 #Cantidad de agentes que cambio actualmente
    agenteSiguiente = 1 #Cantidad de agentes que se busca cambiar
    
    for j in range (0,esfuerzoMax+1):
      esfuerzoSiguiente = esfuerzos[i][agenteSiguiente] #Esfuerzo que me va a costar cambiar un agente más
      
      #Cuando el esfuerzo es igual para diferentes cantidades
      while (j==esfuerzoSiguiente):
        cantCambiar+=1
        agenteSiguiente+=1
        esfuerzoSiguiente = esfuerzos[i][agenteSiguiente]
      
      #CASO TRIVIAL
      if (i==0 and cantCambiar>0):
        e = [0]*n
        e[0] = cantCambiar
        redModificada = obtenerNuevaRed(redSocial, e)
        conflictoVariable = calcularCI(redModificada.sag)
        matrizCI[j][i] = conflictoVariable
        matrizSolucion[j][i] = e
      
      #CASO RECURSIVO
      elif (i>0):
        izquierda = matrizCI[j][i-1] #Valor de la izq se va a usar para comparar

        if(cantCambiar==0):
          conflictoVariable = izquierda
          matrizCI[j][i] = conflictoVariable
          matrizSolucion[j][i] = matrizSolucion[j][i-1]
        else:
          arregloValores = [[izquierda,matrizSolucion[j][i-1]]] #Primera pos el CI, segunda la cantidad de agentes a cambiar
          
          for k in range (0,cantCambiar+1):
            posRef = j-esfuerzos[i][k]

            solParcial = matrizSolucion[posRef][i-1][:]
            solParcial[i] = k

            redModificada = obtenerNuevaRed(redSocial, solParcial)
            valorComparar = calcularCI(redModificada.sag)
            heapq.heappush(arregloValores,[valorComparar, solParcial])
          
          ciMinimo = heapq.heappop(arregloValores)
          matrizCI[j][i] = ciMinimo[0]
          matrizSolucion[j][i] = ciMinimo[1]
  
  sol = matrizSolucion[esfuerzoMax][i]
  redFinal = obtenerNuevaRed(redSocial,sol)
  print("Esta es la solución final: ", sol)
  print("Esta es el nuevo CI: ",calcularCI(redFinal.sag))
  print("Esta es la última celda: ",matrizCI[esfuerzoMax][i])

  return sol, matrizCI[esfuerzoMax][i]

def salida(redSocial):
  print("Entro a salida de Dinamica.py")
  e, ci = solucionDinamica(redSocial)
  nuevaRed= obtenerNuevaRed(redSocial, e)
  esfuerzo = 0
  print("Salida bien")
  return Clases.Salida(e, ci, esfuerzo, nuevaRed)

#--PRUEBA 12--
# ag1 = Clases.Agentes(2,93,-9,0.062)
# ag2 = Clases.Agentes(9,-4,60,0.121)
# ag3 = Clases.Agentes(5,-69,-17,0.449)
# ag4 = Clases.Agentes(8,-12,-18,0.068)
# ag5 = Clases.Agentes(4,69,-55,0.634)
# ag6 = Clases.Agentes(1,96,-13,0.063)
# ag7 = Clases.Agentes(2,66,-89,0.667)
# ag8 = Clases.Agentes(9,-26,-44,0.811)
# ag9 = Clases.Agentes(1,29,95,0.502)
# ag10 = Clases.Agentes(1,-95,-93,0.546)
# ag11 = Clases.Agentes(4,94,-44,0.722)
# ag12 = Clases.Agentes(2,1,81,0.046)
# ag13 = Clases.Agentes(8,42,-2,0.118)
# ag14 = Clases.Agentes(2,53,-59,0.613)
# ag15 = Clases.Agentes(6,66,100,0.538)

# sec = [ag1, ag2, ag3, ag4, ag5, ag6, ag7, ag8, ag9, ag10, ag11, ag12, ag13, ag14, ag15 ]
# redSocial = Clases.RedSocial(sec, 116)
# solucionDinamica(redSocial)
# #Debe ser 16558,266