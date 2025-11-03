# Examen2 – Guía de compilación y pruebas

## Requisitos previos
- **Swift 5.7 o superior** instalado y disponible en la variable `PATH` (`swift`, `swiftc`).
- **Herramientas opcionales** para el reto extra: `python3`, `python` (2.x), `ruby` y/o `gcc`.
- **Permisos de ejecución** en scripts (`chmod +x`) cuando sea necesario.

## Instrucciones por carpeta

### `pregunta1/`
- **`b1.swift`** (problema de Collatz):
  ```bash
  swift pregunta1/b1.swift <numero_entero_positivo>
  ```
  - Usa la función `f(n)` y cuenta iteraciones hasta llegar a 1.
  - Para compilar a binario:
    ```bash
    swiftc pregunta1/b1.swift -o pregunta1/b1
    ./pregunta1/b1 <numero_entero_positivo>
    ```
- **`b2.swift`** (Merge sort genérico):
  ```bash
  swift pregunta1/b2.swift <elementos...>
  ```
  - Ordena números si todos los argumentos son enteros; en caso contrario ordena cadenas.
  - Compilación opcional:
    ```bash
    swiftc pregunta1/b2.swift -o pregunta1/b2
    ./pregunta1/b2 <elementos...>
    ```

### `pregunta2/`
Proyecto Swift Package Manager (`Package.swift`).

- **Compilación** (debug por defecto):
  ```bash
  swift build --package-path pregunta2
  ```
- **Ejecución del binario** (`pregunta2`):
  ```bash
  swift run --package-path pregunta2 pregunta2
  ```
  - El programa abre un REPL que acepta comandos `EVAL` y `MOSTRAR` en notación prefija (`PRE`) o posfija (`POST`).
- **Pruebas automatizadas**:
  ```bash
  swift test --package-path pregunta2
  ```
- **Construcción en modo `release` (opcional)**:
  ```bash
  swift build --package-path pregunta2 -c release
  ```

### `pregunta3/`
- **`c.swift`** (iterador ordenado):
  ```bash
  swift pregunta3/c.swift
  ```
  - Muestra en consola cómo el iterador recorre una lista desordenada en orden ascendente.
  - Compilación opcional:
    ```bash
    swiftc pregunta3/c.swift -o pregunta3/iterador
    ./pregunta3/iterador
    ```

### `pregunta4/`
- **`main.swift`** (análisis de tres implementaciones):
  ```bash
  swift pregunta4/main.swift
  ```
  - Ejecuta un informe comparando recursión directa, recursión de cola e implementación iterativa.
  - Para generar un binario y reutilizarlo:
    ```bash
    swiftc pregunta4/main.swift -O -o pregunta4/analisis
    ./pregunta4/analisis
    ```

### `extra/`
- **`maldad.sh`** (programa políglota):
  ```bash
  chmod +x extra/maldad.sh    # primera vez
  ./extra/maldad.sh <n>
  ```
  - Intenta ejecutarse con `python3`, `python` 2.x, `ruby` y, si no, se compila como programa en C usando `gcc`.
  - Devuelve un valor de una secuencia tribonacci basada en `n`. Requiere `n ≥ 2`.

## Consejos adicionales
- **Uso de rutas**: Todos los comandos se asumen ejecutados desde la raíz `Examen2/`.
