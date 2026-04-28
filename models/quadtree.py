from .nodo import NodoQuad
class Quadtree:
    def __init__(self,limite_global, capacidad):
        self._raiz=NodoQuad(limite_global, capacidad)
    
    @property
    def raiz(self):
        return self._raiz

    def insertar(self, punto):
        """Punto de entrada para insertar un punto en el árbol"""
        return self._raiz.insertar(punto)

    def buscar(self, area_busqueda):
        """
        Punto de entrada para buscar puntos en un área específica.
        """
        encontrados = []
        self._raiz.buscar(area_busqueda, encontrados)
        return encontrados

    def obtener_todos_los_limites(self):
        """
        Recorre el árbol y devuelve una lista de todos los objetos Rect.
        """
        limites = []
        self._recorrer_limites(self._raiz, limites)
        return limites

    def _recorrer_limites(self, nodo, lista):
        """Método privado recursivo para recolectar rectángulos"""
        if nodo is None:
            return
        lista.append(nodo.limite)
        if nodo.dividido:
            self._recorrer_limites(nodo.nw, lista)
            self._recorrer_limites(nodo.ne, lista)
            self._recorrer_limites(nodo.sw, lista)
            self._recorrer_limites(nodo.se, lista)
    
        