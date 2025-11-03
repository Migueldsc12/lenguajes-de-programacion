# test_vector.py
import pytest
from vector import Vector3D

# --- Fixtures para crear vectores de prueba ---
@pytest.fixture
def v1():
    return Vector3D(1, 2, 3)

@pytest.fixture
def v2():
    return Vector3D(4, 5, 6)

# --- Pruebas de funcionalidades básicas ---
def test_creacion_y_representacion(v1):
    assert v1.x == 1 and v1.y == 2 and v1.z == 3
    assert repr(v1) == "Vector3D(1, 2, 3)"
    
def test_creacion_invalida():
    with pytest.raises(TypeError):
        Vector3D("a", 2, 3)

def test_igualdad(v1):
    assert v1 == Vector3D(1, 2, 3)
    assert v1 != Vector3D(3, 2, 1)

# --- Pruebas de operaciones entre vectores ---
def test_suma_vectores(v1, v2):
    assert v1 + v2 == Vector3D(5, 7, 9)

def test_resta_vectores(v1, v2):
    assert v1 - v2 == Vector3D(-3, -3, -3)

def test_producto_cruz(v1, v2):
    # 1*6 - 3*5 = 6 - 15 = -3
    # 3*4 - 1*6 = 12 - 6 = 6
    # 1*5 - 2*4 = 5 - 8 = -3
    assert v1 * v2 == Vector3D(-3, 6, -3)
    
def test_producto_punto(v1, v2):
    # 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
    assert v1 % v2 == 32

def test_norma(v1):
    # sqrt(1^2 + 2^2 + 3^2) = sqrt(1 + 4 + 9) = sqrt(14)
    assert abs(v1) == pytest.approx(3.741657, 0.001)

# --- Pruebas de operaciones con escalares ---
def test_suma_escalar(v1):
    assert v1 + 3 == Vector3D(4, 5, 6)
    assert 3 + v1 == Vector3D(4, 5, 6) # Conmutativa

def test_resta_escalar(v1):
    assert v1 - 2 == Vector3D(-1, 0, 1)
    assert 10 - v1 == Vector3D(9, 8, 7) # No conmutativa

def test_multiplicacion_escalar(v1):
    assert v1 * 3.0 == Vector3D(3.0, 6.0, 9.0)
    assert 3.0 * v1 == Vector3D(3.0, 6.0, 9.0) # Conmutativa

# --- Pruebas de expresiones compuestas ---
def test_expresiones_compuestas(v1, v2):
    a = Vector3D(1, 0, 0)
    b = Vector3D(0, 1, 0)
    c = Vector3D(0, 0, 1)
    
    # a * b + c
    resultado1 = a * b + c
    assert resultado1 == Vector3D(0, 0, 2) # (0,0,1) + (0,0,1)

    # (b + b) * (c - a)
    suma = b + b           # (0, 2, 0)
    resta = c - a          # (-1, 0, 1)
    resultado2 = suma * resta
    assert resultado2 == Vector3D(2, 0, 2)

    # a % (c * b)
    cruz = c * b           # (-1, 0, 0)
    resultado3 = a % cruz
    assert resultado3 == -1

    # (b + b) * (c % a)
    # El producto punto da un escalar (0), por lo que es (0,2,0) * 0
    dot_product = c % a
    resultado4 = (b + b) * dot_product
    assert resultado4 == Vector3D(0, 0, 0)

# --- Pruebas de operaciones no implementadas ---
def test_operaciones_not_implemented(v1):
    # Producto punto con un escalar debe fallar
    with pytest.raises(TypeError):
        _ = v1 % 5