from .nodo import NodoTree
import math

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
    def buscar_por_coordenadas(self, x, y):
        """Busca un punto exacto dadas sus coordenadas x e y"""
        return self._buscar_recursivo(self._raiz, x, y)

    def _buscar_recursivo(self, nodo_actual, x, y):
        # Caso base: No se encontró el punto
        if nodo_actual is None:
            return None
        
        if nodo_actual.punto.x == x and nodo_actual.punto.y == y:
            return nodo_actual.punto
        
        
        eje = nodo_actual.eje
        valor_buscado = x if eje == 0 else y
        valor_nodo = nodo_actual.punto.x if eje == 0 else nodo_actual.punto.y
        
        if valor_buscado < valor_nodo:
            return self._buscar_recursivo(nodo_actual.izq, x, y)
        else:
            # Recordar que en la inserción usamos >= para el lado derecho
            return self._buscar_recursivo(nodo_actual.der, x, y)
    def buscar_mas_cercano(self, x, y, omitir_exacto=True):
        """Busca el punto más cercano de otro, mediante coordenadas"""
        if self._raiz is None:
            return None
        return self._nn_recursivo(self._raiz, x, y, None, float('inf'), omitir_exacto)

    def _nn_recursivo(self, nodo, x, y, mejor_punto, mejor_distancia, omitir_exacto):
        if nodo is None:
            return mejor_punto, mejor_distancia

        dist_actual = math.sqrt((nodo.punto.x - x)**2 + (nodo.punto.y - y)**2)
        es_mismo_punto = dist_actual < 0.001
        
        if dist_actual < mejor_distancia:
            if not (omitir_exacto and es_mismo_punto):
                mejor_distancia = dist_actual
                mejor_punto = nodo.punto

        
        eje = nodo.eje
        valor_buscado = x if eje == 0 else y
        valor_nodo = nodo.punto.x if eje == 0 else nodo.punto.y

        proximo, otro = (nodo.izq, nodo.der) if valor_buscado < valor_nodo else (nodo.der, nodo.izq)

        mejor_punto, mejor_distancia = self._nn_recursivo(proximo, x, y, mejor_punto, mejor_distancia, omitir_exacto)

        if abs(valor_buscado - valor_nodo) < mejor_distancia:
            mejor_punto, mejor_distancia = self._nn_recursivo(otro, x, y, mejor_punto, mejor_distancia, omitir_exacto)

        return mejor_punto, mejor_distancia