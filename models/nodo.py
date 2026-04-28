from .puntos import Point
from .recta import Rect
class NodoQuad:
    def __init__(self, limite, capacidad):
        """Clase Nodo con parametros limite de tipo Rect y capacidad de tipo int"""
        self._limite = limite      #Limites de la recta, obj geometrico (x,y,ancho,alto)
        self._capacidad = capacidad #De puntos que puede albergar una cuadrante
        self._puntos = []          # Lista de datos en un cuadrante (Point)
        self._dividido = False     # Flag para saber si tiene hijos
        """Hijos del Quadtree"""
        self._nw=None #cuadrante superior izquierdo
        self._ne=None #cuadrante superior derecho
        self._sw=None #cuadrante inferior izquierdo
        self._se=None #cuadrante inferior derecho
    
    """Getters and Setters"""
    @property         #decorador para poder usar un metodo como un <atributo>
    def limite (self):
        return self._limite 
    @limite.setter
    def limite (self, _limite):
        self._limite=_limite  
    
    @property
    def capacidad (self):
        return self._capacidad 
    @capacidad.setter
    def capacidad (self, valor):
        if (valor>0):
            self._capacidad=valor
        else:
            raise ValueError(f"Capacidad inválida: {valor}. Debe ser mayor a 0.")
        
    @property
    def puntos(self):
        return self._puntos
    
    @property
    def dividido(self):
        return self._dividido

    @dividido.setter
    def dividido(self, estado):
        if isinstance(estado, bool): #validacion para evitar datos que no sea de tipo bool
            self._dividido = estado
        

    """Getter and Setter de los hijos"""    
    @property
    def nw(self): 
        return self._nw

    @nw.setter
    def nw(self, nodo):
        self._nw = nodo

    @property
    def ne(self): 
        return self._ne

    @ne.setter
    def ne(self, nodo):
        self._ne = nodo

    @property
    def sw(self): 
        return self._sw

    @sw.setter
    def sw(self, nodo):
        self._sw = nodo

    @property
    def se(self): 
        return self._se

    @se.setter
    def se(self, nodo):
        self._se = nodo

    """Implementación de la clase"""
    def insertar(self, punto: Point):
        # Comprobar si el punto pertenece a este cuadrante
        if not self.limite.contains(punto):
            return False

        # Si hay espacio y es un nodo hoja (no está dividido), guardamos el punto
        if len(self.puntos) < self.capacidad and not self.dividido:
            self.puntos.append(punto)
            return True

        # Si está lleno, debemos dividir y repartir (o pasar a los hijos)
        if not self.dividido:
            self.subdividir()

        # Intentamos insertar el punto en cualquiera de los hijos
        # El primero que retorne True detendrá la ejecución
        if self.nw.insertar(punto): 
            return True
        if self.ne.insertar(punto):
            return True
        if self.sw.insertar(punto): 
            return True
        if self.se.insertar(punto): 
            return True

        return False

    def subdividir(self):
        # Le pedimos al rectángulo que calcule los 4 pedazos
        cuadrantes = self.limite.subdividir() 
    
        # Usamos esos pedazos para crear los nuevos nodos hijos con las llaves
        self.nw = NodoQuad(cuadrantes['nw'], self.capacidad)
        self.ne = NodoQuad(cuadrantes['ne'], self.capacidad)
        self.sw = NodoQuad(cuadrantes['sw'], self.capacidad)
        self.se = NodoQuad(cuadrantes['se'], self.capacidad)
    
        self.dividido = True
    def buscar(self, rango, encontrados):
        if not self.limite.intersects(rango):
            return
    
        for p in self.puntos:
            if rango.contains(p):
                encontrados.append(p)
            
        if self.dividido:
            self.nw.buscar(rango, encontrados)
            self.ne.buscar(rango, encontrados)
            self.sw.buscar(rango, encontrados)
            self.se.buscar(rango, encontrados)