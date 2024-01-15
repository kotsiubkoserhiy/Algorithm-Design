import unittest
from balanced_multiway_merge_sort import BalancedMultiwayMergeSort


class TestSortingAlgorithms(unittest.TestCase):
    def test_positive_case(self):
        input_file = 'test_input.txt'
        output_file = 'test_output.txt'
        available_memory = 1024 * 1024 * 100
        file_size = 15000000  # Змінили розмір на 10 МБ
        algorithm = BalancedMultiwayMergeSort(input_file, output_file, available_memory)
        algorithm.generate_large_random_numbers_file(file_size)
        algorithm.run()

        with open(output_file, 'r') as sorted_file:
            lines = sorted_file.readlines()
            self.assertEqual(lines, sorted(lines, key=lambda x: int(x.strip())))

    def test_negative_case(self):
        input_file = 'non_existent_input.txt'
        output_file = 'test_output.txt'
        available_memory = 1024 * 1024 * 100
        algorithm = BalancedMultiwayMergeSort(input_file, output_file, available_memory)

        with self.assertRaises(Exception):
            algorithm.run()

    def test_boundary_case(self):
        input_file = 'test_boundary_input.txt'
        output_file = 'test_boundary_output.txt'
        available_memory = 1024 * 1024 * 100
        file_size = 10000000
        algorithm = BalancedMultiwayMergeSort(input_file, output_file, available_memory)
        algorithm.generate_large_random_numbers_file(file_size)
        algorithm.run()

        with open(output_file, 'r') as sorted_file:
            lines = sorted_file.readlines()
            self.assertEqual(lines, sorted(lines, key=lambda x: int(x.strip())))


if __name__ == '__main__':
    unittest.main()
