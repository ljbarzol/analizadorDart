void main() {
  try {
    int resultado = dividir(10, 0);
    print("Resultado: $resultado");
  } catch (e) {
    print("Ocurrió un error: $e");
  } finally {
    print("Esto siempre se ejecuta, con o sin error.");
  }
}

int dividir(int a, int b) {
  return a ~/ b; // División entera (lanza error si b es 0)
}

