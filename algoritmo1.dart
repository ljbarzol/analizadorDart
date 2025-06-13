int calcularFactorial(int n) {
  int resultado = 1;
  for (int i = 1; i <= n; i++) {
    resultado *= i;
  }
  return resultado;
}

void main() {
  int numero = 5;
  var factorial = calcularFactorial(numero);
  if (factorial == 120) {
    print("El factorial de $numero es $factorial");
  }
}
