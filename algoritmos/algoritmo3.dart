void insertionSort(List<int> arr) {
  for (int i = 1; i < arr.length; i++) {
    int key = arr[i];
    int j = i - 1;

    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      j = j - 1;
    }
    arr[j + 1] = key;
  }
}

void main() {
  List<int> numbers = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
  print("Antes de ordenar: $numbers");
  insertionSort(numbers);
  print("Después de ordenar: $numbers");
}
