import Clases
import math
import copy
import heapq

#Recibe el sga de la red y calcula el CI de dicha red
def calcularCI(red):
  totalAgentes = len(red)
  num = 0
  for ag in red:
    num += ag.n * math.pow((ag.o1 - ag.o2), 2) 
  
  return num / totalAgentes

#Recibe la red y las cantidades de agentes a cambiar y calcula la RS'
def obtenerNuevaRed(redSocial, e):
  solucion = copy.deepcopy(redSocial)
  for i in range (len(solucion.sag)):
    solucion.sag[i].n -= e[i]
    
  return solucion

#Recibe el sag de la red y calcula los esfuerzos necesarios para cada
def matrizEsfuerzo(redSocial):
  matriz = []
  matrizInterna = []
  for i in range (0, len(redSocial)):
    for j in range (0, redSocial[i].n):
      matrizInterna.append(math.ceil(math.fabs(redSocial[i].o1 - redSocial[i].o2) * redSocial[i].r *(j+1)))
    matriz.append(matrizInterna)
    matrizInterna = []
    
  return(matriz)

#Recibe el esfuerzo, y la matriz de esfuerzos para ese grupo
def maxEsfuerzo(esfuerzo, matrizE):
  maxE=0
  cant=0
  for i in matrizE:
    if(i<= esfuerzo and i>maxE):
      maxE=i
      cant+=1
  
  return(cant,maxE)

#print(maxEsfuerzo(300,[75,150,225]))

#Encuentra las cantidades para la solución
#Recibe las dos matrices, la cantidad de grupos, maxEsf, matrizEsf y CIIinicial
def encontrarSolucion(matrizCI, matrizAgentes, n, esfuerzoMax, esfuerzos, cIInicial):
  solucion = [0]*n  
  j = esfuerzoMax
    
  for i in range (n-1,0, -1):
    if (matrizCI[j][i]!=matrizCI[j][i-1]):
      solucion[i] = matrizAgentes[j][i]
      j -= esfuerzos[i][solucion[i]]
  
  #Caso primer grupo
  if(matrizCI[j][0]!=cIInicial):
    solucion[0] = matrizAgentes[j][0]
       
  return solucion

def solucionDinamica(redSocial):
  
  #Inicializar variables y matrices
  grupos=redSocial.sag
  cIInicial = calcularCI(grupos)
  n = len(grupos)
  esfuerzos = matrizEsfuerzo(grupos)
  esfuerzoMax = redSocial.r_max
  matrizCI = [[None] * (n) for _ in range(esfuerzoMax + 1)] 
  matrizAgentes = [[0] * (n) for _ in range(esfuerzoMax + 1)]
  solucionesParciales = [[0] * (n) for _ in range(esfuerzoMax + 1)]
  
  #Recorrer y llenar matrices
  for i in range(0,n):
    for j in range (0,esfuerzoMax+1):
      maxCambio = maxEsfuerzo(j,esfuerzos[i])
      
      #CASO TRIVIAL    
      if (i==0):                  
        e = [0]*n
        e[i] = maxCambio[0]
        redModificada = obtenerNuevaRed(redSocial, e)
        conflictoVariable = calcularCI(redModificada.sag)
        matrizCI[j][i] = conflictoVariable
        matrizAgentes[j][i] = maxCambio[0]
        solucionesParciales[j][i] = copy.deepcopy(e)
      
      #CASO DINÁMICO
      else:
        izquierda = matrizCI[j][i-1]
        
        #Cuando no puedo cambiar ningún agente
        if(maxCambio[0]==0):
          matrizCI[j][i] = izquierda
          matrizAgentes[j][i] = 0
          solucionesParciales[j][i] = copy.deepcopy(solucionesParciales[j][i-1])
        
        #Cuando puedo cambiar 1
        elif (maxCambio[0]==1):
          posRef = j-maxCambio[1]
          e = copy.deepcopy(solucionesParciales[posRef][i-1])
          e[i]=1
          redModificada = obtenerNuevaRed(redSocial, e)
          conflictoVariable = calcularCI(redModificada.sag)
          
          if(izquierda<=conflictoVariable):
            matrizCI[j][i] = izquierda
            matrizAgentes[j][i] = 0
            solucionesParciales[j][i] = copy.deepcopy(solucionesParciales[j][i-1])
          else:
            matrizCI[j][i] = conflictoVariable
            matrizAgentes[j][i] = 1
            #Creo qeu aquí se calcula la solución con la función
            solucionesParciales[j][i] = copy.deepcopy(e)
        
        #Cuando puedo cambiar 2 o más
        else:
          arregloValores = [(izquierda,0,solucionesParciales[j][i-1])]
          
          for k in range (0,maxCambio[0]):
            posRef = j-esfuerzos[i][k]
            print("posRef: ",posRef)
            e = copy.deepcopy(solucionesParciales[posRef][i-1])
            e[i]=k
            redModificada = obtenerNuevaRed(redSocial, e)
            conflictoVariable = calcularCI(redModificada.sag)
            arregloValores.append((conflictoVariable,k,e))
          
          heapq.heapify(arregloValores)
          matrizCI[j][i] = arregloValores[0][0]
          matrizAgentes[j][i] = arregloValores[0][1]
          solucionesParciales[j][i] = copy.deepcopy(arregloValores[0][2])

ag1 = Clases.Agentes(2,-17,25,0.309)
ag2 = Clases.Agentes(4,-54,88,0.339)
ag3 = Clases.Agentes(3,-4,75,0.365)
ag4 = Clases.Agentes(3,-87,-63,0.317)
ag5 = Clases.Agentes(7,-99,-40,0.968)

sec = [ag1, ag2, ag3, ag4, ag5]
redSocial = Clases.RedSocial(sec, 315)
solucionDinamica(redSocial)    
          
          
        
