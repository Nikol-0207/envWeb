from .nodo import NodoQuad
class Quadtree:
    def __init__(self,limite_global, capacidad):
        self._raiz=NodoQuad(limite_global, capacidad)
    
    
        