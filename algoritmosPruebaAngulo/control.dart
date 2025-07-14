void main() {
  int sum = 0;

  for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) {
      continue; // Saltar números pares
    }

    if (i > 7) {
      break; // Salir cuando i sea mayor que 7
    }

    sum = sum + i;
    print("Valor de i: $i, suma actual: $sum");
  }

  int j = 0;
  while (j < 3) {
    print("Ciclo while, j = $j");
    j = j + 1;
  }

  print("Suma final: $sum");
}
