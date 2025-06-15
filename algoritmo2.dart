import 'dart:math';

double calcularArea(double radio) {
  const double pi = 3.1416;
  return pi * radio * radio;
}

void main() {
  double r = 5;
  var area = calcularArea(r);
  print("El área es: $area");
}