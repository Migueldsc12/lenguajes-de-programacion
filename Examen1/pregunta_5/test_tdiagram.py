# test_tdiagram.py
import pytest
from tdiagram import TDiagramSimulator, main
from unittest.mock import patch

@pytest.fixture
def sim():
    """Crea una instancia nueva del simulador para cada prueba."""
    return TDiagramSimulator()

# --- Pruebas de Definición ---
def test_define_program(sim):
    sim.define_program("app1", "PYTHON")
    assert sim.programs["APP1"] == "PYTHON"

def test_define_interpreter(sim):
    sim.define_interpreter("C", "PYTHON")
    assert ("C", "PYTHON") in sim.interpreters

def test_define_translator(sim):
    sim.define_translator("C", "PASCAL", "ASM")
    assert ("C", "PASCAL", "ASM") in sim.translators

# --- Pruebas de Lógica 'is_executable' ---
def test_executable_directo(sim):
    sim.define_program("juego", "LOCAL")
    is_exec, _ = sim.is_executable("JUEGO")
    assert is_exec

def test_executable_con_interprete_directo(sim):
    sim.define_program("mi_app", "PYTHON")
    sim.define_interpreter("LOCAL", "PYTHON")
    is_exec, _ = sim.is_executable("MI_APP")
    assert is_exec

def test_cadena_de_interpretes(sim):
    sim.define_program("ai_model", "LISP")
    sim.define_interpreter("PYTHON", "LISP")
    sim.define_interpreter("LOCAL", "PYTHON")
    is_exec, _ = sim.is_executable("AI_MODEL")
    assert is_exec

def test_executable_con_traductor(sim):
    sim.define_program("legacy_code", "PASCAL")
    sim.define_translator("LOCAL", "PASCAL", "LOCAL")
    is_exec, _ = sim.is_executable("LEGACY_CODE")
    assert is_exec
    
def test_cadena_compleja_traductor_interprete(sim):
    sim.define_program("sistema_banco", "COBOL")
    sim.define_translator("C", "COBOL", "ASM")  # Traductor de COBOL a ASM, escrito en C
    sim.define_interpreter("LOCAL", "C")       # Intérprete para C (para correr el traductor)
    sim.define_interpreter("LOCAL", "ASM")     # Intérprete para ASM (para correr el resultado)
    is_exec, _ = sim.is_executable("SISTEMA_BANCO")
    assert is_exec

def test_no_ejecutable_sin_camino(sim):
    sim.define_program("app_perdida", "HASKELL")
    sim.define_interpreter("LOCAL", "PYTHON")
    is_exec, _ = sim.is_executable("APP_PERDIDA")
    assert not is_exec

def test_no_ejecutable_interprete_no_ejecutable(sim):
    sim.define_program("app_lejana", "LISP")
    sim.define_interpreter("C", "LISP") # Intérprete existe, pero C no es ejecutable
    is_exec, _ = sim.is_executable("APP_LEJANA")
    assert not is_exec

def test_manejo_de_ciclos(sim):
    sim.define_program("app_ciclica", "A")
    sim.define_interpreter("B", "A")
    sim.define_interpreter("A", "B")
    is_exec, _ = sim.is_executable("APP_CICLICA")
    assert not is_exec

def test_programa_no_definido(sim):
    is_exec, msg = sim.is_executable("INEXISTENTE")
    assert not is_exec
    assert "no está definido" in msg

# --- Prueba para la Interfaz de Usuario (main) ---
def test_main_flujo_completo(capsys):
    """Prueba un flujo completo simulando la entrada del usuario."""
    user_inputs = [
        "DEFINIR PROGRAMA mi_app PYTHON",
        "DEFINIR INTERPRETE LOCAL PYTHON",
        "EJECUTABLE mi_app",
        "DEFINIR TRADUCTOR C PASCAL ASM",
        "EJECUTABLE otro_app", # Programa no definido
        "DEFINIR PROGRAMA", # Comando inválido
        "SALIR"
    ]
    with patch('builtins.input', side_effect=user_inputs):
        main()
    
    captured = capsys.readouterr()
    output = captured.out
    
    assert "Programa 'MI_APP' en lenguaje 'PYTHON' definido" in output
    assert "Intérprete para 'PYTHON' en 'LOCAL' definido" in output
    assert "El programa 'MI_APP' es ejecutable" in output
    assert "Traductor de 'PASCAL' a 'ASM' en 'C' definido" in output
    assert "El programa 'OTRO_APP' no está definido" in output
    assert "Comando 'DEFINIR' incompleto" in output
    assert "Saliendo del simulador" in output