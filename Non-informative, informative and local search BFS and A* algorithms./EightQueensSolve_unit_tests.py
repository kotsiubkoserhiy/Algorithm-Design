import unittest
from main import EightQueensSolver

class TestEightQueensSolver(unittest.TestCase):
    def test_positive_case_bfs(self):
        solver = EightQueensSolver(size=4)
        solutions = solver.solve_bfs()
        for solution in solutions:
            self.assertEqual(len(solution), solver.size)
            self.assertFalse(solver.conflict(solution))

    def test_negative_case_bfs(self):
        solver = EightQueensSolver(size=0)
        solutions = solver.solve_bfs()
        self.assertEqual(solutions, [])

    def test_boundary_case_a_star(self):
        solver = EightQueensSolver(size=1)
        solution = solver.solve_a_star()
        if solution:
            self.assertEqual(len(solution), solver.size)
            self.assertFalse(solver.conflict(solution))

if __name__ == '__main__':
    unittest.main()
