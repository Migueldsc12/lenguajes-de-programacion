# Lenguajes de Programación - Proyecto de Ejercicios

Este proyecto contiene la implementación de varios ejercicios relacionados con lenguajes de programación. Cada pregunta está organizada en su propio directorio con implementaciones completas y pruebas unitarias.

## 📁 Estructura del Proyecto

```
Lenguajes/
├── pregunta_1/          # Funciones en MATLAB/Octave
├── pregunta_3/          # Sistema Buddy de gestión de memoria
├── pregunta_4/          # Clase Vector3D con operadores sobrecargados
├── pregunta_5/          # Simulador de Diagramas T
├── extra/               # Pregunta exta
└── README.md           # Este archivo
```

## 🔧 Requisitos del Sistema

- **Python 3.7+** (para preguntas 3, 4, 5)
- **MATLAB** (para pregunta 1)
- **pytest** (para ejecutar las pruebas)

### Instalación de Dependencias

```bash
# Instalar pytest para las pruebas
pip install pytest

# Opcional: Para coverage de código
pip install pytest-cov
```

## Descripción de Ejercicios

### Pregunta 1: Funciones MATLAB/Octave
**Archivos:** `pregunta_1/prod_transpuesta.m`, `pregunta_1/rotate.m`

Implementa dos funciones en MATLAB/Octave:
- **`prod_transpuesta(A)`**: Calcula el producto de una matriz por su transpuesta (A × A^T)
- **`rotate(w,k)`**: Rota una cadena de caracteres k posiciones hacia la izquierda

### Pregunta 3: Sistema Buddy de Gestión de Memoria
**Archivos:** `pregunta_3/buddy_system.py`, `pregunta_3/test_buddy_system.py`

Implementa un simulador del algoritmo **Buddy System** para gestión de memoria:
- Reserva y liberación de bloques de memoria
- División automática de bloques grandes
- Fusión de bloques buddy cuando se liberan
- Interfaz de línea de comandos interactiva

#### Ejecución:
```bash
cd pregunta_3
python buddy_system.py 128  # Inicia con 128 bloques
```

### Pregunta 4: Clase Vector3D
**Archivos:** `pregunta_4/vector.py`, `pregunta_4/test_vector.py`

Implementa una clase `Vector3D` con sobrecarga de operadores:
- **Suma (+)**: Vector + Vector, Vector + Escalar
- **Resta (-)**: Vector - Vector, Vector - Escalar  
- **Producto Cruz (*)**: Vector * Vector
- **Multiplicación Escalar (*)**: Vector * Escalar
- **Producto Punto (%)**: Vector % Vector
- **Norma (abs())**: abs(Vector)

#### Ejemplo de uso:
```python
from vector import Vector3D

v1 = Vector3D(1, 2, 3)
v2 = Vector3D(4, 5, 6)

suma = v1 + v2           # Vector3D(5, 7, 9)
producto_cruz = v1 * v2  # Producto cruz
producto_punto = v1 % v2 # Producto punto
norma = abs(v1)          # Magnitud del vector
```

### Pregunta 5: Simulador de Diagramas T
**Archivos:** `pregunta_5/tdiagram.py`, `pregunta_5/test_tdiagram.py`

Simula el comportamiento de **Diagramas T** para programas, intérpretes y traductores:
- Definición de programas en diferentes lenguajes
- Definición de intérpretes y traductores
- Verificación de ejecutabilidad de programas
- Traducción automática de programas
- Interfaz de línea de comandos

#### Ejecución:
```bash
cd pregunta_5
python tdiagram.py
```

### Extra: Código Compacto
**Archivo:** `extra/main.py`

Contiene una implementación extremadamente compacta (una línea) de un algoritmo matemático.

## Ejecutar las Pruebas

### Ejecutar pruebas por pregunta
```bash
# Pregunta 3: Sistema Buddy
cd pregunta_3
pytest test_buddy_system.py -v

# Pregunta 4: Vector3D
cd pregunta_4
pytest test_vector.py -v

# Pregunta 5: Diagramas T
cd pregunta_5
pytest test_tdiagram.py -v
```

### Ejecutar con coverage
```bash
# Coverage para una pregunta específica
cd pregunta_4
pytest test_vector.py --cov=vector --cov-report=html

# Coverage para todas las preguntas
pytest pregunta_3/ pregunta_4/ pregunta_5/ --cov=pregunta_3.buddy_system --cov=pregunta_4.vector --cov=pregunta_5.tdiagram
```

## 📝 Notas Adicionales

- Las pruebas cubren casos normales, límite y de error
- Los programas interactivos incluyen manejo robusto de entrada del usuario
- El código está documentado con docstrings y comentarios explicativos

**Autor:** Miguel Salomon 
**Fecha:** 14 de octubre 2025  
