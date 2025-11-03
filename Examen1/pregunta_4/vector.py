# vector.py
import math

class Vector3D:
    """
    Una clase para representar vectores tridimensionales y operar con ellos.

    Soporta:
    - Suma (+): Vector + Vector o Vector + Escalar
    - Resta (-): Vector - Vector o Vector - Escalar
    - Producto Cruz (*): Vector * Vector
    - Multiplicación Escalar (*): Vector * Escalar
    - Producto Punto (%): Vector % Vector
    - Norma (abs()): abs(Vector)
    """
    def __init__(self, x, y, z):
        if not all(isinstance(i, (int, float)) for i in [x, y, z]):
            raise TypeError("Las coordenadas del vector deben ser numéricas.")
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """Representación del vector como string, útil para debugging."""
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        """Compara si dos vectores son iguales."""
        return isinstance(other, Vector3D) and self.x == other.x and self.y == other.y and self.z == other.z

    # Operación de Suma (+)
    def __add__(self, other):
        """Sobrecarga del operador +. Suma con otro vector o un escalar."""
        if isinstance(other, Vector3D):
            return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        if isinstance(other, (int, float)):
            return Vector3D(self.x + other, self.y + other, self.z + other)
        return NotImplemented

    def __radd__(self, other):
        """Permite la suma conmutativa (ej. 3 + vector)."""
        return self.__add__(other)

    # Operación de Resta (-)
    def __sub__(self, other):
        """Sobrecarga del operador -. Resta con otro vector o un escalar."""
        if isinstance(other, Vector3D):
            return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        if isinstance(other, (int, float)):
            return Vector3D(self.x - other, self.y - other, self.z - other)
        return NotImplemented

    def __rsub__(self, other):
        """Permite la resta por la izquierda (ej. 3 - vector)."""
        if isinstance(other, (int, float)):
            return Vector3D(other - self.x, other - self.y, other - self.z)
        return NotImplemented
        
    # Operación de Multiplicación (*): Producto Cruz o Multiplicación Escalar
    def __mul__(self, other):
        """
        Sobrecarga del operador *.
        - Si 'other' es un Vector3D, calcula el producto cruz.
        - Si 'other' es un escalar, calcula la multiplicación escalar.
        """
        if isinstance(other, Vector3D): # Producto Cruz
            x = self.y * other.z - self.z * other.y
            y = self.z * other.x - self.x * other.z
            z = self.x * other.y - self.y * other.x
            return Vector3D(x, y, z)
        if isinstance(other, (int, float)): # Multiplicación Escalar
            return Vector3D(self.x * other, self.y * other, self.z * other)
        return NotImplemented
    
    def __rmul__(self, other):
        """Permite la multiplicación conmutativa (ej. 3 * vector)."""
        return self.__mul__(other)

    # Operación de Producto Punto (%)
    def __mod__(self, other):
        """Sobrecarga del operador % para el producto punto."""
        if isinstance(other, Vector3D):
            return self.x * other.x + self.y * other.y + self.z * other.z
        return NotImplemented

    # Operación de Norma (usando abs())
    def __abs__(self):
        """Sobrecarga de la función abs() para calcular la norma (magnitud) del vector."""
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)