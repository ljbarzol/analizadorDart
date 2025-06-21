//FACTORIAL
/*
El factorial es el producto de todos los enteros positivos menores o iguales a n. 
Por ejemplo, el factorial de 5 (escrito como 5!) es 5 * 4 * 3 * 2 * 1 = 120. El factorial de 0, por definición, es igual a 1 (0! = 1). 
*/

import 'dart:io';

const int LIMITE_SUPERIOR = 20; // Límite máximo aceptado para evitar overflow

int calcularFactorialIterativo(int n) {
  if (n < 0) throw ArgumentError("El número no puede ser negativo");
  int resultado = 1;
  for (int i = 2; i <= n; i++) {
    resultado *= i;
  }
  return resultado;
}

int calcularFactorialRecursivo(int n) {
  if (n < 0) throw ArgumentError("El número no puede ser negativo");
  if (n == 0 || n == 1) return 1;
  return n * calcularFactorialRecursivo(n - 1);
}

bool validarEntrada(dynamic valor) {
  if (valor is! int) return false;
  return valor >= 0 && valor <= LIMITE_SUPERIOR;
}

void mostrarResultado(int numero, int resultado) {
  print("El factorial de $numero es $resultado");
}

void main() {
  print("Ingrese un número entero positivo (máximo $LIMITE_SUPERIOR):");
  String? entrada = stdin.readLineSync();
  
  try {
    int numero = int.parse(entrada ?? "0");

    if (!validarEntrada(numero)) {
      print("Número inválido. Intente nuevamente con un entero entre 0 y $LIMITE_SUPERIOR.");
      return;
    }

    int resultadoIterativo = calcularFactorialIterativo(numero);
    int resultadoRecursivo = calcularFactorialRecursivo(numero);

if (resultadoIterativo != resultadoRecursivo) {
      print("¡Alerta! Los métodos iterativo y recursivo no coinciden.");
    } else {
      mostrarResultado(numero, resultadoIterativo);
    }
} catch (e) {
    print("Error de entrada: $e");
  }

}
