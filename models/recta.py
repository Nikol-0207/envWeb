from .puntos import Point
class Rect:
    def __init__(self, x: float, y: float, ancho: float, alto: float):
        self._x = x  # Coordenada X del centro
        self._y = y  # Coordenada Y del centro
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
    def contains (self, point: Point):

        return (point.x >= self.x - self.ancho and
            point.x <= self.x + self.ancho and
            point.y >= self.y - self.alto and
            point.y <= self.y + self.alto) 
    def intersects(self, otro):
        """
        Verifica si este rectángulo se solapa con otro objeto Rect.
        """
        # Comprobamos si las áreas están totalmente separadas.
        # Si alguna de estas condiciones es True, NO hay intersección.
        fuera = (otro.x - otro.ancho > self.x + self.ancho or  
                 otro.x + otro.ancho < self.x - self.ancho or  
                 otro.y - otro.alto > self.y + self.alto or   
                 otro.y + otro.alto < self.y - self.alto)     

        return not fuera
    
    def subdividir(self):
        """Calcula y retorna los 4 cuadrantes hijos (NW, NE, SW, SE)"""
        mitad_w = self.ancho / 2
        mitad_h = self.alto / 2
        
        return {
            'nw': Rect(self.x - mitad_w, self.y - mitad_h, mitad_w, mitad_h),
            'ne': Rect(self.x + mitad_w, self.y - mitad_h, mitad_w, mitad_h),
            'sw': Rect(self.x - mitad_w, self.y + mitad_h, mitad_w, mitad_h),
            'se': Rect(self.x + mitad_w, self.y + mitad_h, mitad_w, mitad_h)
        }



    def __repr__(self):
        """Método para visualizar el objeto en consola"""
        return f"Rect(Centro:({self.x},{self.y}), Radio_W:{self.ancho}, Radio_H:{self.alto})"

