void main() {
  List<int> numeros = [1, 2, 3];
  if (numeros.contains(2)) {
    print('Contiene el 2');
  }

  Set<String> frutas = {'manzana', 'pera'};
  if (frutas.contains('pera')) {
    print('Sí hay pera');
  }

  Map<String, int> stock = {'lapiz': 10, 'borrador': 0};
  if (stock['borrador']! > 0) {
    print('Hay borradores');
  } else {
    print('No hay borradores');
  }
}
