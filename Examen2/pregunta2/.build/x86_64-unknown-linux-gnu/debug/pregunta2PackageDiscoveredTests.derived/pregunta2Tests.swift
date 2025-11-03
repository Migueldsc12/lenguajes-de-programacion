import XCTest
@testable import pregunta2Tests

fileprivate extension ExpressionTests {
    @available(*, deprecated, message: "Not actually deprecated. Marked as deprecated to allow inclusion of deprecated tests (which test deprecated functionality) without warnings")
    static nonisolated(unsafe) let __allTests__ExpressionTests = [
        ("testDivisionByZero", testDivisionByZero),
        ("testEvalExample1", testEvalExample1),
        ("testEvalExample2", testEvalExample2),
        ("testInvalidPostfixTooFewOperands", testInvalidPostfixTooFewOperands),
        ("testInvalidPostfixTooManyOperands", testInvalidPostfixTooManyOperands),
        ("testInvalidPrefixTooFewOperands", testInvalidPrefixTooFewOperands),
        ("testInvalidPrefixTooManyOperands", testInvalidPrefixTooManyOperands),
        ("testInvalidToken", testInvalidToken),
        ("testLeftAssociativityInfix", testLeftAssociativityInfix),
        ("testMixedPrecedenceInfix", testMixedPrecedenceInfix),
        ("testMostrarExample1", testMostrarExample1),
        ("testMostrarExample2", testMostrarExample2),
        ("testPrecedenceInfix", testPrecedenceInfix),
        ("testRightChildAssociativityInfix", testRightChildAssociativityInfix)
    ]
}
@available(*, deprecated, message: "Not actually deprecated. Marked as deprecated to allow inclusion of deprecated tests (which test deprecated functionality) without warnings")
func __pregunta2Tests__allTests() -> [XCTestCaseEntry] {
    return [
        testCase(ExpressionTests.__allTests__ExpressionTests)
    ]
}