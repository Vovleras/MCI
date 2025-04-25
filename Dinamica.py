import funcionesAuxiliares
  
def solucionDinamica(redSocial):
  #Inicializar variables y matrices
  sag = redSocial.sag
  cIInicial = funcionesAuxiliares.calcularCI(sag)
  n = len(sag)
  esfuerzos = funcionesAuxiliares.matrizEsfuerzo(sag)
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
        redModificada = funcionesAuxiliares.obtenerNuevaRed(redSocial, e)
        conflictoVariable = funcionesAuxiliares.calcularCI(redModificada.sag)
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

            redModificada = funcionesAuxiliares.obtenerNuevaRed(redSocial, solParcial)
            valorComparar = funcionesAuxiliares.calcularCI(redModificada.sag)
            arregloValores.append([valorComparar, solParcial])
          
          ciMinimo = min(arregloValores, key=lambda x: x[0])
          matrizCI[j][i] = ciMinimo[0]
          matrizSolucion[j][i] = ciMinimo[1]
          
  solucion = matrizSolucion[esfuerzoMax][i]
  ci = matrizCI[esfuerzoMax][i]
  esfuerzo = funcionesAuxiliares.calcularEsfuerzoSol(solucion,esfuerzos)

  return solucion, ci, esfuerzo