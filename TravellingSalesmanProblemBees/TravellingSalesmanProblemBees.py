import numpy as np
import matplotlib.pyplot as plt
from numpy.random import choice

class BeeAlgorithm:
    def __init__(self, num_vertices, n_bees, n_sites, elite_sites, ngh_size, iterations, report_interval):
        self.num_vertices = num_vertices
        self.n_bees = n_bees
        self.n_sites = n_sites
        self.elite_sites = elite_sites
        self.ngh_size = ngh_size
        self.iterations = iterations
        self.report_interval = report_interval
        self.distance_matrix = self.generate_distance_matrix()
        self.best_path_length = np.inf
        self.best_path = None

    def generate_distance_matrix(self):
        matrix = np.random.randint(1, 51, size=(self.num_vertices, self.num_vertices)).astype(float)
        np.fill_diagonal(matrix, np.inf)
        return matrix

    def _random_solution(self):
        solution = list(range(self.num_vertices))
        np.random.shuffle(solution)
        return solution

    def _total_distance(self, solution):
        return sum(self.distance_matrix[solution[i], solution[i + 1]] for i in range(-1, self.num_vertices - 1))

    def _local_search(self, solution):
        best_solution = solution
        best_distance = self._total_distance(solution)
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                new_solution = solution[:]
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                new_distance = self._total_distance(new_solution)
                if new_distance < best_distance:
                    best_solution, best_distance = new_solution, new_distance
        return best_solution

    def _choose_bees(self, solutions):
        sorted_solutions = sorted(solutions, key=lambda x: self._total_distance(x))
        return sorted_solutions[:self.n_sites]

    def get_iterations(self):
        while True:
            try:
                iterations = int(input("Enter the number of iterations (>1): "))
                if iterations > 1:
                    return iterations
                else:
                    print("Please enter a positive integer (>1).")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    def run(self):
        self.iterations = self.get_iterations()
        quality_over_time = []

        for iteration in range(self.iterations):
            solutions = [self._random_solution() for _ in range(self.n_bees)]
            elite_solutions = self._choose_bees(solutions)[:self.elite_sites]
            other_solutions = self._choose_bees(solutions)[self.elite_sites:]

            for solution in elite_solutions + other_solutions:
                new_solution = self._local_search(solution)
                new_distance = self._total_distance(new_solution)
                if new_distance < self.best_path_length:
                    self.best_path_length, self.best_path = new_distance, new_solution

            if iteration % self.report_interval == 0 or iteration == self.iterations - 1:
                quality_over_time.append(self.best_path_length)
                print(f"Iteration {iteration}; Best path length = {self.best_path_length}")

        x_values = list(range(0, self.iterations, self.report_interval)) + [self.iterations]
        plt.plot(x_values, quality_over_time)
        plt.xlabel('Iteration')
        plt.ylabel('Best path length')
        plt.title('Dependence of the solution quality on the number of iterations')
        plt.grid(True)
        plt.show()
