import heapq
import os
import time
import random

class SortAlgorithm:
    def __init__(self, input_file, output_file, available_memory):
        self.input_file = input_file
        self.output_file = output_file
        self.available_memory = available_memory

    def run(self):
        pass

    def generate_large_random_numbers_file(self, target_size_in_bytes):
        try:
            with open(self.input_file, 'w') as f:
                while os.path.getsize(self.input_file) < target_size_in_bytes:
                    number = random.randint(1, 1000000)
                    f.write(str(number) + '\n')
        except Exception as e:
            print(f"Помилка: {e}")

def merge_sorted_files(files, output_file):
    temp_files_handles = [open(file, 'r') for file in files]
    heap = [(int(file_handle.readline().strip()), i) for i, file_handle in enumerate(temp_files_handles) if file_handle.readline()]
    heapq.heapify(heap)

    with open(output_file, 'w') as outfile:
        while heap:
            try:
                value, index = heapq.heappop(heap)
                outfile.write(str(value) + '\n')
                next_line = temp_files_handles[index].readline().strip()
                if next_line:
                    next_value = int(next_line)
                    heapq.heappush(heap, (next_value, index))
            except Exception as e:
                print(f"Помилка при обробці файлу: {e}")

class BalancedMultiwayMergeSort(SortAlgorithm):
    def run(self):
        chunk_size = self.available_memory // 2

        try:
            def split_input_file(file):
                chunks = []
                while True:
                    chunk = []
                    while sum(chunk) < chunk_size:
                        line = file.readline().strip()
                        if not line:
                            break
                        chunk.append(int(line))
                    if not chunk:
                        break
                    chunk.sort()
                    chunks.append(chunk)
                return chunks

            def merge_sorted_chunks(chunks, output_file):
                heap = [(chunk[0], idx, 0) for idx, chunk in enumerate(chunks)]
                heapq.heapify(heap)

                while heap:
                    value, chunk_idx, index_in_chunk = heapq.heappop(heap)
                    output_file.write(str(value) + '\n')
                    index_in_chunk += 1
                    if index_in_chunk < len(chunks[chunk_idx]):
                        heapq.heappush(heap, (chunks[chunk_idx][index_in_chunk], chunk_idx, index_in_chunk))

            with open(self.input_file, 'r') as infile:
                chunks = split_input_file(infile)

                if not chunks:
                    print("Помилка: Немає даних для сортування.")
                    return

                with open(self.output_file, 'w') as outfile:
                    start_time = time.time()
                    merge_sorted_chunks(chunks, outfile)
                    end_time = time.time()

                    elapsed_time = round(end_time - start_time, 2)
                    print(f"Час роботи алгоритму: {elapsed_time} секунд")

        except Exception as e:
            print(f"Помилка: {e}")
            raise e