// Función que calcula el factorial de un número entero positivo
int factorial(int n) {
  if (n < 0) {
    throw ArgumentError('El número debe ser positivo');
  }
  
  int resultado = 1;
  for (int i = 1; i <= n; i++) {
    resultado *= i;
  }
  return resultado;
}

void main() {
  int numero = 5;
  try {
    int fact = factorial(numero);
    print('El factorial de $numero es $fact');
  } catch (e) {
    print('Error: $e');
  }
}

