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
          valorFinalCI = izquierda #Inicializo para poder comparar
          valorFinalCant = 0 #Inicializo para poder comparar 
          
          for k in range (1,cantCambiar+1):
            #print(f"k: {k} i: {i} j: {j}")
            posRef = j-esfuerzos[i][k]
            #print(f"cantCambiar={cantCambiar} porRef){posRef}")
            e1 = copy.deepcopy(matrizAgentes[posRef])
            e1[i] = k
            redModificada = prueba.obtenerNuevaRed(redSocial, e1)
            valorComparar = prueba.calcularCI(redModificada.sag)
            
            if (valorFinalCI > valorComparar):
              valorFinalCI = valorComparar
              valorFinalCant = k
              print(f"Valor final CI: {valorFinalCI}")
              
          matrizCI[j][i] = valorFinalCI
          matrizAgentes[j][i] = valorFinalCant
            
          
          #print(f"i: {i} | j:{j} | izq: {izquierda} | comparacion: {valorComparar}")
  
  sol = encontrarSolucion(matrizCI, matrizAgentes, n, esfuerzoMax, esfuerzos, cIInicial)
  redFinal = prueba.obtenerNuevaRed(redSocial,sol)
  print("Esta es el nuevo CI: ",prueba.calcularCI(redFinal.sag))
  
  print(f"Matriz de CI:")
  for j in range (0,esfuerzoMax+1):
    print(f"{j}\t{matrizCI[j]}")
  
  print(f"\nMatriz de Cantidades:")
  for j in range (0,esfuerzoMax+1):
    print(f"{j}\t{matrizAgentes[j]}")
    
def encontrarSolucion(matrizCI, matrizAgentes, n, esfuerzoMax, esfuerzos, cIInicial):
  print("Entro a hallar solucion")
  solucion = [0]*n
  
  j = esfuerzoMax
    
  for i in range (n-1,0, -1):
    if (matrizCI[j][i]!=matrizCI[j][i-1]):
      print(f"Entro al if")
      solucion[i] = matrizAgentes[j][i]
      j -= esfuerzos[i][solucion[i]]
    print(f"i: {i} j:{j}")
  
  #Caso primer grupo
  if(matrizCI[j][0]!=cIInicial):
    solucion[0] = matrizAgentes[j][0]
  
  print(f"Solución final: {solucion}")    
  return solucion
      
# ag1 = Clases.Agentes(3,-100,50,0.5)
# ag2 = Clases.Agentes(1,100,80,0.1)
# ag3 = Clases.Agentes(1,-10,0,0.5)

ag1 = Clases.Agentes(2,-17,25,0.309)
ag2 = Clases.Agentes(4,-54,88,0.339)
ag3 = Clases.Agentes(3,-4,75,0.365)
ag4 = Clases.Agentes(3,-87,-63,0.317)
ag5 = Clases.Agentes(7,-99,-40,0.968)

sec = [ag1, ag2, ag3, ag4, ag5]
redSocial = Clases.RedSocial(sec, 315)
solucionDinamica(redSocial)    