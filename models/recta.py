from .puntos import Point
class Rect:
    def __init__(self, x: float, y: float, ancho: float, alto: float):
        self._x = x  
        self._y = y  
        self._ancho = ancho  
        self._alto = alto    


    @property
    def x (self):
        return self._x
    @x.setter
    def x (self, coordenada:float):
        try:
            self._x = float(coordenada)
        except ValueError:
            raise ValueError(f"La coordenada del eje x={coordenada} no es decimal")
    
    @property
    def y(self): 
        return self._y
    @y.setter
    def y(self, coordenada): 
        try:
            self._y = float(coordenada)
        except ValueError:
            raise ValueError(f"La coordenada del eje y={coordenada} no es decimal")   

    @property
    def ancho(self): 
        return self._ancho
    @ancho.setter
    def ancho(self, v): 
        self._ancho = float(v)

    @property
    def alto(self): 
        return self._alto
    @alto.setter
    def alto(self, v): 
        self._alto = float(v)
    
    """Implementacion"""
    def contains(self, point: Point):
        return (point.x >= self.x - self.ancho and
                point.x <= self.x + self.ancho and
                point.y >= self.y - self.alto and
                point.y <= self.y + self.alto)

    def intersects(self, otro):
        fuera = (otro.x - otro.ancho > self.x + self.ancho or  
                 otro.x + otro.ancho < self.x - self.ancho or  
                 otro.y - otro.alto > self.y + self.alto or   
                 otro.y + otro.alto < self.y - self.alto)     
        return not fuera

    def partir(self, punto: Point, eje: int):
        """
        Divide este rectángulo en dos basándose en la posición de un punto y un eje.
        eje 0 = Vertical (X), eje 1 = Horizontal (Y)
        """
        if eje == 0: # División Vertical (Eje X)
            # El nuevo ancho de los hijos es la distancia desde el borde hasta el punto
            ancho_izq = (punto.x - (self.x - self.ancho)) / 2
            ancho_der = ((self.x + self.ancho) - punto.x) / 2
            
            centro_x_izq = (self.x - self.ancho) + ancho_izq
            centro_x_der = (self.x + self.ancho) - ancho_der
            
            return (
                Rect(centro_x_izq, self.y, ancho_izq, self.alto), # Izquierda
                Rect(centro_x_der, self.y, ancho_der, self.alto)  # Derecha
            )
        else: # División Horizontal (Eje Y)
            alto_inf = (punto.y - (self.y - self.alto)) / 2
            alto_sup = ((self.y + self.alto) - punto.y) / 2
            
            centro_y_inf = (self.y - self.alto) + alto_inf
            centro_y_sup = (self.y + self.alto) - alto_sup
            
            return (
                Rect(self.x, centro_y_inf, self.ancho, alto_inf), # Abajo (Izquierda en árbol)
                Rect(self.x, centro_y_sup, self.ancho, alto_sup)  # Arriba (Derecha en árbol)
            )

    def __repr__(self):
        return f"Rect(({self.x},{self.y}), w:{self.ancho}, h:{self.alto})"
    


    
