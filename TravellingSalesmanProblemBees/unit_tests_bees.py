from TravellingSalesmanProblem import BeeAlgorithm, np
import unittest

class TestTravellingSalesmanProblem(unittest.TestCase):
    def test_generate_distance_matrix(self):
        num_vertices = 6
        bee_algo = BeeAlgorithm(num_vertices, 10, 5, 2, 1, 10, 1)
        matrix = bee_algo.generate_distance_matrix()
        assert matrix.shape == (num_vertices, num_vertices), "Matrix dimensions are incorrect"
        assert all(matrix.diagonal() == np.inf), "Diagonal should be inf"


    def test_random_solution(self):
        num_vertices = 6
        bee_algo = BeeAlgorithm(num_vertices, 10, 5, 2, 1, 10, 1)
        solution = bee_algo._random_solution()
        assert len(solution) == num_vertices, "Solution length is incorrect"
        assert sorted(solution) == list(range(num_vertices)), "Solution should be a permutation"

    def test_total_distance(self):
        num_vertices = 6
        bee_algo = BeeAlgorithm(num_vertices, 10, 5, 2, 1, 10, 1)
        solution = list(range(num_vertices))
        expected_distance = sum(bee_algo.distance_matrix[i, (i + 1) % num_vertices] for i in range(num_vertices))
        calculated_distance = bee_algo._total_distance(solution)
        self.assertEqual(calculated_distance, expected_distance, "Total distance calculation is incorrect")


if __name__ == '__main__':
    unittest.main()