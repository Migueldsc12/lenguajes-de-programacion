import Foundation

// Constantes
let X = 2
let Y = 7
let Z = 4

let alpha = ((X + Y) % 5) + 3
let beta = ((Y + Z) % 5) + 3
let limit = alpha * beta

//(a) Subrutina Recursiva
func subrutinaRecursiva(_ n: Int) -> Int {
    if n < limit { return n }
    var suma = 0
    for i in 1...alpha {
        suma += subrutinaRecursiva(n - beta * i)
    }
    return suma
}

// (b) Subrutina Recursiva de Cola
func subrutinaCola(_ n: Int) -> Int {
    if n < 0 { return n }
    var dp = [Int](repeating: 0, count: n + 1)
    return subrutinaColaAux(k: 0, n: n, dp: &dp)
}

// Función auxiliar
private func subrutinaColaAux(k: Int, n: Int, dp: inout [Int]) -> Int {
    if k > n { return dp[n] }
    
    let valorK: Int
    if k < limit {
        valorK = k
    } else {
        var suma = 0
        for i in 1...alpha {
            suma += dp[k - beta * i]
        }
        valorK = suma
    }
    dp[k] = valorK
    return subrutinaColaAux(k: k + 1, n: n, dp: &dp)
}

// (c) Subrutina Iterativa
func subrutinaIterativa(_ n: Int) -> Int {
    if n < 0 { return n }
    var dp = [Int](repeating: 0, count: n + 1)
    for k in 0...n {
        if k < limit {
            dp[k] = k
        } else {
            var suma = 0
            for i in 1...alpha {
                suma += dp[k - beta * i]
            }
            dp[k] = suma
        }
    }
    return dp[n]
}

func measureTime(of block: () -> Int) -> (result: Int, duration: TimeInterval) {
    let startTime = Date()
    let result = block()
    let endTime = Date()
    let duration = endTime.timeIntervalSince(startTime)
    return (result, duration)
}

// --- Función Principal de Ejecución ---
func runAnalysis() {
    print("--- Análisis de F(n) con α = \(alpha) y β = \(beta) (Límite = \(limit)) ---")
    print("--------------------------------------------------\n")
    
    print("--- (a) Subrutina Recursiva (Directa) ---")
    
    let smallNValues = [10, 20, 28, 30, 32, 35]
    for n in smallNValues {
        let (result, duration) = measureTime {
            subrutinaRecursiva(n)
        }
        print(String(format: "F_rec(\(n)): \t Resultado = \(result), \t Tiempo = %.6f s", duration))
    }
    
    print("--- (b) y (c) Recursiva de Cola vs. Iterativa ---")

    let mediumNValues = [35, 100]
    
    print("\n--- (b) Subrutina de Cola ---")
    for n in mediumNValues {
        let (result, duration) = measureTime {
            subrutinaCola(n)
        }
        print(String(format: "F_cola(\(n)): \t Resultado = \(result), \t Tiempo = %.6f s", duration))
    }

    print("\n--- (c) Subrutina Iterativa ---")
    for n in mediumNValues {
        let (result, duration) = measureTime {
            subrutinaIterativa(n)
        }
        print(String(format: "F_iter(\(n)): \t Resultado = \(result), \t Tiempo = %.6f s", duration))
    }
    
    print("\n--- Conclusiones del Análisis ---")
    print("""
    1.  (a) Recursión Directa: Computacionalmente inviable (lento).
    
    2.  (b) Recursión de Cola: Rápida con valores pequeños (n=100), pero
        INESTABLE. Se sabe que causa un crash del compilador
        en este sistema (Swift 6.2/Linux) con n >= 1000.
        
    3.  (c) Iterativa: Es la solución óptima. Es rápida y robusta
        con valores pequeños y, a diferencia de (b),
        también funciona con valores grandes (n=10000+).

    Eficiencia y Estabilidad: (c) Iterativa > (b) Recursiva de Cola > (a) Recursiva Directa
    """)
}

// Ejecutar el análisis
runAnalysis()