import Foundation

/* --- Decisiones de Implementación ---
 *
 * 1. La función es genérica y puede ordenar
 * cualquier tipo de dato siempre que ese tipo sepa cómo compararse a sí mismo.
 * Esto permite que la función ordene `Int`, `String`, `Double`, etc.
 *
 * 2. Este es un algoritmo inherentemente recursivo.
 * `mergesort` se llama a sí mismo para las mitades izquierda y derecha.
 *
 * 3. crea explícitamente nuevos arrays para `leftHalf` y `rightHalf`. 
 * Aunque esto usa más memoria que manipular índices en un solo array,
 * simplifica enormemente la lógica y el manejo de la recursión.
 *
 * @param array El array de elementos a ordenar.
 * @return Un nuevo array con los elementos ordenados.
 */
func mergesort<T: Comparable>(_ array: [T]) -> [T] {
    
    guard array.count > 1 else {
        return array
    }
    
    let middleIndex = array.count / 2
    
    let leftHalf = Array(array[..<middleIndex])
    let rightHalf = Array(array[middleIndex...])
    
    let sortedLeft = mergesort(leftHalf)
    let sortedRight = mergesort(rightHalf)
    
    return merge(sortedLeft, sortedRight)
}

/* --- Decisiones de Implementación ---
 *
 * 1. Se marca como `private` porque es un
 * detalle de implementación de `mergesort`.
 *
 * 2. Esta es una optimización clave.
 * Sabemos el tamaño exacto del array final, así que le pedimos
 * a Swift que asigne toda la memoria una sola vez. Esto evita
 * costosas re-asignaciones de memoria cada vez que usamos `.append()`.
 *
 * 3. Usamos `leftIndex` y `rightIndex` como
 * dos "dedos" o punteros que avanzan por sus respectivas listas,
 * comparando elementos y copiando el más pequeño.
 *
 * @param left Un array ordenado.
 * @param right Otro array ordenado.
 * @return Un único array fusionado y ordenado.
 */
private func merge<T: Comparable>(_ left: [T], _ right: [T]) -> [T] {
    
    // Índices para rastrear el progreso en cada array
    var leftIndex = 0
    var rightIndex = 0
    
    var orderedArray: [T] = []
    orderedArray.reserveCapacity(left.count + right.count)
    
    while leftIndex < left.count && rightIndex < right.count {
        if left[leftIndex] < right[rightIndex] {
            orderedArray.append(left[leftIndex])
            leftIndex += 1
        } else {
            orderedArray.append(right[rightIndex])
            rightIndex += 1
        }
    }
    
    orderedArray.append(contentsOf: left[leftIndex...])
    
    orderedArray.append(contentsOf: right[rightIndex...])
    
    return orderedArray
}

// --- PROGRAMA PRINCIPAL ---

let arguments = Array(CommandLine.arguments[1...])

guard !arguments.isEmpty else {
    print("Uso: swift b2.swift <elemento1> <elemento2> <elemento3> ...")
    exit(1) 
}

let numbers = arguments.compactMap { Int($0) }

if numbers.count == arguments.count {
    
    let sortedNumbers = mergesort(numbers)
    
    print("\nOriginal: \(numbers)")
    print("Ordenado: \(sortedNumbers)")
    
} else {
    
    let sortedStrings = mergesort(arguments)
    
    print("\nOriginal: \(arguments)")
    print("Ordenado: \(sortedStrings)")
}