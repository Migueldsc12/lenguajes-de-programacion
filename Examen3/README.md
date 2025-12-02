# Parte teorica
En el pdf encontrara el link al video de la primera pregunta y la parte 1 (teorica) de la segunda pregunta.
main.py es el programa de la parte 2

# Simulador de Manejo de Memoria para Tipos de Datos

Este proyecto es una herramienta en Python que simula cómo se organizan los tipos de datos en memoria. Permite definir tipos atómicos, estructuras y uniones, y calcular su **tamaño**, **alineación** y **desperdicio (padding)** bajo diferentes estrategias de empaquetado.

## 📋 Características

* Definición de tipos **Atómicos** (int, char, double, etc.).
* Creación de **Structs** (con cálculo de padding y alineación).
* Creación de **Unions** (superposición de memoria).
* Cálculo de métricas con tres estrategias:
    * **Sin empaquetar:** Comportamiento estándar de C/C++.
    * **Empaquetado:** Sin padding (`__attribute__((packed))`).
    * **Optimizado:** Reordenamiento automático de campos para minimizar el desperdicio.

## 🚀 Requisitos Previos

* **Python 3.x** instalado.
* **Coverage** (para el reporte de pruebas).

## 🛠️ Instalación y Configuración

Se recomienda utilizar un entorno virtual para mantener las dependencias aisladas.

### 1. Crear el entorno virtual
En la terminal, dentro de la carpeta del proyecto:

python3 -m venv venv

### 2. Activar el entorno
source venv/bin/activate

### 3. Instalar coverage
pip install coverage

### 4. Ejecutar el programa
python main.py

### 5. Ejecutar pruebas
python main.py test

### 6. Ver porcentaje de cobertura
coverage run main.py test

### 7. Ver reporte en la terminal
coverage report -m

### 8. Opcionalmente se puede generar un html del reporte
coverage html



## Ejemplo de uso
>> ATOMICO char 1 1
Atómico 'char' definido.

>> ATOMICO int 4 4
Atómico 'int' definido.

>> STRUCT ejemplo char int char
Struct 'ejemplo' definido con 3 campos.

>> DESCRIBIR ejemplo
Información para 'ejemplo':
Estrategia      | Tamaño   | Alineación | Desperdicio
-------------------------------------------------------
Sin empaquetar  | 12       | 4          | 6         
Empaquetado     | 6        | 1          | 0         
Optimizado      | 8        | 4          | 2
