import Clases
import prueba
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
          #print(f"Entre al if de cant=0 con i={i} j={j}")
          conflictoVariable = min(izquierda,cIInicial)
          matrizCI[j][i] = conflictoVariable
          matrizAgentes[j][i] = 0
          #print(f"i: {i} | j:{j} | izq: {izquierda} | comparacion: {cIInicial}")
        else:
          arregloValores = [[izquierda,0]] #Primera pos el CI, segunda la cantidad de agentes a cambiar
          
          
          for k in range (0,cantCambiar+1):
            #print(f"k: {k} i: {i} j: {j}")
            posRef = j-esfuerzos[i][k]

            #print(f"cantCambiar={cantCambiar} porRef){posRef}")
            #e1 = copy.deepcopy(matrizAgentes[posRef])
            #e1[i] = k
            #print(f"k: {k} i: {i} j: {j} e: {e1}")

            #Nuevo intento 7:37
            #copiaMatrizAgentes = copy.deepcopy(matrizAgentes[:j])
            #copiaMatrizCI = copy.deepcopy(matrizCI[:j])

            #print(copiaMatrizAgentes)

            solParicial = encontrarSolucion(matrizCI, matrizAgentes, n, posRef, esfuerzos, cIInicial)
            solParicial[i] = k

            redModificada = prueba.obtenerNuevaRed(redSocial, solParicial)
            valorComparar = prueba.calcularCI(redModificada.sag)
            arregloValores.append([valorComparar, k])
            
            # if (valorFinalCI > valorComparar):
            #   valorFinalCI = valorComparar
            #   valorFinalCant = k
            #   print(f"Valor final CI: {valorFinalCI}")
            # print("Valor final a cambiar ", valorFinalCant)
          
          ciMinimo = min(arregloValores, key=lambda x: x[0])
          valorFinalCI = ciMinimo[0] #Inicializo para poder comparar
          valorFinalCant = ciMinimo[1] #Inicializo para poder comparar 
          matrizCI[j][i] = valorFinalCI
          matrizAgentes[j][i] = valorFinalCant
            
          
          #print(f"i: {i} | j:{j} | izq: {izquierda} | comparacion: {valorComparar}")
  
  sol = encontrarSolucion(matrizCI, matrizAgentes, n, esfuerzoMax, esfuerzos, cIInicial)
  redFinal = prueba.obtenerNuevaRed(redSocial,sol)
  print("Esta es la solución final: ", sol)
  print("Esta es el nuevo CI: ",prueba.calcularCI(redFinal.sag))
  print("Esta es la última celda: ",matrizCI[esfuerzoMax][i])
  
  print(f"Matriz de CI:")
  for j in range (0,esfuerzoMax+1):
    print(f"{j}\t{matrizCI[j]}")
  
  # print(f"\nMatriz de Cantidades:")
  # for j in range (0,esfuerzoMax+1):
  #   print(f"{j}\t{matrizAgentes[j]}")
  

    
def encontrarSolucion(matrizCI, matrizAgentes, n, esfuerzoMax, esfuerzos, cIInicial):
  #print("Entro a hallar solucion")
  solucion = [0]*n
  
  j = esfuerzoMax
    
  for i in range (n-1,0, -1):
    if (matrizCI[j][i]!=matrizCI[j][i-1]):
      #print(f"Entro al if")
      solucion[i] = matrizAgentes[j][i]
      j -= esfuerzos[i][solucion[i]]
    #print(f"i: {i} j:{j}")
  
  #Caso primer grupo
  if(matrizCI[j][0]!=cIInicial):
    solucion[0] = matrizAgentes[j][0]
  
  #print(f"Solución final: {solucion}")    
  return solucion
      
# ag1 = Clases.Agentes(3,-100,50,0.5)
# ag2 = Clases.Agentes(1,100,80,0.1)
# ag3 = Clases.Agentes(1,-10,0,0.5)

ag1 = Clases.Agentes(2,93,-9,0.062)
ag2 = Clases.Agentes(9,-4,60,0.121)
ag3 = Clases.Agentes(5,-69,-17,0.449)
ag4 = Clases.Agentes(8,-12,-18,0.068)
ag5 = Clases.Agentes(4,69,-55,0.634)
ag6 = Clases.Agentes(1,96,-13,0.063)
ag7 = Clases.Agentes(2,66,-89,0.667)
ag8 = Clases.Agentes(9,-26,-44,0.811)
ag9 = Clases.Agentes(1,29,95,0.502)
ag10 = Clases.Agentes(1,-95,-93,0.546)
ag11 = Clases.Agentes(4,94,-44,0.722)
ag12 = Clases.Agentes(2,1,81,0.046)
ag13 = Clases.Agentes(8,42,-2,0.118)
ag14 = Clases.Agentes(2,53,-59,0.613)
ag15 = Clases.Agentes(6,66,100,0.538)

sec = [ag1, ag2, ag3, ag4, ag5, ag6, ag7, ag8, ag9, ag10, ag11, ag12, ag13, ag14, ag15 ]
redSocial = Clases.RedSocial(sec, 116)
#solucionDinamica(redSocial) 

a1 = Clases.Agentes(6,57,10,0.537)
a2 = Clases.Agentes(9,63,98,0.749)
a3 = Clases.Agentes(4,-36,39,0.636)
a4 = Clases.Agentes(9,-24,52,0.984)
a5 = Clases.Agentes(4,49,-69,0.452)
"""a6 = Agentes(2,-43,-14,0.719)
a7 = Agentes(10,45,-61,0.475)
a8 = Agentes(10,4,-26,0.081)
a9 = Agentes(10,-7,-74,0.96)
a10 =Agentes(7,-29,91,0.188)"""

sec2 = [a1, a2, a3, a4, a5]#, a6, a7, a8, a9, a10]
redSocial2 = Clases.RedSocial(sec2,460)
solucionDinamica(redSocial2)