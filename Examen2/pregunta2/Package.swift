// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "pregunta2",
    targets: [
        .executableTarget(
            name: "pregunta2",
            dependencies: [],
            path: ".", 
            sources: [
                "main.swift",
                "expression.swift",
                "processor.swift"
            ]
        ),

        .testTarget(
            name: "pregunta2Tests",
            dependencies: ["pregunta2"], 
            path: ".", 
            sources: ["tests.swift"]
        )
    ]
)