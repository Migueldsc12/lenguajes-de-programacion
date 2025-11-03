import XCTest
@testable import pregunta2

final class ExpressionTests: XCTestCase {

    let processor = ExpressionProcessor()

    // Parsea los tokens helper
    private func parse(order: Order, _ tokens: String) -> ArithmeticExpression? {
        let components = tokens.split(separator: " ").map(String.init)
        return processor.buildTree(from: components, order: order)
    }

    //Pruebas de Ejemplos (EVAL)
    
    func testEvalExample1() {
        let expr = parse(order: .pre, "+ * + 3 4 5 7")
        XCTAssertEqual(expr?.evaluate(), 42)
    }
    
    func testEvalExample2() {
        let expr = parse(order: .post, "8 3 - 8 4 4 + * +")
        XCTAssertEqual(expr?.evaluate(), 69)
    }

    //Pruebas de Ejemplos (MOSTRAR)
    
    func testMostrarExample1() {
        let expr = parse(order: .pre, "+ * + 3 4 5 7")
        XCTAssertEqual(expr?.toInfix(), "(3 + 4) * 5 + 7")
    }

    func testMostrarExample2() {
        let expr = parse(order: .post, "8 3 - 8 4 4 + * +")
        XCTAssertEqual(expr?.toInfix(), "8 - 3 + 8 * (4 + 4)")
    }
    
    //Pruebas Adicionales (Casos Borde)
    
    func testDivisionByZero() {
        let expr = parse(order: .pre, "/ 10 0")
        XCTAssertNil(expr?.evaluate())
    }
    
    func testPrecedenceInfix() {
        let expr = parse(order: .pre, "* + 2 3 4")
        XCTAssertEqual(expr?.toInfix(), "(2 + 3) * 4")
    }
    
    func testLeftAssociativityInfix() {
        let expr = parse(order: .pre, "- - 10 5 3")
        XCTAssertEqual(expr?.toInfix(), "10 - 5 - 3")
    }
    
    func testRightChildAssociativityInfix() {
        let expr = parse(order: .pre, "- 10 - 5 3")
        XCTAssertEqual(expr?.toInfix(), "10 - (5 - 3)")
    }
    
    func testMixedPrecedenceInfix() {
        let expr = parse(order: .pre, "- + 1 * 2 3 / 4 5")
        XCTAssertEqual(expr?.toInfix(), "1 + 2 * 3 - 4 / 5")
        XCTAssertEqual(expr?.evaluate(), 1 + 2 * 3 - 4 / 5)
    }

    //Pruebas de Expresiones Mal Formadas

    func testInvalidPrefixTooFewOperands() {
        XCTAssertNil(parse(order: .pre, "+ 5"))
    }
    
    func testInvalidPrefixTooManyOperands() {
        XCTAssertNil(parse(order: .pre, "+ 5 4 3"))
    }
    
    func testInvalidPostfixTooFewOperands() {
        XCTAssertNil(parse(order: .post, "5 +"))
    }
    
    func testInvalidPostfixTooManyOperands() {
        XCTAssertNil(parse(order: .post, "5 4 3 +"))
    }
    
    func testInvalidToken() {
        XCTAssertNil(parse(order: .pre, "+ 1 Z"))
        XCTAssertNil(parse(order: .post, "1 Z +"))
    }
}