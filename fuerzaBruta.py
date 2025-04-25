import copy
import funcionesAuxiliares

def maximoAgentes(redSocial):
    n = len(redSocial.sag)
    maxAgentes = []
    for i in range (n):
        maxAgentes.append(redSocial.sag[i].n)
    return maxAgentes
    

def modciFB(rs):
    maximos = maximoAgentes(rs)
    combinacion = [0] * len(maximos)
    e = [0] * len(maximos)
    solucion = copy.deepcopy(rs)

    def generarCombinacion(combinacion, index, red, solucion, e):
        if index == len(maximos):
            if (funcionesAuxiliares.calcularEsfuerzoRed(rs, combinacion) <= rs.r_max):
                nuevaRed = funcionesAuxiliares.obtenerNuevaRed(red, combinacion)
                if (funcionesAuxiliares.calcularCI(nuevaRed.sag) < funcionesAuxiliares.calcularCI(solucion.sag)):
                    solucion.sag = nuevaRed.sag
                    e[:] = combinacion[:]
            return
        for i in range(maximos[index] + 1):
            combinacion[index] = i
            generarCombinacion(combinacion, index + 1, red, solucion, e)

    generarCombinacion(combinacion, 0, rs, solucion, e)

    esfuerzo = funcionesAuxiliares.calcularEsfuerzoRed(solucion, e)
    ci = funcionesAuxiliares.calcularCI(solucion.sag)
    return e, ci, esfuerzo
