import pytest
from unittest.mock import patch
from buddy_system import BuddySystem, main

# --- Pruebas para la Lógica de la Clase BuddySystem ---

def test_inicializacion_potencia_de_dos():
    """Prueba que el sistema se inicializa correctamente con una potencia de 2."""
    memoria = BuddySystem(128)
    assert memoria.total_blocks == 128
    assert memoria.max_level == 7
    # El bloque inicial completo debe estar libre
    assert memoria.free_list[7] == [0]

def test_inicializacion_no_potencia_de_dos():
    """Prueba que falla la inicialización si el tamaño no es potencia de 2."""
    with pytest.raises(ValueError, match="debe ser una potencia de 2 positiva"):
        BuddySystem(100)

def test_reserva_simple_exitosa():
    """Prueba una reserva básica que no requiere división."""
    memoria = BuddySystem(64)
    resultado = memoria.reservar("proceso_a", 64)
    assert "Éxito" in resultado
    assert memoria.allocated["proceso_a"] == (0, 64)
    assert not memoria.free_list[6] # La lista de bloques de 64 debe estar vacía

def test_reserva_con_division():
    """Prueba una reserva que requiere dividir un bloque más grande."""
    memoria = BuddySystem(32)
    memoria.reservar("proceso_b", 10) # Necesita un bloque de 16 (2^4)
    assert memoria.allocated["proceso_b"] == (0, 16)
    # Debería quedar un buddy libre de tamaño 16 en la dirección 16
    assert memoria.free_list[4] == [16]
    assert not memoria.free_list[5]

def test_liberar_y_fusion_simple():
    """Prueba que al liberar dos buddies, estos se fusionan."""
    memoria = BuddySystem(16)
    memoria.reservar("p1", 8) # Ocupa de 0 a 7
    memoria.reservar("p2", 8) # Ocupa de 8 a 15
    
    memoria.liberar("p1")
    assert memoria.free_list[3] == [0] # Bloque de 8 libre en 0
    
    memoria.liberar("p2")
    # Al liberar p2, su buddy (p1) está libre, deben fusionarse.
    assert not memoria.free_list[3]
    assert memoria.free_list[4] == [0] # Bloque completo de 16 libre en 0

def test_liberar_sin_fusion():
    """Prueba que al liberar un bloque sin su buddy libre, no hay fusión."""
    memoria = BuddySystem(32)
    memoria.reservar("p1", 8) # en 0
    memoria.reservar("p2", 8) # en 8
    memoria.reservar("p3", 16) # en 16
    
    memoria.liberar("p1")
    # El buddy de p1 (en 8) está ocupado por p2, no debe haber fusión.
    assert memoria.free_list[3] == [0]
    assert "p2" in memoria.allocated

def test_error_nombre_duplicado():
    """Prueba que no se puede reservar con un nombre ya en uso."""
    memoria = BuddySystem(128)
    memoria.reservar("proceso_unico", 20)
    resultado = memoria.reservar("proceso_unico", 10)
    assert "Error: El nombre 'proceso_unico' ya está en uso" in resultado

def test_error_liberar_nombre_inexistente():
    """Prueba que no se puede liberar un proceso que no existe."""
    memoria = BuddySystem(32)
    resultado = memoria.liberar("proceso_fantasma")
    assert "Error: No se encontró ninguna reserva" in resultado

def test_error_memoria_insuficiente():
    """Prueba que falla si se solicita más memoria de la total."""
    memoria = BuddySystem(16)
    resultado = memoria.reservar("proceso_grande", 20)
    assert "Error: No hay suficiente memoria" in resultado

def test_error_fragmentacion():
    """Prueba el fallo por no encontrar un bloque contiguo lo suficientemente grande."""
    memoria = BuddySystem(16)
    memoria.reservar("p1", 4) # ocupa 0-3
    memoria.reservar("p2", 4) # ocupa 4-7
    memoria.reservar("p3", 8) # ocupa 8-15
    memoria.liberar("p2") # Libera el bloque 4-7
    
    resultado = memoria.reservar("p4", 8)
    assert "Error: No hay bloques libres que puedan satisfacer la solicitud" in resultado

# --- Pruebas para la Interfaz de Usuario (función main) ---

def test_main_argumento_faltante(capsys):
    """Prueba que el programa sale si no se proporciona el argumento de tamaño."""
    with pytest.raises(SystemExit):
        with patch('sys.argv', ['buddy_system.py']):
            main()
    
    captured = capsys.readouterr()
    assert "Uso: python buddy_system.py <cantidad_de_bloques>" in captured.out

def test_main_argumento_no_potencia_de_2(capsys):
    """Prueba que el programa sale si el argumento no es una potencia de 2."""
    with pytest.raises(SystemExit):
        with patch('sys.argv', ['buddy_system.py', '100']):
            main()
            
    captured = capsys.readouterr()
    assert "Error al inicializar: La cantidad total de bloques debe ser una potencia de 2 positiva." in captured.out

def test_main_flujo_completo_simulado(capsys):
    """
    Prueba un flujo completo de comandos simulando la entrada del usuario
    para cubrir el bucle principal.
    """
    with patch('sys.argv', ['buddy_system.py', '32']):
        user_inputs = [
            "RESERVAR 10 p1",
            "MOSTRAR",
            "LIBERAR p1",
            "COMANDO_INVALIDO",
            "RESERVAR texto p2",  # Entrada inválida para cantidad
            "RESERVAR 10",         # Formato incorrecto
            "LIBERAR",             # Formato incorrecto
            "SALIR"
        ]
        with patch('builtins.input', side_effect=user_inputs):
            main()
            
    captured = capsys.readouterr()
    # Verifica que los mensajes clave se imprimieron en la terminal
    assert "Manejador de memoria iniciado con 32 bloques" in captured.out
    assert "Éxito: Se reservaron 16 bloques para 'p1'" in captured.out
    assert "ESTADO DE LA MEMORIA" in captured.out
    assert "Éxito: Se liberó la memoria de 'p1'" in captured.out
    assert "Error: Comando 'COMANDO_INVALIDO' no reconocido" in captured.out
    assert "Error: La cantidad debe ser un número entero." in captured.out
    assert "Error: Formato incorrecto. Uso: RESERVAR <cantidad> <nombre>" in captured.out
    assert "Error: Formato incorrecto. Uso: LIBERAR <nombre>" in captured.out
    assert "Saliendo del programa." in captured.out