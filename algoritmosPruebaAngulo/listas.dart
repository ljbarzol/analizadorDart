void main() {
  // Declarar una lista de strings
  List<String> lenguajes = ['php', 'python', 'dart'];

  print("Lista de lenguajes: $lenguajes");

  // Agregar un elemento
  lenguajes.add('javascript');
  print("Después de agregar: $lenguajes");

  // Eliminar un elemento
  lenguajes.remove('php');
  print("Después de eliminar 'php': $lenguajes");

  // Acceder por índice
  print("Primer lenguaje: ${lenguajes[0]}");

  // Recorrer la lista con for clásico
  for (int i = 0; i < lenguajes.length; i++) {
    print("Lenguaje en posición $i: ${lenguajes[i]}");
  }

  // Usar propiedades de la lista
  print("Longitud de la lista: ${lenguajes.length}");
  print("Está vacía?: ${lenguajes.isEmpty}");
}
