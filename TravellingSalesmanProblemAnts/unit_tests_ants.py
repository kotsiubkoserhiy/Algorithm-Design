import unittest
from TravellingSalesmanProblem import TravellingSalesmanProblem, np

class TestTravellingSalesmanProblem(unittest.TestCase):

    def setUp(self):
        self.num_vertices = 5
        self.alpha = 1
        self.beta = 1
        self.rho = 0.1
        self.ants = 2
        self.iterations = 100
        self.report_interval = 5
        self.tsp = TravellingSalesmanProblem(self.num_vertices, self.alpha, self.beta,
                   self.rho, self.ants, self.iterations, self.report_interval)

    def test_generate_distance_matrix(self):
        matrix = self.tsp.generate_distance_matrix()
        self.assertEqual(matrix.shape, (self.num_vertices, self.num_vertices))
        self.assertTrue(np.all(np.diag(matrix) == np.inf))

    def test_greedy_algorithm(self):
        path_length, path = self.tsp.greedy_algorithm()
        self.assertIsInstance(path_length, float)
        self.assertEqual(len(path), self.num_vertices)

    def test_initialize_pheromone_matrix(self):
        Lmin = 100.0
        pheromone_matrix = self.tsp.initialize_pheromone_matrix(Lmin)
        self.assertEqual(pheromone_matrix.shape, (self.num_vertices, self.num_vertices))
        self.assertTrue(np.all(pheromone_matrix == 1 / Lmin))

if __name__ == '__main__':
    unittest.main()
