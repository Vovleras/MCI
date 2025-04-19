import math
import copy
import heapq

class RedSocial:
  def __init__(self, sag, r_max):
    self.sag = sag
    self.r_max = r_max

  def __str__(self):
    return f'<{self.sag}, {self.r_max}>'
    
#n: Cantidad de agentes en el grupo
#oi: Opiniones
#r: Nivel de rigidez
class Agentes:
  def __init__(self, n, o1, o2, r):
    self.n = n
    self.o1 = o1
    self.o2 = o2
    self.r = r

  def __str__(self):
    return f'({self.n}, {self.o1}, {self.o2}, {self.r})'
    
class Salida:
  def __init__(self, e, esfuerzo, ci):
    self.e = e
    self.esfuerzo = esfuerzo
    self.ci = ci

  def __str__(self):
    return f'<{self.e}, {self.ci}, {self.esfuerzo}>'
      
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
  cant=0
  maxE=0
  for i in matrizE:
    if(i<= esfuerzo and i>maxE):
      maxE=i
      cant+=1
  
  return(cant)

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

def encontrarSolucionParcial(matriz, n, esfuerzoMax, esfuerzos, cIInicial, solucion):
  #print("Entro a hallar solucion")
  j = esfuerzoMax
    
  for i in range (n,0, -1):
    if (matriz[j][i][0]!=matriz[j][i-1][0]):
      #print(f"Entro al if")
      solucion[i] = matriz[j][i-1][1]
      j -= esfuerzos[i][solucion[i]]
    #print(f"i: {i} j:{j}")
  
  #Caso primer grupo
  if(matriz[j][0][0]!=cIInicial):
    solucion[0] = matriz[j][0][1]
  
  #print(f"Solución final: {solucion}")    
  return solucion

def solucionDinamica(redSocial):
  
  #Inicializar variables y matrices
  grupos=redSocial.sag
  cIInicial = calcularCI(grupos)
  n = len(grupos)
  esfuerzos = matrizEsfuerzo(grupos)
  esfuerzoMax = redSocial.r_max
  matrizFinal = [[(cIInicial,0)] * (n) for _ in range(esfuerzoMax + 1)] 
  
  #Recorrer y llenar matrices
  for i in range(0,n):
    for j in range (0,esfuerzoMax+1):
      maxCambio = maxEsfuerzo(j,esfuerzos[i])
      
      #CASO TRIVIAL    
      if (i==0 and maxCambio>0):   
        e = [0]*n
        e[i] = maxCambio
        redModificada = obtenerNuevaRed(redSocial, e)
        conflictoVariable = calcularCI(redModificada.sag)
        matrizFinal[j][i] = (conflictoVariable,maxCambio)
      
      #CASO DINÁMICO
      elif(i>0):
        izquierda = matrizFinal[j][i-1][0]
        
        #Cuando no puedo cambiar ningún agente
        if(maxCambio<1):
          matrizFinal[j][i] = (izquierda,0)
        
        #Cuando puedo cambiar 1 o más
        else:
          arregloValores = [(izquierda,0)]
          
          for k in range (1,maxCambio+1):
            #posRef = j-esfuerzos[i][k]
            posRef = j - math.ceil(math.fabs(redSocial.sag[i].o1 - redSocial.sag[i].o2) * redSocial.sag[i].r * (k))
            e = encontrarSolucionParcial(matrizFinal, i, posRef, esfuerzos, cIInicial, [0]*n)
            e[i]=k
            redModificada = obtenerNuevaRed(redSocial, e)
            valorComparar = calcularCI(redModificada.sag)
            arregloValores.append((valorComparar,k))
          
          heapq.heapify(arregloValores)
          matrizFinal[j][i] = (arregloValores[0][0],arregloValores[0][1])
          
  print(f"Matriz:")
  for j in range (0,esfuerzoMax+1):
    print(f"{j}\t{matrizFinal[j]}")

#Prueba 12
ag1 = Agentes(2,93,-9,0.062)
ag2 = Agentes(9,-4,60,0.121)
ag3 = Agentes(5,-69,-17,0.449)
ag4 = Agentes(8,-12,-18,0.068)
ag5 = Agentes(4,69,-55,0.634)
ag6 = Agentes(1,96,-13,0.063)
ag7 = Agentes(2,66,-89,0.667)
ag8 = Agentes(9,-26,-44,0.811)
ag9 = Agentes(1,29,95,0.502)
ag10 = Agentes(1,-95,-93,0.546)
ag11 = Agentes(4,94,-44,0.722)
ag12 = Agentes(2,1,81,0.046)
ag13 = Agentes(8,42,-2,0.118)
ag14 = Agentes(2,53,-59,0.613)
ag15 = Agentes(6,66,100,0.538)

sec = [ag1, ag2, ag3, ag4, ag5, ag6, ag7, ag8, ag9, ag10, ag11, ag12, ag13, ag14, ag15 ]
redSocial = RedSocial(sec, 116)
solucionDinamica(redSocial)