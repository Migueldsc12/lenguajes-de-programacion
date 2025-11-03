import Foundation

func f(_ n: Int) -> Int {
    // Usamos el operador ternario para una implementación concisa
    return n % 2 == 0 ? (n / 2) : (3 * n + 1)
}


func count(_ n: Int) -> Int {
    // Si n ya es 1, se necesitan 0 pasos.
    if n == 1 {
        return 0
    }
    
    var steps = 0
    var currentValue = n
    
    // Iteramos el valor actual no sea 1
    while currentValue != 1 {
        // 1. Aplicamos la función f
        currentValue = f(currentValue)
        
        // 2. Incrementamos el contador de pasos
        steps += 1
    }
    
    // Devolvemos el total de pasos cuando el bucle termina (currentValue == 1)
    return steps
}

// --- PROGRAMA PRINCIPAL ---

guard CommandLine.arguments.count > 1 else {
    print("Error: No se proporcionó un número.")
    print("Uso: swift tu_script.swift <numero>")
    exit(1) 
}

guard let n = Int(CommandLine.arguments[1]) else {
    print("Error: El argumento '\(CommandLine.arguments[1])' no es un número entero válido.")
    exit(1)
}

guard n > 0 else {
    print("Error: El número debe ser un entero positivo mayor que 0.")
    exit(1)
}

let resultado = count(n)

print("\(resultado)")