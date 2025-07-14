void main() {
  // Map con claves String y valores int
  var edades = {
    'Alice': 25,
    'Bob': 30,
    'Charlie': 20
  };
  print(edades);

  // Map con claves String y valores String
  var capitales = {
    'Ecuador': 'Quito',
    'Peru': 'Lima',
    'Chile': 'Santiago'
  };
  print(capitales);

  // Map mixto con claves String e int, valores dinámicos
  var mixto = {
    'uno': 1,
    2: 'dos',
    'tres': 3.0,
    4: true
  };
  print(mixto);
}
