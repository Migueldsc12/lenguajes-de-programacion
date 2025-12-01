import sys
import unittest
from abc import ABC, abstractmethod
from typing import List, Tuple

# ==========================================
# 1. MODELO DE DATOS
# ==========================================

class TipoDeDato(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def get_info(self, estrategia: str) -> Tuple[int, int, int]:
        pass

class Atomico(TipoDeDato):
    """Tipos base como int, char."""
    def __init__(self, nombre: str, tamano: int, alineacion: int):
        super().__init__(nombre)
        self.tamano_base = tamano
        self.alineacion_base = alineacion

    def get_info(self, estrategia: str) -> Tuple[int, int, int]:
        return (self.tamano_base, self.alineacion_base, 0)

class Struct(TipoDeDato):
    """Registro que contiene una secuencia de otros tipos."""
    def __init__(self, nombre: str, campos: List[TipoDeDato]):
        super().__init__(nombre)
        self.campos = campos

    def get_info(self, estrategia: str) -> Tuple[int, int, int]:
        campos_a_procesar = list(self.campos)
        
        if estrategia == 'optimizado':
            campos_a_procesar.sort(key=lambda t: t.get_info('sin_empaquetar')[1], reverse=True)
            modo_calculo = 'sin_empaquetar'
        else:
            modo_calculo = estrategia

        if modo_calculo == 'empaquetado':
            tamano_total = sum(c.get_info('empaquetado')[0] for c in campos_a_procesar)
            alineacion_max = 1 
            return (tamano_total, alineacion_max, 0)

        # Lógica 'sin_empaquetar'
        offset_actual = 0
        alineacion_struct = 1
        desperdicio_acumulado = 0

        for campo in campos_a_procesar:
            c_tam, c_align, c_waste = campo.get_info('sin_empaquetar')
            
            padding = 0
            if offset_actual % c_align != 0:
                padding = c_align - (offset_actual % c_align)
            
            desperdicio_acumulado += padding + c_waste
            offset_actual += padding + c_tam
            
            alineacion_struct = max(alineacion_struct, c_align)

        padding_final = 0
        if alineacion_struct > 0 and offset_actual % alineacion_struct != 0:
            padding_final = alineacion_struct - (offset_actual % alineacion_struct)
        
        desperdicio_acumulado += padding_final
        tamano_total = offset_actual + padding_final

        return (tamano_total, alineacion_struct, desperdicio_acumulado)

class Union(TipoDeDato):
    """Registro variante: todos los campos comienzan en offset 0."""
    def __init__(self, nombre: str, campos: List[TipoDeDato]):
        super().__init__(nombre)
        self.campos = campos

    def get_info(self, estrategia: str) -> Tuple[int, int, int]:
        if not self.campos:
            return (0, 1, 0)
            
        max_tam = 0
        max_align = 1
        
        # Si es packed, asumimos align 1 y sin padding final
        if estrategia == 'empaquetado':
             for c in self.campos:
                c_tam, _, _ = c.get_info('empaquetado')
                max_tam = max(max_tam, c_tam)
             return (max_tam, 1, 0)

        # Si es sin_empaquetar u optimizado
        for c in self.campos:
            c_tam, c_align, _ = c.get_info('sin_empaquetar')
            max_tam = max(max_tam, c_tam)
            max_align = max(max_align, c_align)
            
        # El tamaño final de la union debe ser múltiplo de su alineación
        tamano_real = max_tam
        padding_final = 0
        
        if tamano_real % max_align != 0:
            padding_final = max_align - (tamano_real % max_align)
            tamano_real += padding_final
            
        # El desperdicio en una Union es ambiguo. 
        return (tamano_real, max_align, padding_final)


# ==========================================
# 2. CONTROLADOR
# ==========================================

class ManejadorDeTipos:
    def __init__(self):
        self.catalogo = {}

    def ejecutar_comando(self, linea: str) -> str:
        partes = linea.strip().split()
        if not partes:
            return ""
        
        accion = partes[0].upper()

        try:
            if accion == "ATOMICO":
                # ATOMICO <nombre> <tam> <align>
                if len(partes) != 4: return "Error: Argumentos inválidos para ATOMICO"
                nombre, tam, align = partes[1], int(partes[2]), int(partes[3])
                self.catalogo[nombre] = Atomico(nombre, tam, align)
                return f"Atómico '{nombre}' definido."

            elif accion == "STRUCT":
                # STRUCT <nombre> type1 type2 ...
                if len(partes) < 2: return "Error: Nombre de STRUCT faltante"
                nombre = partes[1]
                tipos_campos = self._resolver_tipos(partes[2:])
                self.catalogo[nombre] = Struct(nombre, tipos_campos)
                return f"Struct '{nombre}' definido con {len(tipos_campos)} campos."

            elif accion == "UNION":
                # UNION <nombre> type1 type2 ...
                if len(partes) < 2: return "Error: Nombre de UNION faltante"
                nombre = partes[1]
                tipos_campos = self._resolver_tipos(partes[2:])
                self.catalogo[nombre] = Union(nombre, tipos_campos)
                return f"Union '{nombre}' definida."

            elif accion == "DESCRIBIR":
                # DESCRIBIR <nombre>
                if len(partes) != 2: return "Error: Falta el nombre para DESCRIBIR"
                nombre = partes[1]
                if nombre not in self.catalogo: return f"Error: Tipo '{nombre}' no existe."
                
                obj = self.catalogo[nombre]
                
                res = [f"Información para '{nombre}':"]
                estrategias = [
                    ("Sin empaquetar", "sin_empaquetar"),
                    ("Empaquetado   ", "empaquetado"),
                    ("Optimizado    ", "optimizado")
                ]
                
                res.append(f"{'Estrategia':<15} | {'Tamaño':<8} | {'Alineación':<10} | {'Desperdicio':<10}")
                res.append("-" * 55)
                
                for etiqueta, clave in estrategias:
                    tam, align, waste = obj.get_info(clave)
                    res.append(f"{etiqueta:<15} | {tam:<8} | {align:<10} | {waste:<10}")
                
                return "\n".join(res)

            elif accion == "SALIR":
                return "SALIR"

            else:
                return f"Comando desconocido: {accion}"

        except ValueError:
            return "Error: Se esperaba un número entero en los parámetros."
        except KeyError as e:
            return f"Error: Tipo no definido utilizado en definición: {e}"

    def _resolver_tipos(self, lista_nombres: List[str]) -> List[TipoDeDato]:
        resultado = []
        for nombre in lista_nombres:
            if nombre not in self.catalogo:
                raise KeyError(nombre)
            resultado.append(self.catalogo[nombre])
        return resultado

# ==========================================
# 3. PRUEBAS UNITARIAS
# ==========================================

class TestSimuladorTipos(unittest.TestCase):
    def setUp(self):
        self.manejador = ManejadorDeTipos()
        self.manejador.ejecutar_comando("ATOMICO char 1 1")
        self.manejador.ejecutar_comando("ATOMICO int 4 4")
        self.manejador.ejecutar_comando("ATOMICO double 8 8")

    def test_atomico_simple(self):
        res = self.manejador.ejecutar_comando("DESCRIBIR int")
        self.assertIn("Sin empaquetar  | 4        | 4          | 0", res)

    def test_struct_padding(self):
        self.manejador.ejecutar_comando("STRUCT test1 char int")
        res = self.manejador.ejecutar_comando("DESCRIBIR test1")
        self.assertIn("Sin empaquetar  | 8", res) 
        self.assertIn("3", res)

    def test_struct_reordenado(self):
        self.manejador.ejecutar_comando("STRUCT ineficiente char int char")
        res = self.manejador.ejecutar_comando("DESCRIBIR ineficiente")
        self.assertIn("Sin empaquetar  | 12", res)
        self.assertIn("Optimizado      | 8", res)

    def test_union(self):
        self.manejador.ejecutar_comando("UNION mi_union int double")
        res = self.manejador.ejecutar_comando("DESCRIBIR mi_union")
        self.assertIn("Sin empaquetar  | 8", res)

    def test_struct_anidado(self):
        self.manejador.ejecutar_comando("STRUCT inner double char")
        self.manejador.ejecutar_comando("STRUCT outer char inner")  
        res = self.manejador.ejecutar_comando("DESCRIBIR outer")
        self.assertIn("Sin empaquetar  | 24", res)

    def test_errores(self):
        self.assertTrue("Error" in self.manejador.ejecutar_comando("STRUCT x tipo_inexistente"))
        self.assertTrue("Error" in self.manejador.ejecutar_comando("ATOMICO malo a b"))

# ==========================================
# 4. MAIN
# ==========================================

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        suite = unittest.TestLoader().loadTestsFromTestCase(TestSimuladorTipos)
        unittest.TextTestRunner(verbosity=2).run(suite)
        return

    manejador = ManejadorDeTipos()
    print("=== Simulador de Manejador de Tipos ===")
    print("Escriba 'SALIR' para terminar.")
    
    while True:
        try:
            linea = input(">> ")
            if not linea: continue
            
            resultado = manejador.ejecutar_comando(linea)
            
            if resultado == "SALIR":
                break
                
            print(resultado)
            print("-" * 20)
            
        except EOFError:
            break
        except Exception as e:
            print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()