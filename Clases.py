

class RedSocial:
    def __init__(self, sag, r_max):
        self.sag = sag
        self.r_max = r_max

    def __str__(self):
        return f'<{self.sag}, {self.r_max}>'
    
class Agentes:
    def __init__(self, n, o1, o2, r):
        self.n = n
        self.o1 = o1
        self.o2 = o2
        self.r = r

    def __str__(self):
        return f'({self.n}, {self.o1}, {self.o2}, {self.r})'
    
class Salida:
    def __init__(self, e, esfuerzo, ci, nuevaRed):
        self.e = e
        self.esfuerzo = esfuerzo
        self.ci = ci
        self.nuevaRed = nuevaRed

    def __str__(self):
        return f'<{self.e}, {self.ci}, {self.esfuerzo}>'
    
    
   