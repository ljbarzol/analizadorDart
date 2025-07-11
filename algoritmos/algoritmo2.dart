void main() {
  List<int> numeros = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
  int objetivo = 13;

  int resultado = busquedaBinaria(numeros, objetivo);

  if (resultado != -1) {
    print('Elemento encontrado en la posición $resultado');
  } else {
    print('Elemento no encontrado');
  }
  for (int i = 0; i < numeros.length; i++) {
    if (numeros[i] == objetivo) {
      print('Encontrado con for: ${numeros[i]}');
      break;
    } else if (numeros[i] % 2 == 0) {
      continue;
    } else {
      print('Valor actual en for: ${numeros[i]}');
    }
  }
  int index = 0;
  while (index < numeros.length) {
    if (numeros[index] == objetivo) {
      print('Encontrado con while: ${numeros[index]}');
      break;
    }
    index++;
  }
}
int busquedaBinaria(List<int> lista, int valor) {
  int izquierda = 0;
  int derecha = lista.length - 1;

  while (izquierda <= derecha) {
    int medio = (izquierda + derecha) ~/ 2;

    if (lista[medio] == valor) {
      return medio;
    } else if (lista[medio] < valor) {
      izquierda = medio + 1;
    } else {
      derecha = medio - 1;
    }
  }
  return -1;
}