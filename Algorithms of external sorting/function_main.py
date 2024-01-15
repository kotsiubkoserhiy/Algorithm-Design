from balanced_multiway_merge_sort import BalancedMultiwayMergeSort
from modified_balanced_multiway_merge_sort import ModifiedBalancedMultiwayMergeSort

def main():
    while True:
        print("Вибір алгоритма сортування (1 - збалансоване багатошляхове злиття, "
              "2 - модифікований збалансоване багатошляхове злиття): ")
        choice = input()

        if choice == '1':
            available_memory = 1024 * 1024 * 100
            input_file = 'large_input.txt'
            output_file = 'sorted_output.txt'
            while True:
                try:
                    file_size = int(input("Розмір файлу в байтах (мінімум 10 мб): "))
                    if file_size < 10000000:
                        print("Розмір файлу має бути не менше 10 мб (10000000 байт).")
                    else:
                        break
                except ValueError:
                    print("Введіть коректний розмір файлу (у байтах).")
            algorithm = BalancedMultiwayMergeSort(input_file, output_file, available_memory)
            algorithm.generate_large_random_numbers_file(file_size)
            algorithm.run()
            break
        elif choice == '2':
            chunk_size = 100 * 1024 * 1024
            input_file = 'large_input.txt'
            output_file = 'sorted_output.txt'
            while True:
                try:
                    file_size = int(input("Розмір файлу в байтах (мінімум 10 мб): "))
                    if file_size < 10000000:
                        print("Розмір файлу має бути не менше 10 мб (10000000 байт).")
                    else:
                        break
                except ValueError:
                    print("Введіть коректний розмір файлу (у байтах).")
            algorithm = ModifiedBalancedMultiwayMergeSort(input_file, output_file, chunk_size)
            algorithm.generate_large_random_numbers_file(file_size)
            algorithm.run()
            break
        else:
            print("Помилка. Виберіть 1 або 2.")

