class Point:
    """Guarda las coordenadas x e y del punto"""
    def __init__(self, x: float, y: float, data=None):
        self._x = x
        self._y = y
        self._data = data 
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, valor):
        self._x = float(valor)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, valor):
        self._y = float(valor)

    @property
    def data(self):
        return self._data
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, valor):
        self._data = str(valor)
    
    #Método especial para la depuracion 
    def __repr__(self):
        return f"Point({self.x}, {self.y})"