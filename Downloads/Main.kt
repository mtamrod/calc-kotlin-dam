fun main(args: Array) {
    val (operation, num1, num2) = parseArguments(args)
    val result = when (operation) {
        "multiplica" -> multiplica(num1, num2)
        "divide" -> divideE(num1, num2)
        else -> throw IllegalArgumentException("Operación no soportada")
    }
    showResult(operation, result)
}