import Foundation

/// Define el orden de la expresión de entrada.
enum Order: String {
    case pre = "PRE"
    case post = "POST"
}

struct ExpressionProcessor {
    
    func buildTree(from components: [String], order: Order) -> ArithmeticExpression? {
        var mutableComponents = components
        
        let expression: ArithmeticExpression?
        
        switch order {
        case .pre:
            expression = parsePrefix(tokens: &mutableComponents)
            // Una expresión prefija válida debe consumir TODOS los tokens
            return mutableComponents.isEmpty ? expression : nil
        case .post:
            expression = parsePostfix(tokens: components)
            // El parseo postfijo ya valida si sobran tokens (stack.count != 1)
            return expression
        }
    }
    
    private func parsePrefix(tokens: inout [String]) -> ArithmeticExpression? {
        
        guard !tokens.isEmpty else {
            return nil 
        }
        let token = tokens.removeFirst()
        
        if let number = Int(token) {
            // Caso base
            return .number(number)
        } else if let op = Operator(rawValue: token) {
            // Caso recursivo
            guard let left = parsePrefix(tokens: &tokens),
                  let right = parsePrefix(tokens: &tokens) else {
                return nil // Faltan operandos
            }
            return .operation(op, left, right)
        }
        
        return nil // Token inválido
    }
    
    /// Parsea una expresión en orden.
    private func parsePostfix(tokens: [String]) -> ArithmeticExpression? {
        var stack: [ArithmeticExpression] = []
        
        for token in tokens {
            if let number = Int(token) {
                stack.append(.number(number))
            } else if let op = Operator(rawValue: token) {
                guard let right = stack.popLast(), let left = stack.popLast() else {
                    return nil 
                }
                // Crea un nuevo sub-árbol y lo apila
                stack.append(.operation(op, left, right))
            } else {
                return nil 
            }
        }
        
        return stack.count == 1 ? stack.first : nil
    }
}