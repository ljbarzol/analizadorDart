void main() {
  Set<int> numeros = {1, 2, 2, 2, 3, 3}; 

  print("Set original con duplicados: {1, 2, 2, 2, 3, 3}");
  print("Set almacenado (sin duplicados): $numeros");

  numeros.add(4);
  print("Después de agregar 4: $numeros");

  numeros.add(2);
  print("Después de intentar agregar otro 2: $numeros");

  if (numeros.contains(3)) {
    print("El conjunto contiene el número 3");
  }
}
