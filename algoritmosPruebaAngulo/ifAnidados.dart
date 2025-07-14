void main() {
  int nota = 85;

  if (nota >= 0 && nota <= 100) {
    if (nota >= 90) {
      print("Excelente");
    } else {
      if (nota >= 75) {
        print("Muy bien");
      } else {
        if (nota >= 60) {
          print("Suficiente");
        } else {
          print("Reprobado");
        }
      }
    }
  } else {
    print("Nota inválida");
  }
}

