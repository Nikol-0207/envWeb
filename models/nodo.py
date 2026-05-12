from .puntos import Point

class NodoTree:
    def __init__(self, punto, eje ):
        self._punto = punto           #Objeto de clase Point
        self._eje= eje                #0 para el eje X, 1 para el eje Y
        """Hijos"""
        self._izq= None
        self._der= None
     
    """Getters and Setters"""
    @property         #decorador para poder usar un metodo como un <atributo>
    def punto(self):
        return self._punto

    @property
    def eje(self):
        return self._eje

    @property
    def izq(self):
        return self._izq

    @izq.setter
    def izq(self, nodo):
        self._izq = nodo

    @property
    def der(self):
        return self._der

    @der.setter
    def der(self, nodo):
        self._der = nodo

    
    