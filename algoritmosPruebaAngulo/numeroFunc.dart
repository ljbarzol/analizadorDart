int sumar(int a, int b) {
  return a + b;
}

double dividir(double a, double b) {
  return a / b;
}

void saludar(String nombre) {
  print("Hola, $nombre!");
}

void main() {
  int resultadoSuma = sumar(2, 3); // ✔️ correcto
  print("Suma: $resultadoSuma");

  double resultadoDivision = dividir(10, 2); // ✔️ correcto
  print("División: $resultadoDivision");

  saludar("Dart"); // ✔️ correcto

  // ❌ Argumentos de más
  int errorSuma = sumar(1, 2, 3); // ERROR: sumar espera 2 argumentos

  // ❌ Argumentos de menos
  double errorDivision = dividir(5); // ERROR: dividir espera 2 argumentos
}
