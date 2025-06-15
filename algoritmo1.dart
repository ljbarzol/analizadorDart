
//FACTORIAL
/*
El factorial es el producto de todos los enteros positivos menores o iguales a n. 
Por ejemplo, el factorial de 5 (escrito como 5!) es 5 * 4 * 3 * 2 * 1 = 120. El factorial de 0, por definición, es igual a 1 (0! = 1). 
*/
int calcularFactorial(int n) {
  int resultado = 1;
  for (int i = 1; i <= n; i++) {
    resultado *= i;
  }
  return resultado;
}

void main() {
  int numero = 5;
  var factorial = calcularFactorial(numero);
  if (factorial == 120) {
    print("El factorial de $numero es $factorial");
  }
}
