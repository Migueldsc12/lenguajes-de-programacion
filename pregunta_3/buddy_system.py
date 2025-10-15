# buddy_system.py
import sys
import math

class BuddySystem:
    """
    Simula un manejador de memoria que implementa el algoritmo buddy system.
    """
    def __init__(self, total_blocks):
        # Valida que el tamaño sea una potencia de 2.
        if not (total_blocks > 0 and (total_blocks & (total_blocks - 1)) == 0):
            raise ValueError("La cantidad total de bloques debe ser una potencia de 2 positiva.")

        self.total_blocks = total_blocks
        # El número de niveles en el árbol es log2(total_blocks) + 1
        self.max_level = int(math.log2(total_blocks))
        
        # Lista de listas para los bloques libres. free_list[i] contiene bloques de tamaño 2**i.
        self.free_list = [[] for _ in range(self.max_level + 1)]
        # El bloque inicial completo está en el nivel más alto.
        self.free_list[self.max_level].append(0) 
        
        # Diccionario para rastrear los bloques reservados: {nombre: (dirección, tamaño)}
        self.allocated = {}

    def _get_buddy_address(self, address, size):
        """Calcula la dirección del bloque "buddy"."""
        return address ^ size # Operación XOR

    def reservar(self, nombre, cantidad):
        """Reserva una cantidad de bloques de memoria para un proceso."""
        if nombre in self.allocated:
            return f"Error: El nombre '{nombre}' ya está en uso."
        
        if cantidad <= 0:
            return "Error: La cantidad a reservar debe ser positiva."

        # Calcular el tamaño del bloque necesario (la potencia de 2 más cercana)
        level_needed = math.ceil(math.log2(cantidad))
        size_needed = 2**level_needed

        if size_needed > self.total_blocks:
            return f"Error: No hay suficiente memoria para reservar {cantidad} bloques."

        # Buscar un bloque libre del tamaño adecuado, comenzando desde el nivel necesario.
        level_found = -1
        for i in range(level_needed, self.max_level + 1):
            if self.free_list[i]:
                level_found = i
                break
        
        if level_found == -1:
            return "Error: No hay bloques libres que puedan satisfacer la solicitud (memoria fragmentada)."

        # Tomar el primer bloque disponible del nivel encontrado.
        block_address = self.free_list[level_found].pop(0)

        # Si el bloque es más grande de lo necesario, dividirlo.
        while level_found > level_needed:
            level_found -= 1
            block_size = 2**level_found
            buddy_address = block_address + block_size
            self.free_list[level_found].append(buddy_address)
        
        self.allocated[nombre] = (block_address, size_needed)
        return f"Éxito: Se reservaron {size_needed} bloques para '{nombre}' en la dirección {block_address}."

    def liberar(self, nombre):
        """Libera la memoria asignada a un proceso."""
        if nombre not in self.allocated:
            return f"Error: No se encontró ninguna reserva con el nombre '{nombre}'."

        address, size = self.allocated.pop(nombre)
        
        level = int(math.log2(size))

        # Intentar fusionar el bloque liberado con su buddy.
        while level < self.max_level:
            buddy_address = self._get_buddy_address(address, size)
            
            # Verificar si el buddy está en la lista de libres.
            try:
                self.free_list[level].remove(buddy_address)
                # Si se pudo remover, significa que el buddy estaba libre. Fusionar.
                address = min(address, buddy_address) # La nueva dirección es la menor de las dos.
                size *= 2
                level += 1
            except ValueError:
                # El buddy no está libre, no se puede fusionar más.
                break
        
        # Añadir el bloque (ya fusionado o no) a la lista de libres.
        self.free_list[level].append(address)
        return f"Éxito: Se liberó la memoria de '{nombre}'."

    def mostrar(self):
        """Muestra el estado actual de la memoria."""
        print("-" * 40)
        print("ESTADO DE LA MEMORIA")
        print("-" * 40)
        print("Bloques Reservados:")
        if not self.allocated:
            print("  (Ninguno)")
        else:
            for nombre, (addr, size) in sorted(self.allocated.items()):
                print(f"  - {nombre}: tamaño={size}, dirección={addr}")
        
        print("\nBloques Libres por Nivel (tamaño=2^nivel):")
        for i in range(self.max_level + 1):
            size = 2**i
            blocks = sorted(self.free_list[i])
            print(f"  Nivel {i} (tamaño {size}): {blocks if blocks else '(Ninguno)'}")
        print("-" * 40)

def main():
    """Función principal que maneja la interacción con el usuario."""
    if len(sys.argv) != 2:
        print("Uso: python buddy_system.py <cantidad_de_bloques>")
        sys.exit(1)
    
    try:
        total_blocks = int(sys.argv[1])
        memoria = BuddySystem(total_blocks)
    except ValueError as e:
        print(f"Error al inicializar: {e}")
        sys.exit(1)

    print(f"Manejador de memoria iniciado con {total_blocks} bloques.")
    print("Comandos disponibles: RESERVAR <cant> <nombre>, LIBERAR <nombre>, MOSTRAR, SALIR")

    while True:
        try:
            comando = input("> ").strip().upper().split()
            if not comando:
                continue

            accion = comando[0]

            if accion == "RESERVAR":
                if len(comando) != 3:
                    print("Error: Formato incorrecto. Uso: RESERVAR <cantidad> <nombre>")
                    continue
                cantidad = int(comando[1])
                nombre = comando[2].lower() # Guardar nombres en minúscula para evitar duplicados
                print(memoria.reservar(nombre, cantidad))
            
            elif accion == "LIBERAR":
                if len(comando) != 2:
                    print("Error: Formato incorrecto. Uso: LIBERAR <nombre>")
                    continue
                nombre = comando[1].lower()
                print(memoria.liberar(nombre))

            elif accion == "MOSTRAR":
                memoria.mostrar()
            
            elif accion == "SALIR":
                print("Saliendo del programa.")
                break
            
            else:
                print(f"Error: Comando '{accion}' no reconocido.")

        except ValueError:
            print("Error: La cantidad debe ser un número entero.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()