import Foundation

/// Representa los operadores aritméticos y su precedencia.
enum Operator: String, CaseIterable {
    case add = "+"
    case subtract = "-"
    case multiply = "*"
    case divide = "/"
    
    var precedence: Int {
        switch self {
        case .add, .subtract:
            return 1
        case .multiply, .divide:
            return 2
        }
    }
}

indirect enum ArithmeticExpression {
    case number(Int)
    case operation(Operator, ArithmeticExpression, ArithmeticExpression) // operador, izq, der
    
    // I. Lógica de EVAL
    
    func evaluate() -> Int? {
        switch self {
        case .number(let value):
            return value
            
        case .operation(let op, let left, let right):
            // Evalúa recursivamente los hijos
            guard let leftValue = left.evaluate(), let rightValue = right.evaluate() else {
                return nil 
            }
            
            // Realiza la operación
            switch op {
            case .add:
                return leftValue + rightValue
            case .subtract:
                return leftValue - rightValue
            case .multiply:
                return leftValue * rightValue
            case .divide:
                if rightValue == 0 {
                    return nil
                }
                return leftValue / rightValue // División entera
            }
        }
    }
    
    // II. Lógica de MOSTRAR
    
    func toInfix() -> String {
        return toInfix(parentPrecedence: 0, isRightChild: false)
    }
    
    private func toInfix(parentPrecedence: Int, isRightChild: Bool) -> String {
        switch self {
        case .number(let value):
            return "\(value)"
            
        case .operation(let op, let left, let right):
            let currentPrecedence = op.precedence
            
            // Convierte recursivamente los hijos
            let leftInfix = left.toInfix(parentPrecedence: currentPrecedence, isRightChild: false)
            let rightInfix = right.toInfix(parentPrecedence: currentPrecedence, isRightChild: true)
            
            let expressionString = "\(leftInfix) \(op.rawValue) \(rightInfix)"
            
            var needsParens = false
            
            if currentPrecedence < parentPrecedence {
                needsParens = true
            }
            else if currentPrecedence == parentPrecedence && isRightChild {
                needsParens = true
            }
            
            if needsParens {
                return "(\(expressionString))"
            } else {
                return expressionString
            }
        }
    }
}