String clasificarNota(int nota) {
  if (nota < 0 || nota > 100) {
    return "Nota inválida";
  } else if (nota >= 90) {
    return "Excelente";
  } else if (nota >= 75) {
    return "Muy bien";
  } else if (nota >= 60) {
    return "Suficiente";
  } else {
    return "Reprobado";
  }
}

void main() {
  int nota = 85;
  String resultado = clasificarNota(nota);
  print("Resultado: $resultado");
}

