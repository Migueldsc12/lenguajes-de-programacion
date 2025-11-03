import Foundation

func iteradorOrdenado(_ lista: [Int]) -> AnySequence<Int> {
    
    var copiaLista = lista
    
    return AnySequence {
        return AnyIterator {
            guard let minElement = copiaLista.min() else {
                return nil
            }
            
            guard let index = copiaLista.firstIndex(of: minElement) else {
                return nil
            }
            
            copiaLista.remove(at: index)
            
            return minElement
        }
    }
}

// --- CÓDIGO DE PRUEBA ---

print("--- Prueba del Iterador Ordenado ---")

let listaDesordenada = [8, 3, 5, 1, 9, 2, 5, 4]

print("Lista Original: \(listaDesordenada)")
print("Elementos Ordenados:")

for numero in iteradorOrdenado(listaDesordenada) {
    print(numero)
}