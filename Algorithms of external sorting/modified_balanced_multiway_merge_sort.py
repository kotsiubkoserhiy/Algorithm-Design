from balanced_multiway_merge_sort import SortAlgorithm, merge_sorted_files
import tempfile
import os
import sys
import time


class ModifiedBalancedMultiwayMergeSort(SortAlgorithm):
    def run(self):
        chunk_size = 100 * 1024 * 1024

        try:
            def sort_large_file(input_file, output_file, chunk_size):
                temp_dir = tempfile.mkdtemp()
                temp_files = []

                with open(input_file, 'r') as infile:
                    chunk = []
                    while True:
                        line = infile.readline().strip()
                        if not line:
                            break
                        chunk.append(int(line))
                        if sys.getsizeof(chunk) >= chunk_size:
                            chunk.sort()
                            temp_file = os.path.join(temp_dir, f'temp_{len(temp_files)}.txt')
                            temp_files.append(temp_file)
                            with open(temp_file, 'w') as temp_outfile:
                                temp_outfile.writelines([str(num) + '\n' for num in chunk])
                            chunk = []

                    if chunk:
                        chunk.sort()
                        temp_file = os.path.join(temp_dir, f'temp_{len(temp_files)}.txt')
                        temp_files.append(temp_file)
                        with open(temp_file, 'w') as temp_outfile:
                            temp_outfile.writelines([str(num) + '\n' for num in chunk])

                start_time = time.time()
                merge_sorted_files(temp_files, self.output_file)
                end_time = time.time()

                elapsed_time = round(end_time - start_time, 2)
                print(f"Час роботи алгоритму: {elapsed_time} секунд")

            sort_large_file(self.input_file, self.output_file, chunk_size)

        except Exception as e:
            print(f"Помилка: {e}")
