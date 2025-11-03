import Foundation

/// Ejecuta el bucle principal de la calculadora.
func runCalculator() {
    let processor = ExpressionProcessor()
    
    print("Calculadora de expresiones. Ingrese su acción (EVAL, MOSTRAR) o SALIR.")
    print("> ", terminator: "")
    
    while let line = readLine() {
        let components = line.split(separator: " ").map(String.init)
        
        guard let command = components.first?.uppercased() else {
            print("> ", terminator: "") // Línea vacía, pedir de nuevo
            continue
        }
        
        // Acción SALIR
        if command == "SALIR" {
            print("Adiós.")
            break
        }
        
        // Validar que el comando tiene suficientes partes
        guard components.count >= 3 else {
            print("Error: Acción incompleta. Formato: <COMANDO> <orden> <expr>")
            print("> ", terminator: "")
            continue
        }
        
        // Validar el <orden> (PRE o POST)
        guard let order = Order(rawValue: components[1].uppercased()) else {
            print("Error: Orden desconocido. Use PRE o POST.")
            print("> ", terminator: "")
            continue
        }
        
        // Extraer la expresión
        let exprComponents = Array(components[2...])
        
        // Intentar construir el árbol
        guard let expression = processor.buildTree(from: exprComponents, order: order) else {
            print("Error: Expresión mal formada.")
            print("> ", terminator: "")
            continue
        }
        
        // Ejecutar la acción
        switch command {
        case "EVAL":
            if let result = expression.evaluate() {
                print(result)
            } else {
                print("Error: División por cero.")
            }
        
        case "MOSTRAR":
            print(expression.toInfix())
            
        default:
            print("Error: Comando desconocido. Use EVAL, MOSTRAR o SALIR.")
        }
        
        // Pedir la siguiente acción
        print("> ", terminator: "")
    }
}

// Iniciar el programa
runCalculator()