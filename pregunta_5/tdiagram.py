# tdiagram.py
import sys

class TDiagramSimulator:
    """
    Simula programas, intérpretes y traductores como en los diagramas de T.
    """
    def __init__(self):
        # Constante para el lenguaje de la máquina local
        self.LOCAL_LANGUAGE = "LOCAL"
        
        # Almacenes para las definiciones
        # {'nombre_programa': 'lenguaje'}
        self.programs = {}
        # {('lenguaje_base', 'lenguaje_interpretado'): True}
        self.interpreters = {}
        # {('base', 'origen', 'destino'): True}
        self.translators = {}

    def define_program(self, name, language):
        """Define un nuevo programa."""
        if name.upper() in self.programs:
            return f"Advertencia: Redefiniendo el programa '{name}'."
        self.programs[name.upper()] = language.upper()
        return f"Éxito: Programa '{name}' en lenguaje '{language.upper()}' definido."

    def define_interpreter(self, base_lang, target_lang):
        """Define un nuevo intérprete."""
        key = (base_lang.upper(), target_lang.upper())
        if key in self.interpreters:
            return f"Advertencia: Intérprete para '{target_lang.upper()}' en '{base_lang.upper()}' ya existe."
        self.interpreters[key] = True
        return f"Éxito: Intérprete para '{target_lang.upper()}' en '{base_lang.upper()}' definido."

    def define_translator(self, base_lang, source_lang, dest_lang):
        """Define un nuevo traductor."""
        key = (base_lang.upper(), source_lang.upper(), dest_lang.upper())
        if key in self.translators:
            return "Advertencia: Traductor ya existe."
        self.translators[key] = True
        return f"Éxito: Traductor de '{source_lang.upper()}' a '{dest_lang.upper()}' en '{base_lang.upper()}' definido."

    def is_executable(self, program_name):
        """
        Verifica si un programa es ejecutable en la máquina LOCAL.
        """
        if program_name.upper() not in self.programs:
            return False, f"Error: El programa '{program_name}' no está definido."
            
        program_language = self.programs[program_name.upper()]
        
        # Usamos un conjunto para evitar ciclos infinitos en la recursión
        visited = set()
        
        if self._can_run_language(program_language, self.LOCAL_LANGUAGE, visited):
            return True, f"El programa '{program_name}' es ejecutable."
        else:
            return False, f"El programa '{program_name}' NO es ejecutable."

    def _can_run_language(self, lang_to_run, machine_lang, visited):
        """
        Función recursiva para determinar si un lenguaje puede ejecutarse en una máquina.
        """
        # Caso base: El lenguaje es el nativo de la máquina.
        if lang_to_run == machine_lang:
            return True
        
        # Prevención de ciclos: si ya intentamos correr este lenguaje, detenemos la rama.
        if lang_to_run in visited:
            return False
        visited.add(lang_to_run)

        # Opción 1: Buscar un intérprete directo.
        # ¿Existe un intérprete para `lang_to_run` que se ejecute en `machine_lang`?
        if (machine_lang, lang_to_run) in self.interpreters:
            return True

        # Opción 2: Buscar un intérprete que necesite ser interpretado (cadena de intérpretes).
        # ¿Existe un intérprete para `lang_to_run` en `intermediate_lang`?
        # Si es así, ¿podemos ejecutar `intermediate_lang` en nuestra `machine_lang`?
        for base_lang, target_lang in self.interpreters:
            if target_lang == lang_to_run:
                if self._can_run_language(base_lang, machine_lang, visited.copy()):
                    return True

        # Opción 3: Buscar un traductor.
        # ¿Existe un traductor que convierta `lang_to_run` a `new_lang`?
        # Y, ¿podemos ejecutar el traductor Y el resultado de la traducción?
        for t_base, t_source, t_dest in self.translators:
            if t_source == lang_to_run:
                # Verificar si podemos ejecutar el traductor Y el lenguaje destino
                can_run_translator = self._can_run_language(t_base, machine_lang, visited.copy())
                if can_run_translator:
                    can_run_result = self._can_run_language(t_dest, machine_lang, visited.copy())
                    if can_run_result:
                        return True
        
        return False

def main():
    """Bucle principal de la interfaz de usuario."""
    sim = TDiagramSimulator()
    print("Simulador de Diagramas de T. Escriba 'SALIR' para terminar.")
    print("Ejemplos:")
    print("  DEFINIR PROGRAMA mi_app PYTHON")
    print("  DEFINIR INTERPRETE LOCAL PYTHON")
    print("  EJECUTABLE mi_app")

    while True:
        try:
            line = input("> ").strip().upper()
            if not line:
                continue

            parts = line.split()
            command = parts[0]

            if command == "SALIR":
                print("Saliendo del simulador.")
                break
            
            elif command == "DEFINIR":
                if len(parts) < 3:
                    print("Error: Comando 'DEFINIR' incompleto.")
                    continue
                
                def_type = parts[1]
                args = parts[2:]

                if def_type == "PROGRAMA" and len(args) == 2:
                    print(sim.define_program(args[0], args[1]))
                elif def_type == "INTERPRETE" and len(args) == 2:
                    print(sim.define_interpreter(args[0], args[1]))
                elif def_type == "TRADUCTOR" and len(args) == 3:
                    print(sim.define_translator(args[0], args[1], args[2]))
                else:
                    print(f"Error: Tipo de definición '{def_type}' o número de argumentos incorrecto.")

            elif command == "EJECUTABLE":
                if len(parts) != 2:
                    print("Error: Comando 'EJECUTABLE' requiere un nombre de programa.")
                    continue
                
                _, message = sim.is_executable(parts[1])
                print(message)
            
            else:
                print(f"Error: Comando '{command}' no reconocido.")

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()