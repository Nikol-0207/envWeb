from .nodo import NodoTree
class Kdtree:
    def __init__(self):
        self._raiz=None
    
    @property
    def raiz(self):
        return self._raiz
    
    """Implementación de la clase"""
    def insertar(self, punto):
        if self._raiz is None:
            self._raiz = NodoTree(punto, 0)    # El primer punto define el eje X (0)
            return True
        return self._insertar_recursivo(self._raiz, punto)
    def _insertar_recursivo(self, nodo_actual, punto_nuevo):
        eje = nodo_actual.eje
        
        # Usamos las propiedades de tu clase Point
        valor_nuevo = punto_nuevo.x if eje == 0 else punto_nuevo.y
        valor_actual = nodo_actual.punto.x if eje == 0 else nodo_actual.punto.y

        proximo_eje = 1 - eje

        if valor_nuevo < valor_actual:
            if nodo_actual.izq is None:
                nodo_actual.izq = NodoTree(punto_nuevo, proximo_eje)
            else:
                self._insertar_recursivo(nodo_actual.izq, punto_nuevo)
        else:
            if nodo_actual.der is None:
                nodo_actual.der = NodoTree(punto_nuevo, proximo_eje)
            else:
                self._insertar_recursivo(nodo_actual.der, punto_nuevo)
        return True
        